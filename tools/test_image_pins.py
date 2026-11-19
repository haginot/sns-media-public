"""Behavior tests for the commit-pinned image URL checker.

Each test builds a temporary git repository and drives the public functions
or the CLI. Expected bytes come from the scenario, not from the checker.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import image_pins

TOOL = Path(image_pins.__file__)


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def init_repo(path: Path) -> None:
    run_git(path, "init", "-b", "main")
    run_git(path, "config", "user.name", "Pin Test")
    run_git(path, "config", "user.email", "pin-test@example.com")
    run_git(path, "config", "commit.gpgsign", "false")


def write(repo: Path, rel: str, content: bytes) -> None:
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def commit(repo: Path, rel: str, content: bytes, message: str) -> str:
    write(repo, rel, content)
    run_git(repo, "add", "--", rel)
    run_git(repo, "commit", "-m", message)
    return run_git(repo, "rev-parse", "HEAD")


def pin_url(commit_id: str, object_path: str) -> str:
    return (
        "https://raw.githubusercontent.com/haginot/sns-media-public/"
        f"{commit_id}/{object_path}"
    )


def cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(repo), *args],
        capture_output=True,
        text=True,
    )


class ImagePinTests(unittest.TestCase):
    def test_current_pin_is_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            markdown = f"![a]({pin_url(image_commit, 'figs/a.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin the figure")
            findings = self.scan(repo)
            self.assertEqual(
                [finding.verdict for finding in findings],
                [image_pins.Verdict.current],
            )
            before = (repo / "note.md").read_bytes()
            result = cli(repo, "--fix")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((repo / "note.md").read_bytes(), before)
            self.assertIn("current=1 stale=0 missing=0 unknown_commit=0", result.stdout)

    def test_stale_pin_rewrites_only_the_url(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            prose = f"Shipped from {image_commit}."
            markdown = f"{prose}\n![a]({pin_url(image_commit, 'figs/a.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin the figure")
            commit(repo, "figs/a.png", b"version-two", "redraw figure")
            head = run_git(repo, "rev-parse", "HEAD")
            findings = self.scan(repo)
            self.assertEqual(findings[0].verdict, image_pins.Verdict.stale)
            self.assertNotEqual(findings[0].pinned_blob, findings[0].head_blob)
            check = cli(repo)
            self.assertEqual(check.returncode, 1, check.stdout)
            self.assertIn("stale\tnote.md:2\t", check.stdout)
            self.assertIn("current=0 stale=1 missing=0 unknown_commit=0", check.stdout)
            fixed = cli(repo, "--fix")
            self.assertEqual(fixed.returncode, 0, fixed.stderr)
            text = (repo / "note.md").read_text(encoding="utf-8")
            self.assertIn(prose, text)
            self.assertIn(pin_url(head, "figs/a.png"), text)
            self.assertNotIn(pin_url(image_commit, "figs/a.png"), text)
            again = (repo / "note.md").read_bytes()
            second = cli(repo, "--fix")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual((repo / "note.md").read_bytes(), again)

    def test_bytes_restored_after_redraw_stay_current(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            markdown = f"![a]({pin_url(image_commit, 'figs/a.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin the figure")
            commit(repo, "figs/a.png", b"version-two", "redraw figure")
            commit(repo, "figs/a.png", b"version-one", "restore figure")
            before = (repo / "note.md").read_bytes()
            findings = self.scan(repo)
            self.assertEqual(findings[0].verdict, image_pins.Verdict.current)
            self.assertEqual(findings[0].pinned_blob, findings[0].head_blob)
            result = cli(repo, "--fix")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((repo / "note.md").read_bytes(), before)

    def test_unknown_commit_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            missing = "0123456789abcdef0123456789abcdef01234567"
            markdown = f"![a]({pin_url(missing, 'figs/a.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin a missing commit")
            before = (repo / "note.md").read_bytes()
            findings = self.scan(repo)
            self.assertEqual(findings[0].verdict, image_pins.Verdict.unknown_commit)
            result = cli(repo, "--fix")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("unknown_commit\tnote.md:1\t", result.stdout)
            self.assertEqual((repo / "note.md").read_bytes(), before)

    def test_missing_path_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            markdown = f"![a]({pin_url(image_commit, 'figs/a.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin the figure")
            run_git(repo, "rm", "figs/a.png")
            run_git(repo, "commit", "-m", "remove figure")
            before = (repo / "note.md").read_bytes()
            findings = self.scan(repo)
            self.assertEqual(findings[0].verdict, image_pins.Verdict.missing)
            result = cli(repo, "--fix")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("missing\tnote.md:1\t", result.stdout)
            self.assertEqual((repo / "note.md").read_bytes(), before)

    def test_non_image_urls_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            markdown = "\n".join(
                [
                    pin_url(image_commit, "2026-11-19/muse-en/"),
                    pin_url(image_commit, "notes/readme.txt"),
                    f"![a]({pin_url(image_commit, 'figs/a.png')})",
                    "",
                ]
            )
            commit(repo, "note.md", markdown.encode(), "mixed urls")
            pins = image_pins.find_pins(
                (repo / "note.md").read_text(encoding="utf-8"),
                "note.md",
            )
            self.assertEqual([pin.object_path for pin in pins], ["figs/a.png"])
            result = cli(repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("current=1 stale=0 missing=0 unknown_commit=0", result.stdout)
            self.assertNotIn("muse-en", result.stdout)
            self.assertNotIn("readme.txt", result.stdout)

    def test_cursor_directory_is_not_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/a.png", b"version-one", "add figure")
            current = f"![a]({pin_url(image_commit, 'figs/a.png')})\n"
            commit(repo, "note.md", current.encode(), "pin the figure")
            commit(repo, "figs/a.png", b"version-two", "redraw figure")
            hidden = repo / ".cursor" / "vendor.md"
            hidden.parent.mkdir()
            hidden.write_text(
                f"![hidden]({pin_url(image_commit, 'figs/a.png')})\n",
                encoding="utf-8",
            )
            note = (repo / "note.md").read_bytes()
            result = cli(repo, "--fix")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(".cursor", result.stdout)
            self.assertEqual(hidden.read_text(encoding="utf-8"), f"![hidden]({pin_url(image_commit, 'figs/a.png')})\n")
            self.assertNotEqual((repo / "note.md").read_bytes(), note)

    def test_bad_arguments_exit_2(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL), "--nope"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)

    def test_encoded_path_uses_the_unquoted_git_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            image_commit = commit(repo, "figs/my figure.png", b"version-one", "add figure")
            markdown = f"![a]({pin_url(image_commit, 'figs/my%20figure.png')})\n"
            commit(repo, "note.md", markdown.encode(), "pin the figure")
            pins = image_pins.find_pins(
                (repo / "note.md").read_text(encoding="utf-8"),
                "note.md",
            )
            self.assertEqual(pins[0].object_path, "figs/my figure.png")
            self.assertEqual(pins[0].raw_url, pin_url(image_commit, "figs/my%20figure.png"))
            findings = self.scan(repo)
            self.assertEqual(findings[0].verdict, image_pins.Verdict.current)

    def scan(self, repo: Path) -> tuple[image_pins.Finding, ...]:
        store = image_pins.GitBlobStore(repo)
        head = store.head()
        text = (repo / "note.md").read_text(encoding="utf-8")
        return tuple(
            image_pins.classify_pin(pin, store, head)
            for pin in image_pins.find_pins(text, "note.md")
        )


if __name__ == "__main__":
    unittest.main()
