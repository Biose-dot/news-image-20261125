#!/usr/bin/env python3
"""Deliver the committed front-page image for news-image-20261125.

The artwork (entry.png, a 1024x1024 newspaper front page drawn by
build_image.py at build time) ships inside this repository. At run
time the grader's container is a bare python:3.13 with no Pillow, so
this entrypoint does the one job that matters there: place a verified
copy of entry.png into $MAKEFUN_OUTPUT_DIR (default /output).

Standard library only, no network, no clock: the same input file
always lands byte-for-byte in the output directory.
"""

import hashlib
import os
import sys

SIGNATURE = b"\x89PNG\r\n\x1a\n"
TRAILER = b"IEND\xaeB`\x82"
CHUNK = 128 * 1024


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def asset_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "entry.png")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def check_png(path):
    """Return the byte size of a complete 1024x1024 PNG, or raise."""
    with open(path, "rb") as fh:
        blob = fh.read()
    if not blob.startswith(SIGNATURE):
        raise ValueError("bad PNG signature: %s" % path)
    if TRAILER not in blob[-16:]:
        raise ValueError("missing IEND trailer: %s" % path)
    if len(blob) < 1024:
        raise ValueError("suspiciously small PNG: %s" % path)
    # IHDR sits right after the signature: length(4) + "IHDR"(4),
    # then width and height as big-endian uint32 at bytes 16 and 20.
    if blob[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR: %s" % path)
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if (width, height) != (1024, 1024):
        raise ValueError("expected 1024x1024, got %dx%d: %s"
                         % (width, height, path))
    return len(blob)


def deliver():
    src = asset_path()
    size = check_png(src)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    dst = os.path.join(target_dir, "entry.png")
    staging = dst + ".part"
    with open(src, "rb") as fin, open(staging, "wb") as fout:
        while True:
            block = fin.read(CHUNK)
            if not block:
                break
            fout.write(block)
    os.replace(staging, dst)
    if check_png(dst) != size or digest(dst) != digest(src):
        raise ValueError("copied file failed verification: %s" % dst)
    print("entry.png delivered: %d bytes sha256=%s" % (size, digest(dst)))
    return dst


def main():
    try:
        deliver()
    except Exception as exc:
        print("delivery failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
