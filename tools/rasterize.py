"""SVG -> PNG at the SVG's own declared size, via headless Chrome.

`qlmanage -t` silently CROPS wide SVGs instead of scaling them, which makes
rendered specimens look like layout bugs (content missing at the right edge)
when the SVG is actually fine.  Every LOOK loop in this repo should go
through here instead.

    python3 tools/rasterize.py out.png in.svg [more.svg ...]
    python3 tools/rasterize.py --scale 2 dir/*.svg      # writes <name>.png
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "/Applications/Chromium.app/Contents/MacOS/Chromium")


def chrome_path():
    for p in CHROME:
        if os.path.exists(p):
            return p
    raise SystemExit("no Chrome/Chromium found for rasterizing")


def svg_size(path):
    head = open(path).read(600)
    w = re.search(r'width="([\d.]+)"', head)
    h = re.search(r'height="([\d.]+)"', head)
    if not (w and h):
        raise SystemExit(f"{path}: no width/height on the root <svg>")
    return int(float(w.group(1))), int(float(h.group(1)))


def render(src, out, scale=2):
    w, h = svg_size(src)
    cmd = [chrome_path(), "--headless", "--disable-gpu", "--hide-scrollbars",
           f"--screenshot={os.path.abspath(out)}",
           f"--window-size={w},{h}",
           f"--force-device-scale-factor={scale}",
           "file://" + os.path.abspath(src)]
    r = subprocess.run(cmd, capture_output=True)
    if not os.path.exists(out):
        sys.stderr.write(r.stderr.decode()[-800:])
        raise SystemExit(f"failed to rasterize {src}")
    return out, w, h


def main(argv):
    scale = 2
    if argv and argv[0] == "--scale":
        scale = int(argv[1])
        argv = argv[2:]
    if len(argv) >= 2 and argv[0].endswith(".png"):
        out, srcs = argv[0], argv[1:]
        if len(srcs) != 1:
            raise SystemExit("one .svg per explicit .png output")
        print(render(srcs[0], out, scale))
        return 0
    for src in argv:
        out = os.path.splitext(src)[0] + ".png"
        print(render(src, out, scale))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
