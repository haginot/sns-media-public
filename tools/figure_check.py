#!/usr/bin/env python3
"""Compare figure number, filename, and description across an article folder."""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SKIP_DIRS = {".git", ".cursor", "node_modules"}
FIG_NAME = re.compile(r"(?i)^(?:fig|f)(\d+)\.(?:png|jpe?g|gif|webp)$")
STATED_NUMBER = re.compile(r"(?i)^(?:figure|図)\s*0*(\d+)\b")
ID_NUMBER = re.compile(r"(?i)^(?:fig|f)?0*(\d+)$")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
GITHUB_PATH = re.compile(
    r"https?://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/(.+)$"
)
CATALOG_NAMES = {"index.md", "meta.md"}


@dataclass(frozen=True, order=True)
class Mismatch:
    source: str
    line: int
    kind: str
    filename: str
    detail: str


@dataclass(frozen=True)
class CatalogRow:
    source: str
    line: int
    filename: str
    number: int | None
    stated_number: int | None
    descriptions: tuple[str, ...]
    full: Path


def norm(text: str) -> str:
    text = (
        text.replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u00a0", " ")
    )
    return re.sub(r"\s+", " ", text).strip()


def number_from_name(filename: str) -> int | None:
    match = FIG_NAME.match(filename)
    if match is None:
        return None
    return int(match.group(1))


def stated_number(text: str) -> int | None:
    match = STATED_NUMBER.match(text.strip())
    if match is None:
        return None
    return int(match.group(1))


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(cell == "" or set(cell) <= {"-", ":"} for cell in cells)


def is_figure_header(cells: list[str]) -> bool:
    lowered = [cell.lower() for cell in cells]
    has_file = "file" in lowered or "filename" in lowered
    has_text = any(
        cell in {"caption", "alt", "alt text"} or cell.startswith("alt ")
        for cell in lowered
    )
    return has_file and has_text


def cell_path(cell: str) -> str:
    match = re.search(r"\(([^)]+)\)", cell)
    if match is not None:
        return match.group(1).strip()
    return cell.strip("`").strip()


def unique_texts(texts: list[str]) -> tuple[str, ...]:
    kept: list[str] = []
    seen: set[str] = set()
    for text in texts:
        key = norm(text)
        if key in seen:
            continue
        seen.add(key)
        kept.append(text)
    return tuple(kept)


def iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def ancestor_distance(path: Path) -> int:
    distance = 0
    current = path
    while not current.exists():
        if current.parent == current:
            return 10**6
        current = current.parent
        distance += 1
    return distance


def resolve_catalog_file(raw: str, catalog: Path, root: Path) -> Path | None:
    raw = raw.split("?", 1)[0].split("#", 1)[0]
    if "/" not in raw and "\\" not in raw:
        candidate = (catalog.parent / raw).resolve()
        if under_root(candidate, root):
            return candidate
        return None
    candidates = [
        catalog.parent / raw,
        catalog.parent.parent / raw,
        catalog.parent.parent.parent / raw,
        root / raw,
    ]
    ranked = [item.resolve() for item in candidates if under_root(item, root)]
    if not ranked:
        return None
    return min(ranked, key=ancestor_distance)


def parse_catalog(path: Path, root: Path) -> list[CatalogRow]:
    rows: list[CatalogRow] = []
    header: list[str] | None = None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            header = None
            continue
        cells = split_row(line)
        if header is None:
            if is_figure_header(cells):
                header = [cell.lower() for cell in cells]
            continue
        if is_separator(cells) or len(cells) < len(header):
            continue
        record = dict(zip(header, cells))
        raw = cell_path(record.get("file") or record.get("filename") or "")
        if raw == "":
            continue
        filename = Path(raw.split("?", 1)[0]).name
        number = number_from_name(filename)
        if number is None:
            continue
        descriptions = [
            record[key]
            for key in ("caption", "alt text", "alt")
            if record.get(key)
        ]
        id_match = ID_NUMBER.match((record.get("#") or record.get("id") or "").strip("`"))
        full = resolve_catalog_file(raw, path, root)
        if full is None:
            continue
        rows.append(
            CatalogRow(
                source=rel(path, root),
                line=lineno,
                filename=filename,
                number=number,
                stated_number=int(id_match.group(1)) if id_match else None,
                descriptions=unique_texts(descriptions),
                full=full,
            )
        )
    return rows


def resolve_article_url(url: str, article: Path, root: Path) -> Path | None:
    url = url.strip()
    match = GITHUB_PATH.match(url)
    if match is not None:
        return (root / match.group(1)).resolve()
    if url.startswith("http://") or url.startswith("https://"):
        return None
    url = url.split("?", 1)[0].split("#", 1)[0]
    return (article.parent / url).resolve()


def iter_images(text: str):
    fenced = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for alt, url in IMAGE.findall(line):
            yield lineno, alt, url


def number_mismatch(source: str, line: int, filename: str, stated: int, number: int) -> Mismatch:
    return Mismatch(
        source=source,
        line=line,
        kind="number",
        filename=filename,
        detail=f"stated figure {stated}, filename {filename} is figure {number}",
    )


def description_mismatch(source: str, line: int, filename: str, alt: str, catalog_lines: tuple[str, ...]) -> Mismatch:
    lines = [
        "article alt does not match the catalog description",
        f"article: {alt}",
        *catalog_lines,
    ]
    return Mismatch(
        source=source,
        line=line,
        kind="description",
        filename=filename,
        detail="\n".join(lines),
    )


def check_catalog_row(row: CatalogRow) -> list[Mismatch]:
    found: list[Mismatch] = []
    if row.stated_number is not None and row.stated_number != row.number:
        found.append(
            number_mismatch(row.source, row.line, row.filename, row.stated_number, row.number)
        )
    for text in row.descriptions:
        stated = stated_number(text)
        if stated is not None and stated != row.number:
            found.append(number_mismatch(row.source, row.line, row.filename, stated, row.number))
    if not row.full.is_file():
        found.append(
            Mismatch(
                source=row.source,
                line=row.line,
                kind="filename",
                filename=row.filename,
                detail=f"{row.filename} is listed in the catalog but missing from the figures directory",
            )
        )
    return found


def bundle_root(figures_dir: Path) -> Path:
    if figures_dir.name in {"figures", "figs"}:
        return figures_dir.parent
    return figures_dir


def check_articles(root: Path, figures_dir: Path, rows: list[CatalogRow]) -> list[Mismatch]:
    by_name: dict[str, list[CatalogRow]] = {}
    for row in rows:
        by_name.setdefault(row.filename, []).append(row)
    found: list[Mismatch] = []
    bundle = bundle_root(figures_dir)
    for article in iter_markdown(bundle):
        if article.name in CATALOG_NAMES:
            continue
        text = article.read_text(encoding="utf-8")
        for lineno, alt, url in iter_images(text):
            full = resolve_article_url(url, article, root)
            if full is None or not under_root(full, root):
                continue
            try:
                full.relative_to(figures_dir)
            except ValueError:
                continue
            filename = full.name
            source = rel(article, root)
            catalog = by_name.get(filename)
            if catalog is None:
                found.append(
                    Mismatch(
                        source=source,
                        line=lineno,
                        kind="filename",
                        filename=filename,
                        detail=f"{filename} is used in the article but not listed in index.md or meta.md",
                    )
                )
                stated = stated_number(alt)
                number = number_from_name(filename)
                if stated is not None and number is not None and stated != number:
                    found.append(number_mismatch(source, lineno, filename, stated, number))
                continue
            catalog_lines: list[str] = []
            seen: set[str] = set()
            for row in catalog:
                for text in row.descriptions:
                    key = norm(text)
                    if key in seen:
                        continue
                    seen.add(key)
                    catalog_lines.append(f"catalog {row.source}:{row.line}: {text}")
            if catalog_lines and norm(alt) not in seen:
                found.append(
                    description_mismatch(source, lineno, filename, alt, tuple(catalog_lines))
                )
            stated = stated_number(alt)
            number = number_from_name(filename)
            if stated is not None and number is not None and stated != number:
                found.append(number_mismatch(source, lineno, filename, stated, number))
    return found


def check(root: Path) -> list[Mismatch]:
    root = root.resolve()
    grouped: dict[Path, list[CatalogRow]] = {}
    found: list[Mismatch] = []
    for path in iter_markdown(root):
        if path.name not in CATALOG_NAMES:
            continue
        for row in parse_catalog(path, root):
            grouped.setdefault(row.full.parent, []).append(row)
            found.extend(check_catalog_row(row))
    for figures_dir, rows in grouped.items():
        found.extend(check_articles(root, figures_dir, rows))
    return sorted(set(found))


def render(found: list[Mismatch]) -> str:
    noun = "mismatch" if len(found) == 1 else "mismatches"
    lines = [f"{len(found)} {noun}"]
    for item in found:
        lines.append(f"{item.kind}\t{item.source}:{item.line}\t{item.filename}")
        for detail in item.detail.splitlines():
            lines.append(f"  {detail}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Report figure number, filename, and description disagreements "
            "between article images, index.md, meta.md, and the figures directory."
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to scan. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    found = check(root)
    sys.stdout.write(render(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
