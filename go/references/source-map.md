# Go References Source Map

Use this map to pick the smallest set of PDFs needed for a question.

## Core Language

- `Go Programming Language Specification.pdf`: Syntax, types, declarations, statements, interfaces, generics, and built-in language rules.
- `Go Memory Model.pdf`: `happens-before`, synchronization, and visibility guarantees.
- `Effective Go Guide.pdf`: Idiomatic guidance and recommended style patterns.

## Package Index

- `Standard library - Go Packages.pdf`: Entry point for package discovery and package-level summaries.

## Package-Specific PDFs Included

- `archive/tar`: `tar package - archive_tar - Go Packages.pdf`
- `archive/zip`: `zip package - archive_zip - Go Packages.pdf`
- `argon2`: `argon2 package Go Packages.pdf`
- `crypto`: `crypto package - crypto - Go Packages.pdf`
- `crypto/cipher`: `cipher package - crypto_cipher - Go Packages.pdf`
- `crypto/rsa`: `rsa package - crypto_rsa - Go Packages.pdf`
- `crypto/x509`: `x509 package - crypto_x509 - Go Packages.pdf`
- `encoding/gob`: `gob package - encoding_gob - Go Packages.pdf`
- `net/http`: `http package - net_http - Go Packages.pdf`
- `image`: `image package - image - Go Packages.pdf`
- `image/color`: `color package - image_color - Go Packages.pdf`
- `image/draw`: `draw package - image_draw - Go Packages.pdf`
- `regexp`: `regexp package - regexp - Go Packages.pdf`
- `regexp/syntax`: `syntax package - regexp_syntax - Go Packages.pdf`
- `sort`: `sort package - sort - Go Packages.pdf`

## Tooling and Performance

- `Go Fuzzing - The Go Programming Language.pdf`
- `Tutorial_ Getting started with fuzzing.pdf`
- `Coverage profiling support for integration tests.pdf`
- `Profile-guided optimization.pdf`
- `Managing dependencies.pdf`

## Supplemental Articles

- `JSON and Go - The Go Programming Language.pdf`
- `Writing Web Applications.pdf`
- `Tutorial_ Developing a RESTful API with Go and Gin.pdf`
- `A Guide to the Go Garbage Collector.pdf`
- `The Go image package.pdf`
- `The Go image_draw package.pdf`

Use supplemental articles only when the spec or package docs do not directly answer the question.

## Secure App and Web Guidance

- Password hashing: Prefer `argon2 package Go Packages.pdf` for API behavior. For new application guidance, prefer Argon2id and store password hashes instead of plaintext passwords.
- Certificates and TLS: Use `x509 package - crypto_x509 - Go Packages.pdf` and `rsa package - crypto_rsa - Go Packages.pdf` when generating self-signed certificates or reasoning about certificate and key handling.
- Web stack: Prefer `net/http` plus `html/template`, locally served `htmx.min.js`, and Tailwind CSS for server-rendered applications.
- Session management: Prefer secure, `HttpOnly`, `SameSite=Strict` cookies over JWTs for typical web sessions.
- `net/http`: Use `http package - net_http - Go Packages.pdf` for API behavior and `Writing Web Applications.pdf` for supplemental HTTP/web patterns.
