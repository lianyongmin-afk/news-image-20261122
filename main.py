#!/usr/bin/env python3
"""Entrypoint for news-image-20261122.

Writes the pre-rendered infographic for Sunday 22 November 2026
(entry.png, shipped in this repository) to the grader output path.

Only the Python standard library is used. The operation is a plain
byte copy, so running it twice produces identical output bytes.
"""

import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.png"


def run() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    blob = target.read_bytes()
    if blob[:8] != PNG_MAGIC:
        print("error: output does not start with the PNG signature",
              file=sys.stderr)
        return 1
    if len(blob) > MAX_BYTES:
        print(f"error: output is {len(blob)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
