#!/usr/bin/env python3
"""Observable behavior of the figure check command."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "figure_check.py"


def write_tree(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if path.suffix.lower() in {".png", ".jpg", ".gif", ".webp"}:
            path.write_bytes(b"")


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


class FigureCheckTests(unittest.TestCase):
    def test_matching_meta_alt_filename_and_number_exits_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "# note\n\n"
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                    "note/article.md": (
                        "Body\n\n"
                        "![Ads are absent now](figures/fig01.png)\n"
                    ),
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "0 mismatches\n")
        self.assertEqual(result.stderr, "")

    def test_article_alt_must_match_meta_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                    "note/article.md": "![Ads are guaranteed forever](figures/fig01.png)\n",
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("1 mismatch\n", result.stdout)
        self.assertIn("description\tnote/article.md:1\tfig01.png", result.stdout)
        self.assertIn("article: Ads are guaranteed forever", result.stdout)
        self.assertIn("catalog note/meta.md:3: Ads are absent now", result.stdout)

    def test_catalog_id_must_match_filename_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig02 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("number\tnote/meta.md:3\tfig01.png", result.stdout)
        self.assertIn("stated figure 2, filename fig01.png is figure 1", result.stdout)

    def test_alt_figure_number_must_match_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Figure 2: Ads are absent now |\n"
                    ),
                    "note/article.md": "![Figure 2: Ads are absent now](figures/fig01.png)\n",
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("number\tnote/article.md:1\tfig01.png", result.stdout)
        self.assertIn("number\tnote/meta.md:3\tfig01.png", result.stdout)
        self.assertNotIn("description", result.stdout)

    def test_listed_file_must_exist_in_the_figures_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("filename\tnote/meta.md:3\tfig01.png", result.stdout)
        self.assertIn("missing from the figures directory", result.stdout)

    def test_article_image_missing_from_the_catalog_is_a_filename_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                    "note/article.md": "![Figure 9: Something else](figures/fig02.png)\n",
                    "note/figures/fig01.png": "",
                    "note/figures/fig02.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("filename\tnote/article.md:1\tfig02.png", result.stdout)
        self.assertIn("not listed in index.md or meta.md", result.stdout)
        self.assertIn("number\tnote/article.md:1\tfig02.png", result.stdout)
        self.assertIn("stated figure 9, filename fig02.png is figure 2", result.stdout)

    def test_caption_or_alt_column_can_match_the_article(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "en/figures/index.md": (
                        "| File | Caption | Alt text |\n"
                        "|---|---|---|\n"
                        "| [fig1.png](fig1.png) | Figure 1: Scope | A long description of scope |\n"
                    ),
                    "en/article.md": "![Figure 1: Scope](figures/fig1.png)\n",
                    "en/substack.md": "![A long description of scope](figures/fig1.png)\n",
                    "en/figures/fig1.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "0 mismatches\n")

    def test_quote_style_alone_is_not_a_description_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Called \u201contology\u201d |\n"
                    ),
                    "note/article.md": '![Called "ontology"](figures/fig01.png)\n',
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_image_outside_the_figures_directory_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "en/figures/index.md": (
                        "| File | Caption | Alt text |\n"
                        "|---|---|---|\n"
                        "| [fig1.png](fig1.png) | Figure 1: Scope | Figure 1: Scope |\n"
                    ),
                    "en/article.md": (
                        "![Figure 1: Scope](figures/fig1.png)\n"
                        "![Table: standards](images/table_01.png)\n"
                    ),
                    "en/figures/fig1.png": "",
                    "en/images/table_01.png": "",
                    "en/other/fig1.png": "",
                    "en/other.md": "![A different picture](other/fig1.png)\n",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unlisted_companion_file_is_not_a_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig09 | `note/figures/fig09.gif` | Sentinel reviews traffic |\n"
                    ),
                    "note/article.md": "![Sentinel reviews traffic](figures/fig09.gif)\n",
                    "note/figures/fig09.gif": "",
                    "note/figures/fig09.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fenced_example_is_not_an_article_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "note/meta.md": (
                        "| # | file | alt text |\n"
                        "|---|---|---|\n"
                        "| fig01 | `note/figures/fig01.png` | Ads are absent now |\n"
                    ),
                    "note/article.md": (
                        "![Ads are absent now](figures/fig01.png)\n"
                        "```\n"
                        "![Wrong words](figures/fig01.png)\n"
                        "```\n"
                    ),
                    "note/figures/fig01.png": "",
                },
            )
            result = run_check(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_root_exits_with_usage_status(self) -> None:
        result = run_check(Path(tempfile.gettempdir()) / "figure-check-missing-root")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a directory", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
