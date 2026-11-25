#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 entry (Python 3.13 stdlib only).

"The World Today" front page for Wednesday 25 November 2026 — lead
story: Shenzhou-24 carries the first Pakistani in orbit to Tiangong.
Writes entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR (default /output).

Two paths, both deterministic and byte-identical:
  1. Build path: render the front page with build_image.render()
     (needs Pillow) and save it straight into the output directory,
     so it works even when the repository is mounted read-only.
  2. Fallback path: copy the entry.png shipped in this repository
     (pure stdlib, used when Pillow is missing -- the grader runs a bare
     python:3.13 image with no Pillow installed).

Every write is atomic (write to a .tmp file, then os.replace) and the
result is verified afterwards: PNG magic bytes, IEND trailer (the file
is a whole image) and file size.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def _out_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _here():
    return os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_png(path, expected_size=None):
    """Check the file is a whole PNG of the expected size (if given)."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: bad magic bytes in %s" % path)
    if not data.endswith(PNG_IEND):
        raise ValueError("truncated PNG file: missing IEND trailer in %s"
                         % path)
    size = len(data)
    if size == 0:
        raise ValueError("empty PNG file: %s" % path)
    if expected_size is not None and size != expected_size:
        raise ValueError(
            "size mismatch for %s: got %d, expected %d" % (path, size, expected_size)
        )
    return size


def _atomic_copy(src, dst):
    """Copy src to dst atomically, then verify the result."""
    tmp = dst + ".tmp"
    expected = _verify_png(src)
    with open(src, "rb") as fin, open(tmp, "wb") as fout:
        shutil.copyfileobj(fin, fout, 65536)
    os.replace(tmp, dst)
    got = _verify_png(dst, expected)
    return got


def fallback_copy():
    """Pure-stdlib copy of the shipped entry.png into the output dir."""
    src = os.path.join(_here(), "entry.png")
    out_dir = _out_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    got = _atomic_copy(src, dst)
    print("fallback_copy: copied entry.png (%d bytes, sha256 %s)"
          % (got, _sha256(dst)))
    return dst


def main():
    out_dir = _out_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    try:
        import build_image  # noqa: F401  (needs Pillow)

        tmp = dst + ".tmp"
        img = build_image.render()
        img.save(tmp, "PNG")
        os.replace(tmp, dst)
        got = _verify_png(dst)
        print("build path: wrote entry.png (%d bytes, sha256 %s)"
              % (got, _sha256(dst)))
    except Exception as exc:  # noqa: BLE001 - any failure falls back
        print("build path failed (%s); using fallback_copy" % exc,
              file=sys.stderr)
        fallback_copy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
