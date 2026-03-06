#!/usr/bin/env python3
"""Search bundled HL7/DICOM standards PDFs and print page-numbered snippets."""

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
    "hl7v23": "hl7 hl7v23 Implementation Support Guide HL7 version 2.3.pdf",
    "ps3.5": "DICOM PS3.5 2026a - Data Structures and Encoding.pdf",
    "ps3.6": "DICOM PS3.6 2026a - Data Dictionary.pdf",
    "ps3.7": "DICOM PS3.7 2026a - Message Exchange.pdf",
    "ps3.8": "DICOM PS3.8 2026 - Network Communication Support for Message Exchange.pdf",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search HL7/DICOM standards PDFs and return page-numbered matches."
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
        file_name = DOC_MAP[alias]
        yield alias, references_dir / file_name


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
            snippet = normalize_snippet(text[start:end])
            matches.append((page_num, snippet))
    return matches


def main() -> int:
    args = parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")

    if args.list_docs:
        for alias, filename in DOC_MAP.items():
            print(f"{alias:6} -> {filename}")
        return 0

    if not args.query:
        print("error: query is required unless --list-docs is used", file=sys.stderr)
        return 2

    if PdfReader is None:
        print("error: missing dependency 'pypdf'. Install with: pip install pypdf", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    references_dir = skill_root / "references"
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
