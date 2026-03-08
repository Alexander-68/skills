#!/usr/bin/env python3
"""Search bundled PowerShell references and print page- or line-numbered snippets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


DOC_MAP = {
    'multi-platform-hints': 'PowerShell hints for multi-platform scripts.md',
    'scripting-75': 'powershell-scripting-powershell-7.5.pdf',
    'help-system': 'The Help system - PowerShell.pdf',
    'quick-reference': 'PowerShellQuickReference-PowerShell7.0-v1.05-3.pdf',
    'psdocs': 'powershell-module-psdocs-powershell-7.5.pdf',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Search bundled PowerShell references and return numbered matches.',
    )
    parser.add_argument('query', nargs='?', help='Search text or regex pattern.')
    parser.add_argument(
        '--doc',
        choices=['all', *DOC_MAP.keys()],
        default='all',
        help='Document alias to search (default: all).',
    )
    parser.add_argument(
        '--regex',
        action='store_true',
        help='Interpret query as a regular expression.',
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Enable case-sensitive matching (default: case-insensitive).',
    )
    parser.add_argument(
        '--context',
        type=int,
        default=80,
        help='Characters to include before and after a PDF match (default: 80).',
    )
    parser.add_argument(
        '--line-context',
        type=int,
        default=0,
        help='Surrounding lines to include for text or Markdown matches (default: 0).',
    )
    parser.add_argument(
        '--max-hits',
        type=int,
        default=25,
        help='Maximum number of matches to print across all documents (default: 25).',
    )
    parser.add_argument(
        '--list-docs',
        action='store_true',
        help='List available document aliases and exit.',
    )
    return parser.parse_args()


def build_pattern(query: str, use_regex: bool, case_sensitive: bool) -> re.Pattern[str]:
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern_text = query if use_regex else re.escape(query)
    return re.compile(pattern_text, flags)


def normalize_snippet(text: str) -> str:
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def iter_doc_paths(selected_doc: str, references_dir: Path) -> Iterable[tuple[str, Path]]:
    aliases = DOC_MAP.keys() if selected_doc == 'all' else [selected_doc]
    for alias in aliases:
        yield alias, references_dir / DOC_MAP[alias]


def search_pdf(doc_path: Path, pattern: re.Pattern[str], context_chars: int) -> list[tuple[int, str]]:
    reader = PdfReader(str(doc_path))
    matches: list[tuple[int, str]] = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ''
        if not text:
            continue
        for match in pattern.finditer(text):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            matches.append((page_num, normalize_snippet(text[start:end])))
    return matches


def search_text(doc_path: Path, pattern: re.Pattern[str], line_context: int) -> list[tuple[int, str]]:
    lines = doc_path.read_text(encoding='utf-8', errors='replace').splitlines()
    matches: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if not pattern.search(line):
            continue
        start = max(0, index - line_context)
        end = min(len(lines), index + line_context + 1)
        snippet = ' | '.join(part.strip() for part in lines[start:end] if part.strip())
        matches.append((index + 1, normalize_snippet(snippet or line)))
    return matches


def main() -> int:
    args = parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    if args.list_docs:
        for alias, filename in DOC_MAP.items():
            print(f'{alias:22} -> {filename}')
        return 0

    if not args.query:
        print('error: query is required unless --list-docs is used', file=sys.stderr)
        return 2

    try:
        pattern = build_pattern(args.query, args.regex, args.case_sensitive)
    except re.error as exc:
        print(f'error: invalid regex pattern: {exc}', file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    references_dir = script_dir.parent / 'references'
    if not references_dir.exists():
        print(f'error: references directory not found: {references_dir}', file=sys.stderr)
        return 2

    printed = 0
    searched_any = False
    missing_docs: list[Path] = []
    skipped_pdfs: list[Path] = []

    for alias, doc_path in iter_doc_paths(args.doc, references_dir):
        if not doc_path.exists():
            missing_docs.append(doc_path)
            continue

        if doc_path.suffix.lower() == '.pdf':
            if PdfReader is None:
                skipped_pdfs.append(doc_path)
                continue
            searched_any = True
            doc_matches = search_pdf(doc_path, pattern, args.context)
            label_prefix = 'p.'
        else:
            searched_any = True
            doc_matches = search_text(doc_path, pattern, args.line_context)
            label_prefix = 'line '

        if not doc_matches:
            continue

        print(f'\n=== {alias}: {doc_path.name} ===')
        for location, snippet in doc_matches:
            print(f'[{label_prefix}{location}] {snippet}')
            printed += 1
            if printed >= args.max_hits:
                print(f'\nStopped after {args.max_hits} hits.')
                return 0

    for missing in missing_docs:
        print(f'warning: missing document: {missing}', file=sys.stderr)

    if skipped_pdfs:
        print(
            "warning: skipped PDF documents because 'pypdf' is not installed; install it with: pip install pypdf",
            file=sys.stderr,
        )

    if not searched_any:
        print('error: no searchable documents were available', file=sys.stderr)
        return 2

    if printed == 0:
        print('No matches found.')
        return 1

    print(f'\nTotal hits: {printed}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
