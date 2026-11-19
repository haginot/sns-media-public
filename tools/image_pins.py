"""Compare commit-pinned sns-media-public image URLs with the blobs at HEAD."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Protocol

PIN_RE = re.compile(
    r"https://raw\.githubusercontent\.com/haginot/sns-media-public/"
    r"([0-9a-fA-F]{40})/([^\s\)<>\"']+)"
)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SKIP_DIRS = {".git", ".cursor"}


class Verdict(str, Enum):
    current = "current"
    stale = "stale"
    missing = "missing"
    unknown_commit = "unknown_commit"


@dataclass(frozen=True)
class ImagePin:
    markdown_path: str
    line: int
    commit: str
    object_path: str
    raw_url: str


@dataclass(frozen=True)
class Finding:
    pin: ImagePin
    verdict: Verdict
    pinned_blob: str | None
    head_blob: str | None


class BlobStore(Protocol):
    def commit_exists(self, commit: str) -> bool: ...

    def blob(self, commit: str, path: str) -> str | None: ...


class GitError(RuntimeError):
    pass


class GitBlobStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def head(self) -> str:
        result = self._git("rev-parse", "--verify", "HEAD")
        if result.returncode != 0:
            message = result.stderr.strip() or "HEAD is missing"
            raise GitError(message)
        return result.stdout.strip()

    def commit_exists(self, commit: str) -> bool:
        result = self._git("cat-file", "-t", commit)
        return result.returncode == 0 and result.stdout.strip() == "commit"

    def blob(self, commit: str, path: str) -> str | None:
        result = self._git("rev-parse", "--verify", "--quiet", f"{commit}:{path}")
        if result.returncode != 0:
            return None
        oid = result.stdout.strip()
        kind = self._git("cat-file", "-t", oid)
        if kind.returncode != 0 or kind.stdout.strip() != "blob":
            return None
        return oid

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True,
            text=True,
            check=False,
        )


def image_object_path(url_path: str) -> str | None:
    without_fragment = url_path.split("#", 1)[0]
    without_query = without_fragment.split("?", 1)[0]
    if PurePosixPath(without_query).suffix.lower() not in IMAGE_SUFFIXES:
        return None
    return urllib.parse.unquote(without_query)


def find_pins(markdown_text: str, markdown_path: str) -> tuple[ImagePin, ...]:
    pins: list[ImagePin] = []
    for line_number, line in enumerate(markdown_text.splitlines(keepends=True), start=1):
        for match in PIN_RE.finditer(line):
            object_path = image_object_path(match.group(2))
            if object_path is None:
                continue
            pins.append(
                ImagePin(
                    markdown_path=markdown_path,
                    line=line_number,
                    commit=match.group(1).lower(),
                    object_path=object_path,
                    raw_url=match.group(0),
                )
            )
    return tuple(pins)


def classify_pin(pin: ImagePin, blobs: BlobStore, head: str) -> Finding:
    if not blobs.commit_exists(pin.commit):
        return Finding(pin, Verdict.unknown_commit, None, None)
    pinned_blob = blobs.blob(pin.commit, pin.object_path)
    head_blob = blobs.blob(head, pin.object_path)
    if pinned_blob is None or head_blob is None:
        return Finding(pin, Verdict.missing, pinned_blob, head_blob)
    if pinned_blob == head_blob:
        return Finding(pin, Verdict.current, pinned_blob, head_blob)
    return Finding(pin, Verdict.stale, pinned_blob, head_blob)


def apply_fixes(markdown_text: str, findings: tuple[Finding, ...], head: str) -> str:
    stale = {
        (finding.pin.line, finding.pin.raw_url)
        for finding in findings
        if finding.verdict == Verdict.stale
    }
    if not stale:
        return markdown_text
    rewritten: list[str] = []
    for line_number, line in enumerate(markdown_text.splitlines(keepends=True), start=1):
        cursor = 0
        parts: list[str] = []
        for match in PIN_RE.finditer(line):
            if (line_number, match.group(0)) not in stale:
                continue
            if image_object_path(match.group(2)) is None:
                continue
            parts.append(line[cursor : match.start(1)])
            parts.append(head)
            cursor = match.end(1)
        parts.append(line[cursor:])
        rewritten.append("".join(parts))
    return "".join(rewritten)


def markdown_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                found.append(Path(dirpath) / name)
    return found


def collect(root: Path, store: GitBlobStore) -> tuple[str, tuple[Finding, ...]]:
    head = store.head()
    findings: list[Finding] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        for pin in find_pins(text, relative):
            findings.append(classify_pin(pin, store, head))
    findings.sort(key=lambda finding: (finding.pin.markdown_path, finding.pin.line, finding.pin.raw_url))
    return head, tuple(findings)


def write_fixes(root: Path, findings: tuple[Finding, ...], head: str) -> None:
    by_file: dict[str, list[Finding]] = {}
    for finding in findings:
        by_file.setdefault(finding.pin.markdown_path, []).append(finding)
    for relative, group in by_file.items():
        if not any(finding.verdict == Verdict.stale for finding in group):
            continue
        path = root / relative
        text = path.read_text(encoding="utf-8")
        updated = apply_fixes(text, tuple(group), head)
        if updated != text:
            path.write_bytes(updated.encode("utf-8"))


def format_report(findings: tuple[Finding, ...], show_all: bool) -> str:
    counts = {verdict: 0 for verdict in Verdict}
    lines: list[str] = []
    for finding in findings:
        counts[finding.verdict] += 1
        if show_all or finding.verdict != Verdict.current:
            pin = finding.pin
            lines.append(
                f"{finding.verdict.value}\t{pin.markdown_path}:{pin.line}\t{pin.commit}\t{pin.object_path}"
            )
    lines.append(
        "current={current} stale={stale} missing={missing} unknown_commit={unknown}".format(
            current=counts[Verdict.current],
            stale=counts[Verdict.stale],
            missing=counts[Verdict.missing],
            unknown=counts[Verdict.unknown_commit],
        )
    )
    return "\n".join(lines) + "\n"


def exit_code(findings: tuple[Finding, ...]) -> int:
    for finding in findings:
        if finding.verdict != Verdict.current:
            return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Compare commit-pinned sns-media-public image URLs with the file bytes at HEAD."
    )
    parser.add_argument("--root", default=".", help="repository root to scan")
    parser.add_argument("--fix", action="store_true", help="rewrite stale image pins to HEAD")
    parser.add_argument("--all", action="store_true", help="print current pins as well as problems")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code is None else int(code)
    root = Path(args.root).resolve()
    store = GitBlobStore(root)
    try:
        head, findings = collect(root, store)
        if args.fix:
            write_fixes(root, findings, head)
            _, findings = collect(root, store)
    except GitError as exc:
        print(f"git failed in {root}: {exc}", file=sys.stderr)
        return 2
    except UnicodeError as exc:
        print(f"markdown is not utf-8 under {root}: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(format_report(findings, args.all))
    return exit_code(findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
