#!/usr/bin/env python3
"""Convert source renders into web-ready images.

Usage:
    python ingest.py <room-slug> <version> <file.png> [file2.png ...]

Files are named by their stem (e.g. view-1.png -> view-1), and written to
docs/img/<room-slug>/v<version>/<stem>-<width>.webp for each width in SIZES.
Existing outputs are overwritten. Nothing else is touched; add the image
entries to content/book.yaml afterwards.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SIZES = (900, 1600)          # widths; a source narrower than a size is not upscaled
QUALITY = 84


def convert(src: Path, out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    written = []
    for w in SIZES:
        target = min(w, im.width)
        h = round(im.height * target / im.width)
        resized = im if target == im.width else im.resize((target, h), Image.LANCZOS)
        out = out_dir / f"{src.stem}-{w}.webp"
        resized.save(out, "WEBP", quality=QUALITY, method=6)
        written.append(f"{out.relative_to(ROOT)}  {resized.width}x{resized.height}  {out.stat().st_size // 1024} KB")
    return written


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__)
        return 1
    slug, version, files = argv[1], argv[2].lstrip("v"), argv[3:]
    out_dir = ROOT / "docs" / "img" / slug / f"v{version}"
    for f in files:
        for line in convert(Path(f), out_dir):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
