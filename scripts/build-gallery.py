#!/usr/bin/env python3
"""Emit .gallery-item tiles into a page between marker comments.

Each tile's <img src> points at the thumbnail and its <a href> at the full-size
photo, so the grid stays light while the lightbox (and the no-JS fallback) still
gets the good image.

Usage:
  python3 scripts/build-gallery.py <page.html> <full_dir> <thumb_dir> --alt "<alt text prefix>"

Example:
  python3 scripts/build-gallery.py pages/gallery-bharat-mandapam.html \\
      assets/images/events/04-07-2026 assets/images/events/04-07-2026/thumbs \\
      --alt "ESSF Samman, Scholarship & Cultural Fest, Bharat Mandapam, 4 July 2026"
"""
import argparse
import html
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED TILES -->"
END = "<!-- END GENERATED TILES -->"

TILE = (
    '      <div class="gallery-item">'
    '<a href="{full}" target="_blank" rel="noopener">'
    '<img src="{thumb}" alt="{alt}" loading="lazy" /></a>'
    '<div class="overlay">View Full</div></div>'
)


def build(page: Path, full_dir: Path, thumb_dir: Path, alt_prefix: str) -> None:
    full = {p.stem: p for p in full_dir.glob("*.jpg")}
    thumbs = {p.stem: p for p in thumb_dir.glob("*.jpg")}

    missing_thumbs = sorted(full.keys() - thumbs.keys())
    orphan_thumbs = sorted(thumbs.keys() - full.keys())
    if missing_thumbs or orphan_thumbs:
        print(f"Tier mismatch — {len(missing_thumbs)} without thumbnails, {len(orphan_thumbs)} orphaned.")
        for stem in (missing_thumbs + orphan_thumbs)[:10]:
            print(f"  {stem}")
        sys.exit(1)

    text = page.read_text()
    if BEGIN not in text or END not in text or text.index(BEGIN) > text.index(END):
        print(f"Markers missing or out of order in {page}")
        sys.exit(1)

    stems = sorted(full)
    tiles = []
    for i, stem in enumerate(stems, 1):
        alt = html.escape(f"{alt_prefix} — photo {i} of {len(stems)}", quote=True)
        tiles.append(
            TILE.format(
                full=_rel(full[stem], page),
                thumb=_rel(thumbs[stem], page),
                alt=alt,
            )
        )

    head = text[: text.index(BEGIN) + len(BEGIN)]
    tail = text[text.index(END) :]
    page.write_text(head + "\n" + "\n".join(tiles) + "\n      " + tail)
    print(f"Wrote {len(tiles)} tiles to {page}")


def _rel(target: Path, page: Path) -> str:
    """Path to target relative to the page's own directory, using forward slashes."""
    import os

    return os.path.relpath(target.resolve(), page.resolve().parent).replace("\\", "/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page")
    parser.add_argument("full_dir")
    parser.add_argument("thumb_dir")
    parser.add_argument("--alt", required=True, help="alt text prefix, photo number is appended")
    args = parser.parse_args()

    build(Path(args.page), Path(args.full_dir), Path(args.thumb_dir), args.alt)
