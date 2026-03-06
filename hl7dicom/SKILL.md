---
name: hl7dicom
description: Verify and cite requirements from HL7 v2.3 and DICOM standards using bundled PDF references. Use when Codex must confirm HL7 v2.3 message structures, segments, and field definitions, or DICOM data dictionary values (tag, VR, VM), encoding rules, message exchange behavior, and network communication requirements against official standards text.
---

# HL7 DICOM Standards Verification

## Overview

Use this skill to answer standards questions with document-grounded citations from the bundled HL7 and DICOM PDFs in [`references/`](references/).

## Workflow

1. Classify the request:
- Route to HL7 v2.3, DICOM, or both.
- Identify whether the user needs definition lookup, structural rules, encoding requirements, or network/message behavior.

2. Select the minimum required source documents:
- Use [`references/source-map.md`](references/source-map.md) to pick the right PDF first.
- Read only the sections needed to answer the exact question.

3. Extract and verify evidence:
- Locate the exact table, clause, or section that supports the answer.
- Cross-check related constraints when needed (for example, PS3.6 dictionary values plus PS3.5 encoding semantics).
- Treat unsupported assumptions as unknown.

4. Return a standards-grounded response:
- Provide the direct answer first.
- Add concise citations with document name and section/page.
- State the standard edition when relevant (for example, DICOM 2026a parts 3.5/3.6/3.7 and DICOM 2026 part 3.8).

## Fast Lookup Script

Use [`scripts/search_standards.py`](scripts/search_standards.py) to quickly locate candidate pages before deeper reading.

- Linux/macOS launcher:
`bash scripts/search_standards.sh --list-docs`
- Windows launcher:
`pwsh -File scripts/search_standards.ps1 --list-docs`
- Direct Python (cross-platform):
`python scripts/search_standards.py --list-docs`
- Search all documents:
`python scripts/search_standards.py "Specific Character Set" --max-hits 10`
- Search one document:
`python scripts/search_standards.py "(0010,0010)" --doc ps3.6 --max-hits 10`
- Regex search:
`python scripts/search_standards.py "shall\\s+support" --doc ps3.8 --regex --max-hits 10`

## Cross-Platform Notes

- Keep paths relative to the skill root; avoid absolute Windows-only paths.
- Prefer `bash scripts/search_standards.sh ...` on Linux and `pwsh -File scripts/search_standards.ps1 ...` on Windows.
- Install dependency once per environment: `pip install pypdf`.

## Citation Rules

- Cite every normative claim.
- Use this citation pattern: `[Document Name, section or table, page if available]`.
- Distinguish requirement levels exactly as written (`shall`, `should`, `may`) and do not upgrade recommendation language into requirements.
- Flag ambiguity explicitly when the standards text is silent or conflicting.

## Boundaries

- Do not invent HL7 or DICOM constraints without textual support.
- Do not mix versions silently; call out version mismatches if they appear in the question.
- If a required PDF is missing or unreadable, state the gap and ask for the file before giving a definitive compliance answer.
