---
name: pwsh
description: Use bundled PowerShell references to create, edit, review, debug, and explain PowerShell scripts executed with `pwsh`. Use when Codex needs authoritative local guidance for `.ps1` scripting, command or help syntax, pipeline behavior, or cross-platform PowerShell workflows that must run on both Windows and Linux, especially when PowerShell 7.5.4+ behavior matters.
---

# PowerShell Script Authoring Reference

## Overview

Use this skill to answer PowerShell scripting questions with the bundled local references in [`references/`](references/). Prefer cross-platform `pwsh` workflows and verify the installed runtime before depending on version-specific behavior.

## Workflow

1. Check the local runtime first.
- Prefer `python scripts/check_pwsh_version.py` from the skill directory.
- Fall back to `pwsh -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'` if needed.
- Require PowerShell `7.5.4` or newer before relying on this skill's baseline behavior.
- If `pwsh` is missing or older, say so explicitly and avoid claiming newer behavior is available.

2. Classify the request.
- Determine whether the task is script authoring, debugging, help lookup, module usage, pipeline behavior, file handling, or cross-platform portability.

3. Search before reading deeply.
- Start with [`references/source-map.md`](references/source-map.md).
- Use `python scripts/search_pwsh_refs.py` to find candidate references, pages, and line numbers quickly.
- Use [`references/PowerShell hints for multi-platform scripts.md`](references/PowerShell hints for multi-platform scripts.md) first for portability rules.
- Open only the specific PDF or text reference that matches the task.

4. Prefer cross-platform defaults.
- Use `pwsh`, not legacy `powershell`, in commands and shebangs.
- Prefer full cmdlet names instead of aliases in scripts.
- Prefer `Join-Path`, `[System.IO.Path]::GetTempPath()`, and forward-slash-safe path handling over hardcoded separators or root drives.
- Use `$IsWindows`, `$IsLinux`, and `$IsMacOS` for OS-specific branches.
- Avoid unguarded use of COM, WMI, registry providers, or Windows-only modules.
- Guard optional commands or modules with `Get-Command` or `Get-Module -ListAvailable` before using them.

5. Separate documentation from environment facts.
- Use the bundled references for documented syntax and behavior.
- Verify local availability with commands such as `Get-Command`, `Get-Help`, `Get-Module -ListAvailable`, and `$PSVersionTable` when the answer depends on the installed environment.
- Treat third-party modules as environment-dependent unless you confirm they are installed.

6. Return a cited answer.
- Provide the script, command, or conclusion first.
- Add concise citations in the format `[Document, p. X]` for PDFs or `[Document, line X]` for text references.
- State clearly when a recommendation is an inference or a portability best practice rather than an explicit normative rule from the source.

## Fast Lookup Scripts

Use the bundled scripts for deterministic checks and quick searches.

- Check the local baseline version:
`python scripts/check_pwsh_version.py`
- Check against a different minimum:
`python scripts/check_pwsh_version.py --min-version 7.6.0`
- Emit machine-readable version data:
`python scripts/check_pwsh_version.py --json`
- List document aliases:
`python scripts/search_pwsh_refs.py --list-docs`
- Search all references:
`python scripts/search_pwsh_refs.py "comment-based help" --max-hits 10`
- Search only the portability notes:
`python scripts/search_pwsh_refs.py "Join-Path" --doc multi-platform-hints`
- Search one PDF reference:
`python scripts/search_pwsh_refs.py "advanced function" --doc scripting-75 --max-hits 5`

Install `pypdf` once per environment to search the PDF references:
`pip install pypdf`

Markdown and text searches continue to work without `pypdf`.

## Source Priority

Use this priority when sources overlap:

1. `powershell-scripting-powershell-7.5.pdf` for PowerShell 7.5 scripting behavior and examples.
2. `The Help system - PowerShell.pdf` for `Get-Help`, help content, and help update behavior.
3. `PowerShell hints for multi-platform scripts.md` for concise portability rules that prevent Windows-only assumptions.
4. `PowerShellQuickReference-PowerShell7.0-v1.05-3.pdf` for fast syntax recall.
5. `powershell-module-psdocs-powershell-7.5.pdf` only when the user asks about PSDocs or generating documentation from PowerShell content.

## Reference Selection Guide

- Use `multi-platform-hints` for path handling, aliases, OS detection, shebangs, encoding, and line-ending guidance.
- Use `scripting-75` for core script structure, control flow, functions, pipelines, objects, error handling, and PowerShell 7.5 behavior.
- Use `help-system` when the request involves `Get-Help`, comment-based help, or updating help content.
- Use `quick-reference` when the question is mostly about syntax recall or a compact command pattern.
- Use `psdocs` only for PSDocs-specific authoring or documentation-generation workflows.

## Portability Guardrails

- Write scripts so they run under `pwsh` on both Windows and Linux unless the user explicitly requests an OS-specific script.
- Prefer PowerShell-native object pipelines over shell-specific text parsing when possible.
- Mention when a script depends on native tools whose flags differ by platform.
- Use LF line endings and UTF-8 without BOM when a script is meant to be executed directly on Linux.
- Add `#!/usr/bin/env pwsh` only when the script is intended to be invoked as an executable on Unix-like systems.

## Answer Style

- Prefer a ready-to-run script or function when the user asks how to do something.
- Explain placeholders such as paths, module names, and parameters.
- Keep portability caveats close to the exact command or line they affect.
- Verify locally before stating that a command, module, or feature is available on the current machine.
