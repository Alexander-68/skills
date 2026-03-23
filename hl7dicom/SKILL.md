---
name: hl7dicom
description: Verify and cite requirements from HL7 and DICOM references bundled with this skill. Use when Codex must confirm HL7 v2 message structures, segments, fields, trigger-event message layouts, or DICOM data dictionary values (tag, VR, VM), encoding rules, message exchange behavior, and network communication requirements against local standards artifacts. Prefer the bundled HL7 v2.7 XSD schemas for OMG_O19 and SIU_S12 message structure checks, keep legacy ORM^O01 support grounded in the bundled HL7 v2.3 implementation guide, and call out version mismatches explicitly.
---

# HL7 DICOM Standards Verification

## Overview

Use this skill to answer standards questions with citations grounded in the bundled HL7 and DICOM artifacts in [`references/`](references/).

## Workflow

1. Classify the request:
- Route to HL7, DICOM, or both.
- Identify whether the user needs segment or field definitions, message structure, trigger-event compatibility, encoding requirements, or network/message behavior.
- Distinguish schema-shape questions from normative requirements before selecting sources.

2. Select the minimum required source documents:
- Use [`references/source-map.md`](references/source-map.md) to pick the right PDF first.
- For HL7 v2.7 message layout questions, inspect the relevant XSD directly with `rg` or a text reader before loading broader references.
- Read only the sections needed to answer the exact question.

3. Extract and verify evidence:
- Locate the exact table, clause, or section that supports the answer.
- For schema artifacts, locate the exact `xsd:element` or `xsd:complexType` sequence that supports the structural claim.
- Cross-check related constraints when needed (for example, PS3.6 dictionary values plus PS3.5 encoding semantics).
- Treat the XSDs as message-shape evidence, not a substitute for missing HL7 v2.7 normative prose.
- Treat unsupported assumptions as unknown.

4. Return a standards-grounded response:
- Provide the direct answer first.
- Add concise citations with document name and section/page.
- State the artifact and version boundary when relevant:
  - HL7 v2.7 XSD for `OMG_O19` or `SIU_S12` structure.
  - HL7 v2.3 implementation guide for legacy `ORM^O01` or shared segment/field semantics.
  - DICOM 2026a parts 3.5/3.6/3.7 and DICOM 2026 part 3.8.

## Fast Lookup Script

Use [`scripts/search_standards.py`](scripts/search_standards.py) to quickly locate candidate pages in the bundled PDFs before deeper reading.

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
- Search HL7 XSD schemas directly:
`rg -n "OMG_O19|ORC|OBR|SPM" references/OMG_O19.xsd`
`rg -n "SIU_S12|SCH|RGS|AIS|AIP" references/SIU_S12.xsd`

## Cross-Platform Notes

- Keep paths relative to the skill root; avoid absolute Windows-only paths.
- Prefer `bash scripts/search_standards.sh ...` on Linux and `pwsh -File scripts/search_standards.ps1 ...` on Windows.
- Install dependency once per environment: `pip install pypdf`.

## Citation Rules

- Cite every normative claim.
- Use this citation pattern: `[Document Name, section or table, page if available]`.
- For schema-based structural claims, use: `[File Name, element or complexType name]`.
- Distinguish requirement levels exactly as written (`shall`, `should`, `may`) and do not upgrade recommendation language into requirements.
- Label schema-only conclusions as structural or schema-based when no normative HL7 prose is available in the bundle.
- Flag ambiguity explicitly when the standards text is silent or conflicting.

## Boundaries

- Do not invent HL7 or DICOM constraints without textual support.
- Do not mix HL7 versions silently:
  - Prefer `OMG_O19.xsd` for the main HL7 v2.7 order-message structure target.
  - Keep `SIU_S12.xsd` available for scheduling-message structure checks.
  - Treat `ORM^O01` as a legacy inbound path and ground it in the bundled HL7 v2.3 guide unless a newer normative source is added.
- If a question asks for HL7 v2.7 semantics beyond what the XSD expresses, state that the bundle has schema evidence but not the corresponding v2.7 normative chapter text.
- If a required PDF is missing or unreadable, state the gap and ask for the file before giving a definitive compliance answer.
