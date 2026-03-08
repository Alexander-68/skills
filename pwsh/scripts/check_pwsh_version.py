#!/usr/bin/env python3
"""Check the installed pwsh version against a required minimum."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Version:
    parts: tuple[int, ...]

    @classmethod
    def parse(cls, raw: str) -> "Version":
        match = re.search(r"\d+(?:\.\d+)+", raw.strip())
        if not match:
            raise ValueError(f"could not parse version from: {raw!r}")
        return cls(tuple(int(part) for part in match.group(0).split('.')))

    def __str__(self) -> str:
        return '.'.join(str(part) for part in self.parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the installed pwsh version meets a required minimum.",
    )
    parser.add_argument(
        '--command',
        default='pwsh',
        help="PowerShell executable to run (default: pwsh).",
    )
    parser.add_argument(
        '--min-version',
        default='7.5.4',
        help="Minimum acceptable PowerShell version (default: 7.5.4).",
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Print machine-readable JSON output.",
    )
    return parser.parse_args()


def detect_version(command: str) -> tuple[str | None, str | None, str | None]:
    resolved = shutil.which(command)
    if resolved is None:
        return None, None, f"command not found: {command}"

    try:
        completed = subprocess.run(
            [command, '-NoLogo', '-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
        )
    except OSError as exc:
        return resolved, None, f"failed to run {command}: {exc}"

    output = (completed.stdout or '').strip()
    error = (completed.stderr or '').strip()
    if completed.returncode != 0:
        detail = error or output or f"exit code {completed.returncode}"
        return resolved, None, detail
    if not output:
        return resolved, None, 'pwsh returned no version text'
    return resolved, output, None


def main() -> int:
    args = parse_args()

    try:
        minimum = Version.parse(args.min_version)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    resolved, detected_raw, error = detect_version(args.command)
    if error is not None:
        payload = {
            'command': args.command,
            'resolved_path': resolved,
            'required_minimum': str(minimum),
            'ok': False,
            'error': error,
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"error: {error}", file=sys.stderr)
        return 2

    try:
        detected = Version.parse(detected_raw or '')
    except ValueError as exc:
        payload = {
            'command': args.command,
            'resolved_path': resolved,
            'required_minimum': str(minimum),
            'ok': False,
            'error': str(exc),
            'raw_output': detected_raw,
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2

    ok = detected >= minimum
    payload = {
        'command': args.command,
        'resolved_path': resolved,
        'detected_version': str(detected),
        'required_minimum': str(minimum),
        'ok': ok,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        status = 'meets' if ok else 'does not meet'
        print(
            f"{args.command} {detected} at {resolved} {status} the minimum version {minimum}."
        )

    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
