#!/usr/bin/env python3
"""Fireplace page: cut the fireplace part out of each square variant image for the sideways strip.

    python crop_fireplace.py            # all docs/img/fireplace/v<N>/k-*-1600.webp → k-*-crop-600.webp

The strip on the page shows the crop (fireplace plus the start of the TV wall); the lightbox shows the
whole view. Crop keeps the left 600/1024 of the width (full height), whatever the source size.
"""
import sys
from pathlib import Path
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent
LEFT = 600 / 1024          # share of the width kept, measured on the 1024-px batch images
QUALITY = 84


def main() -> int:
    fp = yaml.safe_load((ROOT / "content" / "fireplace.yaml").read_text(encoding="utf-8"))["fireplace"]
    d = ROOT / "docs" / "img" / "fireplace" / f"v{fp['img_version']}"
    n = 0
    for src in sorted(d.glob("k-*-1600.webp")):
        im = Image.open(src).convert("RGB")
        w, h = im.size
        out = d / src.name.replace("-1600.webp", "-crop-600.webp")
        im.crop((0, 0, round(w * LEFT), h)).save(out, "WEBP", quality=QUALITY, method=6)
        n += 1
    print(f"{n} crops written to {d.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
