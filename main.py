#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261119 (v1).

Writes the pre-composed front page (assets/entry.png, "The World Today —
Thursday, 19 November 2026", 43 stories: 13 illustrated + 30 briefs)
to the output directory as entry.png.

The program is deliberately a plain byte copy: no network, no randomness,
no timestamps, so two runs always produce identical bytes. Before copying
it verifies the source image against its known SHA-256, so a corrupted
or swapped asset fails loudly instead of shipping a wrong image.
The byte copy also guarantees the output is a valid PNG — no re-encode,
no truncation, no surprises.

Usage:
    MAKEFUN_OUTPUT_DIR=<dir> python3 main.py

Writes <dir>/entry.png (creates the directory if needed).
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "b779b2507e6027a869cdd9700b11da7cd301e056b66b51198926003e232820c4"
ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "assets", "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isfile(ASSET):
        print(f"error: asset missing: {ASSET}", file=sys.stderr)
        return 1
    with open(ASSET, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(
            f"error: asset checksum mismatch: got {digest}, "
            f"expected {EXPECTED_SHA256}",
            file=sys.stderr,
        )
        return 1
    if len(data) == 0:
        print("error: asset is empty", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: asset is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1024 * 1024:
        print(f"error: asset is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    print(f"wrote {out_path} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
