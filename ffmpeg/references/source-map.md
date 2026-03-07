# FFmpeg Reference Map

Use this file first to choose the smallest useful source set.

## Core tools

- `ffmpeg-tool` -> `ffmpeg tool Documentation.pdf`: Primary CLI reference for `ffmpeg` options, stream handling, filtergraphs, and transcoding behavior.
- `ffprobe-tool` -> `ffprobe tool Documentation.pdf`: Primary CLI reference for `ffprobe` inspection, output formatting, and stream or format queries.

## Subsystem references

- `codecs` -> `FFmpeg Codecs Documentation.pdf`: Encoder, decoder, and codec-specific options.
- `protocols` -> `FFmpeg Protocols Documentation.pdf`: Network and file protocols such as RTMP, HLS-related transport details, SRT, HTTP, and others.
- `devices` -> `FFmpeg Input Output Devices Documentation.pdf`: Capture and output devices, including desktop and webcam related device interfaces.

## Task guides

- `filtering` -> `Filtering Guide – FFmpeg.pdf`: Filtergraph concepts and examples.
- `scaling` -> `Scaling – FFmpeg.pdf`: Resize and scale workflows.
- `cropping` -> `Cropping Video – FFmpeg.pdf`: Crop expressions and examples.
- `mapping` -> `Selecting streams with the -map option – FFmpeg.pdf`: Stream selection and mapping examples.
- `multi-output` -> `Creating multiple outputs – FFmpeg.pdf`: One-input to many-outputs workflows.
- `desktop-capture` -> `Capture_Desktop – FFmpeg.pdf`: Desktop or screen capture patterns.
- `webcam-capture` -> `Capture_Webcam – FFmpeg.pdf`: Webcam capture patterns.
- `streaming-guide` -> `Streaming Guide – FFmpeg.pdf`: Streaming workflows and publishing patterns.
- `streaming-sites` -> `Encoding Fo rStreaming Sites – FFmpeg.pdf`: Service-oriented encoding examples.
- `denoise` -> `Denoise Examples – FFmpeg.pdf`: Denoising examples and filter usage.
- `errors` -> `Errors troubleshooting – FFmpeg.pdf`: Troubleshooting and common error explanations.

## Hardware acceleration

- `hwaccel-intro` -> `FFMPEG HW AccelIerators intro Hardware encoders decoder.pdf`: General hardware-acceleration overview.
- `hwaccel-qsv` -> `Hardware_QuickSync Intel Quick Sync Video FFmpeg.pdf`: Intel Quick Sync guidance.
- `qsv-guide` -> `quicksync-video-ffmpeg qsv Intel Graphics.pdf`: Additional Intel QSV workflow details.

## Supplemental references

- `hardware-cheatsheet` -> `ffmpeg-hw-accelerators-cheat-sheet.md`: Local workflow for checking build support, identifying host GPU hardware, matching FFmpeg encoder names, and running null-output hardware tests.
- `book` -> `FFmpeg_Book.pdf`: Broad background and worked examples.
- `ffserver` -> `ffserver – FFmpeg.pdf`: Historical reference for deprecated `ffserver` workflows.

## Suggested starting points

- Use `ffprobe-tool` for media inspection questions.
- Use `ffmpeg-tool` plus `mapping` for stream copy, selection, or container questions.
- Use `codecs` when encoder or decoder private options matter.
- Use `protocols` plus `streaming-guide` for live publishing questions.
- Use `devices`, `desktop-capture`, or `webcam-capture` for capture-device workflows.
- Use `hardware-cheatsheet` before deep PDF reading when the user first needs to confirm whether hardware acceleration is even available on the current machine.
- Use the hardware references only after confirming the user actually needs accelerator-specific behavior.
