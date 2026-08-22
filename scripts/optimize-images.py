#!/usr/bin/env python3
"""Batch-resize and compress a folder of raw event photos for the ESSF gallery.

Output filenames are sanitised to be URL-safe: `DSC_1199A (5).JPG` becomes
`DSC_1199A_05.jpg`, and a short numeric suffix is zero-padded to 4 so
`DSC_460.JPG` sorts with its `DSC_0xxx` siblings instead of after `DSC_1398`.

Usage:
  python3 scripts/optimize-images.py <input_folder> <output_folder> [--max-dim N] [--quality Q]

Example:
  python3 scripts/optimize-images.py ~/Downloads/bharat-mandapam-selects assets/images/events/04-07-2026
  python3 scripts/optimize-images.py ~/tmp/raw assets/images/events/04-07-2026/thumbs --max-dim 500 --quality 78
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

MAX_DIMENSION = 1600
JPEG_QUALITY = 82
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

SERIES_RE = re.compile(r"^(.*?)\s*\((\d+)\)$")       # "DSC_1199A (5)"  → DSC_1199A_05
SHORT_NUM_RE = re.compile(r"^([A-Za-z]+_)(\d{1,3})$")  # "DSC_460"        → DSC_0460


def sanitize_stem(stem: str) -> str:
    """Make a filename stem URL-safe and correctly sortable."""
    series = SERIES_RE.match(stem)
    if series:
        return f"{series.group(1)}_{int(series.group(2)):02d}"

    short = SHORT_NUM_RE.match(stem)
    if short:
        return f"{short.group(1)}{int(short.group(2)):04d}"

    return stem.replace(" ", "_")


def optimize(input_dir: Path, output_dir: Path, max_dim: int, quality: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in VALID_EXTENSIONS)

    if not files:
        print(f"No images found in {input_dir}")
        return

    written: dict[str, str] = {}
    for src in files:
        im = Image.open(src)
        im = ImageOps.exif_transpose(im)  # respect camera rotation
        if im.mode != "RGB":
            im = im.convert("RGB")

        im.thumbnail((max_dim, max_dim), Image.LANCZOS)

        stem = sanitize_stem(src.stem)
        if stem in written:
            print(f"Name collision: {src.name} and {written[stem]} both map to {stem}.jpg")
            sys.exit(1)
        written[stem] = src.name

        dest = output_dir / f"{stem}.jpg"
        im.save(dest, "JPEG", quality=quality, optimize=True)

        before_kb = src.stat().st_size / 1024
        after_kb = dest.stat().st_size / 1024
        print(f"{src.name} → {dest.name}  {before_kb:.0f}KB → {after_kb:.0f}KB  {im.size}")

    print(f"\nDone. {len(files)} images written to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_folder")
    parser.add_argument("output_folder")
    parser.add_argument("--max-dim", type=int, default=MAX_DIMENSION, help="long-edge cap in pixels")
    parser.add_argument("--quality", type=int, default=JPEG_QUALITY, help="JPEG quality, 1-95")
    args = parser.parse_args()

    if not 1 <= args.quality <= 95:
        print("--quality must be between 1 and 95")
        sys.exit(1)

    input_dir = Path(args.input_folder).expanduser()
    output_dir = Path(args.output_folder).expanduser()

    if not input_dir.is_dir():
        print(f"Input folder not found: {input_dir}")
        sys.exit(1)

    optimize(input_dir, output_dir, args.max_dim, args.quality)
