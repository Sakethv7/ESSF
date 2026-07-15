#!/usr/bin/env python3
"""Batch-resize and compress a folder of raw event photos for the ESSF gallery.

Usage:
  python3 scripts/optimize-images.py <input_folder> <output_folder>

Example:
  python3 scripts/optimize-images.py ~/Downloads/bharat-mandapam-selects assets/images/events/04-07-2026
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

MAX_DIMENSION = 1600
JPEG_QUALITY = 82
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def optimize(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in VALID_EXTENSIONS)

    if not files:
        print(f"No images found in {input_dir}")
        return

    for src in files:
        im = Image.open(src)
        im = ImageOps.exif_transpose(im)  # respect camera rotation
        if im.mode != "RGB":
            im = im.convert("RGB")

        im.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

        dest = output_dir / f"{src.stem}.jpg"
        im.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)

        before_kb = src.stat().st_size / 1024
        after_kb = dest.stat().st_size / 1024
        print(f"{src.name} → {dest.name}  {before_kb:.0f}KB → {after_kb:.0f}KB  {im.size}")

    print(f"\nDone. {len(files)} images written to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_dir = Path(sys.argv[1]).expanduser()
    output_dir = Path(sys.argv[2]).expanduser()

    if not input_dir.is_dir():
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)

    optimize(input_dir, output_dir)
