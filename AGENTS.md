# AGENTS.md instructions for C:\Alex\skills

## Purpose
This repository contains custom Codex skills. Each skill lives in its own folder with a `SKILL.md`, optional `scripts/`, optional `references/`, and agent metadata in `agents/`.

## Available skills
- `ffmpeg`: Verify FFmpeg and FFprobe command-line behavior, codecs, filters, protocols, capture workflows, streaming workflows, troubleshooting steps, and hardware acceleration guidance using bundled reference PDFs. (file: `ffmpeg/SKILL.md`)
- `go`: Verify and cite Go language rules and standard library behavior using bundled Go specification and package documentation PDFs. (file: `go/SKILL.md`)
- `hl7dicom`: Verify and cite HL7 v2.3 and DICOM requirements using bundled standards PDFs. (file: `hl7dicom/SKILL.md`)

## Trigger rules
- If the user explicitly names a skill (for example `$ffmpeg`, `ffmpeg`, `$go`, `go`, `$hl7dicom`, `hl7dicom`), use that skill in the current turn.
- If the request clearly matches a skill description, use that skill even if not explicitly named.
- Do not carry a skill across turns unless it is named again or clearly required by the new request.

## Skill usage workflow
1. Open the selected skill's `SKILL.md` and follow its workflow.
2. Resolve relative paths from the skill directory first.
3. Load only the minimum references needed for the user request.
4. Prefer bundled scripts in `scripts/` for search/lookup instead of ad-hoc reimplementation.
5. Cite claims using the citation pattern defined in the active `SKILL.md`.

## Multi-skill coordination
- If multiple skills are relevant, use the minimum combination and state the order.
- Avoid mixing standards or versions silently; call out version boundaries and uncertainty.

## Repository conventions
- Keep paths relative and cross-platform where possible.
- When adding references, update the skill’s `references/source-map.md`.
- Update this `AGENTS.md` whenever a skill is added, removed, renamed, moved, or its trigger description changes.
- Keep the `Available skills` list, trigger examples, and any workflow or coordination notes synchronized with the actual skill set in the repository.
- Keep changes scoped to the target skill unless shared tooling must be updated.

## Fallback behavior
- If a named skill file is missing or unreadable, state the issue briefly and continue with the best available method.
