#!/usr/bin/env python3
"""
import_clinical_covers.py - turn the cover originals dropped in incoming-covers/
into the four variants every book card on this site expects.

The eighteen covers this site already carries follow a fixed convention, and new
ones must match it exactly or they will look wrong in the same grid:

    assets/img/<slug>.jpg        938x1500   full size
    assets/img/<slug>-600.jpg    600x960    small variant for srcset
    assets/img/<slug>.webp       938x1500
    assets/img/<slug>-600.webp   600x960

Originals stay in incoming-covers/ (git-ignored). Only the derived files ship,
so re-running after replacing an original simply refreshes them.

    python tools/import_clinical_covers.py            # import what is present
    python tools/import_clinical_covers.py --check    # report only, write nothing

Exit status is non-zero if a cover is missing or unusable, so this can gate a
build. A missing cover is reported, never substituted.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python -m pip install Pillow")

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "incoming-covers"
OUT = REPO / "assets" / "img"

# The eight books this site is the only home for. Slugs match local_books.py;
# build_site.py derives the image name from the slug, so these must agree.
SLUGS = [
    "clinical-audit-quality-improvement",
    "clinical-case-report",
    "clinical-research-design-simplified",
    "clinical-trial-protocol",
    "evidence-based-practice-project",
    "implementation-science",
    "public-health-research-simplified",
    "systematic-reviews-healthcare-simplified",
]

ACCEPT = (".jpg", ".jpeg", ".png", ".webp")
SIZES = [(938, 1500, ""), (600, 960, "-600")]
TARGET_RATIO = 1500 / 938          # 1.599, the 5:8 portrait the grid assumes
RATIO_TOLERANCE = 0.06             # a few percent of letterboxing is invisible
MIN_WIDTH = 938                    # below this we are upscaling


def find_source(slug):
    """Return the dropped original for a slug, whatever extension it carries."""
    for ext in ACCEPT:
        p = SRC / (slug + ext)
        if p.exists():
            return p
    # tolerate a stray suffix like "-cover" so a KDP download works unrenamed
    for p in sorted(SRC.iterdir()) if SRC.is_dir() else []:
        if p.suffix.lower() in ACCEPT and p.stem.lower().startswith(slug):
            return p
    return None


def derive(src, slug, write=True):
    """Produce the four variants. Returns (notes, wrote_count)."""
    notes, wrote = [], 0
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        ratio = h / w

        if abs(ratio - TARGET_RATIO) > RATIO_TOLERANCE:
            notes.append("shape %dx%d (ratio %.2f, expected %.2f) - it will be "
                         "letterboxed onto the 5:8 card rather than cropped"
                         % (w, h, ratio, TARGET_RATIO))
        if w < MIN_WIDTH:
            notes.append("only %dpx wide; upscaling to %dpx will look soft next "
                         "to the other covers" % (w, MIN_WIDTH))

        if not write:
            return notes, 0

        for tw, th, suffix in SIZES:
            # Fit inside the target box and pad, so nothing is ever cropped off
            # a cover. A correctly-proportioned source pads by zero pixels.
            fitted = im.copy()
            fitted.thumbnail((tw, th), Image.LANCZOS)
            canvas = Image.new("RGB", (tw, th), (255, 255, 255))
            canvas.paste(fitted, ((tw - fitted.width) // 2,
                                  (th - fitted.height) // 2))
            canvas.save(OUT / ("%s%s.jpg" % (slug, suffix)), "JPEG",
                        quality=88, optimize=True, progressive=True)
            canvas.save(OUT / ("%s%s.webp" % (slug, suffix)), "WEBP", quality=86)
            wrote += 2
    return notes, wrote


def main():
    check_only = "--check" in sys.argv
    if not SRC.is_dir():
        sys.exit("drop folder not found: %s" % SRC)
    OUT.mkdir(parents=True, exist_ok=True)

    missing, done, total_files = [], 0, 0
    for slug in SLUGS:
        src = find_source(slug)
        if src is None:
            missing.append(slug)
            print("  MISSING  %s" % slug)
            continue
        try:
            notes, wrote = derive(src, slug, write=not check_only)
        except Exception as exc:                      # unreadable / truncated file
            missing.append(slug)
            print("  UNUSABLE %s (%s): %s" % (slug, src.name, exc))
            continue
        total_files += wrote
        done += 1
        print("  %s %-44s <- %s" % ("check " if check_only else "import", slug, src.name))
        for n in notes:
            print("           warning: %s" % n)

    print("\n  %d of %d covers %s, %d files written"
          % (done, len(SLUGS), "checked" if check_only else "imported", total_files))
    if missing:
        print("\n  still needed (see incoming-covers/README.md):")
        for s in missing:
            print("    %s" % s)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
