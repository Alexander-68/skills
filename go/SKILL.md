---
name: go
description: Verify and cite Go language rules and standard library behavior using bundled Go specification and package documentation PDFs. Use when Codex needs authoritative references for Go syntax, semantics, memory model behavior, testing/profiling guidance, or details about standard library packages covered by this skill.
---

# Go Specification and Stdlib Reference

## Overview

Use this skill to answer Go questions with document-grounded citations from bundled PDFs in [`references/`](references/). Treat `Go Programming Language Specification.pdf` as the canonical spec snapshot shipped with this skill.

## Workflow

1. Classify the request.
- Determine whether it is language specification, memory model, general guidance, tooling guidance, or package API behavior.

2. Select the minimum source set.
- Use [`references/source-map.md`](references/source-map.md) first.
- Prefer the most normative source available for the question.

3. Extract and verify evidence.
- Locate the exact section heading or page that supports the claim.
- For behavioral questions, cross-check at least one normative source plus one package-specific source when both are available.

4. Return a cited answer.
- Provide the answer first.
- Add concise citations in the format `[Document, section/page]`.
- If the bundled references do not cover the package/version asked for, state that gap explicitly.

## Fast Lookup Script

Use [`scripts/search_go_refs.py`](scripts/search_go_refs.py) to find candidate pages quickly before deeper reading.

- Linux/macOS launcher:
`bash scripts/search_go_refs.sh --list-docs`
- Windows launcher:
`pwsh -File scripts/search_go_refs.ps1 --list-docs`
- Direct Python (cross-platform):
`python scripts/search_go_refs.py --list-docs`
- Search all documents:
`python scripts/search_go_refs.py "type parameter" --max-hits 10`
- Search a specific document alias:
`python scripts/search_go_refs.py "happens-before" --doc memory-model --max-hits 10`
- Regex search:
`python scripts/search_go_refs.py "func\\s+\\(.*\\)\\s+~" --doc spec --regex --max-hits 10`

## Source Priority

Use this priority when sources overlap:

1. `Go Programming Language Specification.pdf` for syntax and language semantics.
2. `Go Memory Model.pdf` for memory ordering and concurrent visibility guarantees.
3. Package documentation PDFs for package contracts and APIs.
4. `Effective Go Guide.pdf` and tutorial articles for idioms and practical examples.

## Citation and Version Rules

- Cite every non-trivial technical claim.
- Do not present tutorial guidance as a language requirement when the specification says otherwise.
- If the user asks about a newer Go release than what is represented in bundled docs, state that the answer is based on the bundled snapshot and call out possible version drift.
- When references conflict or are ambiguous, report the ambiguity and avoid definitive claims.

## Cross-Platform Notes

- Keep paths relative to the skill root.
- Use `bash scripts/search_go_refs.sh ...` on Linux/macOS and `pwsh -File scripts/search_go_refs.ps1 ...` on Windows.
- Install dependency once per environment: `pip install pypdf`.
