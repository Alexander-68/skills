# PowerShell Reference Map

Use this file first to choose the smallest useful source set.

## Core references

- `scripting-75` -> `powershell-scripting-powershell-7.5.pdf`: Primary reference for PowerShell 7.5 scripting behavior, language features, pipelines, functions, objects, and script structure.
- `help-system` -> `The Help system - PowerShell.pdf`: Reference for `Get-Help`, comment-based help, online help, and help update behavior.

## Fast-start reference

- `multi-platform-hints` -> `PowerShell hints for multi-platform scripts.md`: Quick checklist for Windows and Linux portability, including paths, aliases, OS detection, shebang usage, line endings, and encoding.

## Supplemental references

- `quick-reference` -> `PowerShellQuickReference-PowerShell7.0-v1.05-3.pdf`: Compact syntax and command recall sheet for common PowerShell patterns.
- `psdocs` -> `powershell-module-psdocs-powershell-7.5.pdf`: PSDocs module reference for documentation-generation workflows.

## Suggested starting points

- Use `multi-platform-hints` first when the script must run on both Windows and Linux.
- Use `scripting-75` for most script-authoring, function, pipeline, and error-handling questions.
- Use `help-system` for `Get-Help`, comment-based help, or discoverability questions.
- Use `quick-reference` when the user needs terse syntax reminders.
- Use `psdocs` only when the user explicitly asks about PSDocs.
