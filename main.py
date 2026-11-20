#!/usr/bin/env python3
"""Copy the built front-page image to the output directory.

The entry image (entry.png, drawn by draw.py) sits beside this file.
This program is the competition entrypoint: it copies that image to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (default ``/output``), creating the
output directory if needed.  Standard library only, no network, and
fully deterministic -- the bytes copied are the bytes committed.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # Never copy a file onto itself (e.g. if the output dir is the repo).
    if os.path.abspath(src) == os.path.abspath(dst):
        return 0
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
