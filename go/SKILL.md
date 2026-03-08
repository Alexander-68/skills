---
name: go
description: Verify and cite Go language rules and package behavior using bundled Go specification and package documentation PDFs. Use when Codex needs authoritative references for Go syntax, semantics, memory model behavior, secure password hashing with Argon2, TLS or certificate generation with crypto/x509 and crypto/rsa, standard net/http web-stack guidance, secure session-cookie handling, testing or profiling guidance, or details about bundled Go packages.
---

# Go Specification and Stdlib Reference

## Overview

Use this skill to answer Go questions with document-grounded citations from bundled PDFs in [`references/`](references/). Treat `Go Programming Language Specification.pdf` as the canonical spec snapshot shipped with this skill.

Apply the secure application defaults in this skill when the user asks for implementation recommendations, scaffolding, or architecture choices for Go applications.

## Workflow

1. Classify the request.
- Determine whether it is language specification, memory model, general guidance, tooling guidance, or package API behavior.

2. Select the minimum source set.
- Use [`references/source-map.md`](references/source-map.md) first.
- Prefer the most normative source available for the question.
- For secure application guidance, separate bundled API facts from this skill's implementation preferences.

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

## Secure Application Defaults

Apply these defaults for new Go applications unless the user gives a conflicting requirement.

- Prefer Argon2 password hashing for admin or user authentication flows.
- Store a password hash, not a password.
- Prefer Argon2id for new password-storage designs. Treat this as the secure default for this skill and discourage new bcrypt-based designs unless compatibility with an existing system requires bcrypt.
- Use `argon2 package Go Packages.pdf` for API-level details about Argon2 usage.
- When the user asks for standards justification beyond Go package behavior, state that the bundled references cover Go/package behavior and that the Argon2id preference is this skill's secure-default policy.

## TLS and Certificate Defaults

- When HTTPS, LDAPS, or another TLS endpoint needs local certificate files, prefer a startup routine that checks for `cert.pem` and `key.pem`.
- If the files do not exist, prefer generating a self-signed certificate on startup with `crypto/x509` and `crypto/rsa`, then write the generated certificate and key to those paths.
- Use `x509 package - crypto_x509 - Go Packages.pdf` and `rsa package - crypto_rsa - Go Packages.pdf` for API details and constraints.

## Web Layer Defaults

- Recommend the standard library web stack: `net/http` plus `html/template`.
- Prefer serving a local `htmx.min.js` asset instead of depending on a CDN.
- Prefer Tailwind CSS for styling when the user wants a lightweight server-rendered UI.
- Prefer stateful session management with secure cookies instead of JWTs for typical Go web applications.
- Set cookie attributes to `Secure`, `HttpOnly`, and `SameSite=Strict` unless a concrete cross-site requirement forces a narrower choice.
- Use `http package - net_http - Go Packages.pdf` for `net/http` API details, with `Writing Web Applications.pdf` as supplemental web-serving guidance.

## Citation and Version Rules

- Cite every non-trivial technical claim.
- Do not present tutorial guidance as a language requirement when the specification says otherwise.
- Do not present the secure defaults above as claims from the language specification unless the bundled references directly support the specific API or behavior.
- If the user asks about a newer Go release than what is represented in bundled docs, state that the answer is based on the bundled snapshot and call out possible version drift.
- When references conflict or are ambiguous, report the ambiguity and avoid definitive claims.

## Cross-Platform Notes

- Keep paths relative to the skill root.
- Use `bash scripts/search_go_refs.sh ...` on Linux/macOS and `pwsh -File scripts/search_go_refs.ps1 ...` on Windows.
- Install dependency once per environment: `pip install pypdf`.
