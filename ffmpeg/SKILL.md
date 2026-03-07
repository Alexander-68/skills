---
name: ffmpeg
description: Use bundled FFmpeg and FFprobe reference PDFs to verify command-line options, codecs, filters, protocols, streaming workflows, capture devices, troubleshooting steps, and hardware acceleration guidance. Use when Codex needs authoritative local references for `ffmpeg` or `ffprobe` commands, media inspection, transcoding, encoding, decoding, scaling, filtering, stream mapping, desktop or webcam capture, live streaming, or accelerator-specific behavior such as QSV and other hardware backends.
---

# FFmpeg and FFprobe Reference

## Overview

Use this skill to answer FFmpeg and FFprobe questions with document-grounded citations from bundled PDFs in [`references/`](references/). Treat the tool documentation PDFs as the primary source for CLI syntax and option behavior, then use task guides for workflows and examples.

## Workflow

1. Classify the request.
- Determine whether the question is about `ffmpeg` CLI syntax, `ffprobe` inspection, codecs, filters, protocols, devices, streaming, hardware acceleration, or troubleshooting.

2. Select the minimum source set.
- Start with [`references/source-map.md`](references/source-map.md).
- Prefer the most normative document available for the exact topic.

3. Search before reading deeply.
- Use [`scripts/search_ffmpeg_refs.py`](scripts/search_ffmpeg_refs.py) to find candidate pages quickly.
- Open only the specific PDFs that match the request.

4. Separate document facts from local-build facts.
- Use the bundled PDFs for documented behavior.
- When the answer depends on the installed binary, verify locally with commands such as `ffmpeg -version`, `ffmpeg -buildconf`, `ffmpeg -encoders`, `ffmpeg -decoders`, `ffmpeg -hwaccels`, `ffmpeg -filters`, `ffmpeg -protocols`, `ffmpeg -devices`, or `ffprobe -show_streams -show_format INPUT`.

5. Return a cited answer.
- Provide the command or conclusion first.
- Add concise citations in the format `[Document, p. X]` or `[Document, section/page]`.
- State clearly when a claim is inferred from examples rather than stated normatively.

## Fast Lookup Script

Use [`scripts/search_ffmpeg_refs.py`](scripts/search_ffmpeg_refs.py) to search the bundled PDFs.

- List document aliases:
`python scripts/search_ffmpeg_refs.py --list-docs`
- Search all references:
`python scripts/search_ffmpeg_refs.py "hwaccel" --max-hits 10`
- Search one document alias:
`python scripts/search_ffmpeg_refs.py "-map" --doc mapping --max-hits 10`
- Regex search:
`python scripts/search_ffmpeg_refs.py "RTMP|HLS|SRT" --doc protocols --regex --max-hits 10`

Install dependency once per environment if needed:
`pip install pypdf`

## Source Priority

Use this priority when sources overlap:

1. `ffmpeg tool Documentation.pdf` and `ffprobe tool Documentation.pdf` for CLI options, syntax, and command behavior.
2. `FFmpeg Codecs Documentation.pdf`, `FFmpeg Protocols Documentation.pdf`, and `FFmpeg Input Output Devices Documentation.pdf` for subsystem-specific details.
3. Hardware references for accelerator-specific workflows and limits.
4. Task guides such as filtering, scaling, cropping, mapping, capture, streaming, and troubleshooting for worked examples.
5. `FFmpeg_Book.pdf` for broader conceptual context when the official docs are not enough.

## Citation and Version Rules

- Cite every non-trivial technical claim.
- Distinguish official tool or subsystem documentation from cookbook-style examples.
- Do not assume an encoder, decoder, device, protocol, or accelerator is available just because the docs describe it; verify locally when availability matters.
- Treat `ffserver` guidance as historical unless the user explicitly asks about it.
- If the bundled references do not cover the exact build, codec, or accelerator variant the user asked about, state that gap explicitly.

## Reference Selection Guide

- Use `ffmpeg-tool` for global options, stream selection, filtergraphs, and CLI syntax.
- Use `ffprobe-tool` for metadata inspection, stream introspection, and output formatting.
- Use `codecs`, `protocols`, and `devices` for subsystem-specific options and support matrices.
- Use `filtering`, `scaling`, `cropping`, `mapping`, `desktop-capture`, `webcam-capture`, and `multi-output` for task workflows.
- Use `hwaccel-intro`, `hwaccel-qsv`, and `qsv-guide` for hardware-accelerated pipelines.
- Use `errors` when the user reports runtime failures, muxing issues, or format mismatches.

## Hardware Acceleration Triage

Use [`references/ffmpeg-hw-accelerators-cheat-sheet.md`](references/ffmpeg-hw-accelerators-cheat-sheet.md) when the user asks whether FFmpeg can use a GPU, how to enable NVENC/QSV/AMF/VAAPI/VideoToolbox, or why hardware encoding or decoding fails.

Follow this order:

1. Check FFmpeg build capabilities.
- Run `ffmpeg -encoders`, `ffmpeg -decoders`, and `ffmpeg -hwaccels` before assuming GPU support exists.

2. Check host hardware.
- Identify the actual installed GPU with the OS-appropriate command before recommending a hardware path.

3. Match vendor to FFmpeg names.
- Map NVIDIA to `cuda`/`cuvid`/`*_nvenc`, Intel to `qsv`, AMD to `amf` on Windows or `vaapi` on Linux, and Apple hardware to `videotoolbox`.

4. Run an acid test.
- Prefer a null-output encode test such as `ffmpeg -f lavfi -i testsrc -c:v h264_nvenc -f null -` to confirm the FFmpeg build, driver, and hardware path actually work together.

5. Suggest the next fix.
- If the test fails with messages such as `Function not implemented` or `Device not found`, suggest updating the vendor graphics driver and then re-checking FFmpeg capabilities.

## Answer Style

- Prefer a ready-to-run command when the user is asking how to do something.
- Explain placeholders such as input paths, stream indexes, bitrate values, and device names.
- Mention shell-specific escaping when filter expressions or complex maps are involved.
- Keep citations compact and attach them to the exact claim they support.
