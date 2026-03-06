#!/usr/bin/env python3
"""Search bundled Go reference PDFs and print page-numbered snippets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - dependency guard
    PdfReader = None


DOC_MAP = {
    "spec": "Go Programming Language Specification.pdf",
    "memory-model": "Go Memory Model.pdf",
    "effective-go": "Effective Go Guide.pdf",
    "stdlib": "Standard library - Go Packages.pdf",
    "archive-tar": "tar package - archive_tar - Go Packages.pdf",
    "archive-zip": "zip package - archive_zip - Go Packages.pdf",
    "crypto": "crypto package - crypto - Go Packages.pdf",
    "crypto-cipher": "cipher package - crypto_cipher - Go Packages.pdf",
    "encoding-gob": "gob package - encoding_gob - Go Packages.pdf",
    "image": "image package - image - Go Packages.pdf",
    "image-color": "color package - image_color - Go Packages.pdf",
    "image-draw": "draw package - image_draw - Go Packages.pdf",
    "regexp": "regexp package - regexp - Go Packages.pdf",
    "regexp-syntax": "syntax package - regexp_syntax - Go Packages.pdf",
    "sort": "sort package - sort - Go Packages.pdf",
    "gc-guide": "A Guide to the Go Garbage Collector.pdf",
    "fuzzing": "Go Fuzzing - The Go Programming Language.pdf",
    "fuzzing-tutorial": "Tutorial_ Getting started with fuzzing.pdf",
    "coverage": "Coverage profiling support for integration tests.pdf",
    "pgo": "Profile-guided optimization.pdf",
    "deps": "Managing dependencies.pdf",
    "json-and-go": "JSON and Go - The Go Programming Language.pdf",
    "web-apps": "Writing Web Applications.pdf",
    "gin-tutorial": "Tutorial_ Developing a RESTful API with Go and Gin.pdf",
    "go-image-article": "The Go image package.pdf",
    "go-image-draw-article": "The Go image_draw package.pdf",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search Go reference PDFs and return page-numbered matches."
    )
    parser.add_argument("query", nargs="?", help="Search text or regex pattern.")
    parser.add_argument(
        "--doc",
        choices=["all", *DOC_MAP.keys()],
        default="all",
        help="Document alias to search (default: all).",
    )
    parser.add_argument(
        "--regex",
        action="store_true",
        help="Interpret query as a regular expression.",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Enable case-sensitive matching (default: case-insensitive).",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=80,
        help="Characters to include before and after each match (default: 80).",
    )
    parser.add_argument(
        "--max-hits",
        type=int,
        default=25,
        help="Maximum number of matches to print across all documents (default: 25).",
    )
    parser.add_argument(
        "--list-docs",
        action="store_true",
        help="List available document aliases and exit.",
    )
    return parser.parse_args()


def build_pattern(query: str, use_regex: bool, case_sensitive: bool) -> re.Pattern[str]:
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern_text = query if use_regex else re.escape(query)
    return re.compile(pattern_text, flags)


def normalize_snippet(text: str) -> str:
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def iter_doc_paths(selected_doc: str, references_dir: Path) -> Iterable[tuple[str, Path]]:
    aliases = DOC_MAP.keys() if selected_doc == "all" else [selected_doc]
    for alias in aliases:
        yield alias, references_dir / DOC_MAP[alias]


def search_pdf(doc_path: Path, pattern: re.Pattern[str], context_chars: int) -> list[tuple[int, str]]:
    reader = PdfReader(str(doc_path))
    matches: list[tuple[int, str]] = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text:
            continue
        for match in pattern.finditer(text):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            matches.append((page_num, normalize_snippet(text[start:end])))
    return matches


def main() -> int:
    args = parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")

    if args.list_docs:
        for alias, filename in DOC_MAP.items():
            print(f"{alias:21} -> {filename}")
        return 0

    if not args.query:
        print("error: query is required unless --list-docs is used", file=sys.stderr)
        return 2

    if PdfReader is None:
        print("error: missing dependency 'pypdf'. Install with: pip install pypdf", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    references_dir = script_dir.parent / "references"
    if not references_dir.exists():
        print(f"error: references directory not found: {references_dir}", file=sys.stderr)
        return 2

    try:
        pattern = build_pattern(args.query, args.regex, args.case_sensitive)
    except re.error as exc:
        print(f"error: invalid regex pattern: {exc}", file=sys.stderr)
        return 2

    printed = 0
    missing_docs: list[Path] = []
    for alias, doc_path in iter_doc_paths(args.doc, references_dir):
        if not doc_path.exists():
            missing_docs.append(doc_path)
            continue

        doc_matches = search_pdf(doc_path, pattern, args.context)
        if not doc_matches:
            continue

        print(f"\n=== {alias}: {doc_path.name} ===")
        for page_num, snippet in doc_matches:
            print(f"[p.{page_num}] {snippet}")
            printed += 1
            if printed >= args.max_hits:
                print(f"\nStopped after {args.max_hits} hits.")
                return 0

    for missing in missing_docs:
        print(f"warning: missing document: {missing}", file=sys.stderr)

    if printed == 0:
        print("No matches found.")
        return 1

    print(f"\nTotal hits: {printed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
