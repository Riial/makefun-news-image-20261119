#!/usr/bin/env python3
"""World News Summary — 19 November 2026 (bento grid entry).

Writes the entry image to /output/entry.png.

The image is produced from bento.html + bento.css (editorial bento-grid
layout, rendered with a headless browser at 2x and downscaled to
1024x576). The sandbox runs Python 3.13 stdlib-only with no network and
no browser, so this program ships the finished image in the repository
and copies it to the output path — the documented "simplest entry"
pattern. The copy is byte-for-byte deterministic.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "bento.png")
DST = "/output/entry.png"


def main() -> None:
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
