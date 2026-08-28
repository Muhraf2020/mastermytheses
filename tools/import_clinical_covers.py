#!/usr/bin/env python3
"""
import_clinical_covers.py - derive site covers for the eight books this site is
the only home for.

The eighteen covers already here follow a fixed convention, and new ones must
match it exactly or they look wrong in the same grid:

    assets/img/<slug>.jpg        938x1500   full size
    assets/img/<slug>-600.jpg    600x960    small variant for srcset
    assets/img/<slug>.webp       938x1500
    assets/img/<slug>-600.webp   600x960

Sources are the author's originals. Filenames there carry no slug, and the five
clinical workbooks are numbered CW01-CW05 rather than named, so SOURCES records
the mapping explicitly. Each was confirmed by opening the file and reading the
cover, and the template count printed on each cover matches local_books.py.

Fit is a centre crop, not a pad. Five of the eight are exactly 5:8 and are
untouched by it. The three "Simplified" covers are 1700x2560, and letterboxing
those would put white bars across a dark navy cover; trimming about 3% from each
side is invisible by comparison. A crop deeper than MAX_CROP is refused rather
than silently mangling artwork.

    python tools/import_clinical_covers.py            # import
    python tools/import_clinical_covers.py --check    # report only, write nothing
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python -m pip install Pillow")

REPO = Path(__file__).resolve().parent.parent
DROP = REPO / "incoming-covers"
LIBRARY = Path(os.environ.get("BOOKS_DIR", "D:/books"))
OUT = REPO / "assets" / "img"

# slug -> filename in the author's book library. Verified visually, one by one.
SOURCES = {
    "clinical-audit-quality-improvement":       "CW01_eBook_Cover_1600x2560.png",
    "evidence-based-practice-project":          "CW02_eBook_Cover_1600x2560.jpg",
    "clinical-case-report":                     "CW03_eBook_Cover_1600x2560.png",
    "implementation-science":                   "CW04_eBook_Cover_1600x2560.jpg",
    "clinical-trial-protocol":                  "CW05_eBook_Cover_1600x2560.jpg",
    "clinical-research-design-simplified":      "Clinical_Research_Design_Simplified.jpg",
    "public-health-research-simplified":        "Public_Health_Research_Simplified_eBook Cover.jpg",
    "systematic-reviews-healthcare-simplified": "Systematic_Reviews_Meta_Analysis_Healthcare_Simplified ebook.jpg",
}

ACCEPT = (".jpg", ".jpeg", ".png", ".webp")
SIZES = [(938, 1500, ""), (600, 960, "-600")]
TARGET = 938 / 1500      # 0.6253, the 5:8 the grid assumes
MIN_WIDTH = 938
MAX_CROP = 0.15          # refuse to discard more than this fraction of a side


def find_source(slug):
    """Prefer a file dropped in incoming-covers/, else the mapped original."""
    for ext in ACCEPT:
        p = DROP / (slug + ext)
        if p.exists():
            return p
    name = SOURCES.get(slug)
    if name:
        p = LIBRARY / name
        if p.exists():
            return p
    return None


def derive(src, slug, write=True):
    notes, wrote = [], 0
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size

        if w < MIN_WIDTH:
            notes.append("only %dpx wide; upscaling to %dpx will look soft"
                         % (w, MIN_WIDTH))

        # Centre-crop to the target aspect, discarding the smaller dimension.
        want = TARGET
        have = w / h
        if have > want:                       # too wide: trim left and right
            new_w = int(round(h * want))
            off = (w - new_w) // 2
            box = (off, 0, off + new_w, h)
            frac = (w - new_w) / w
            side = "width"
        else:                                 # too tall: trim top and bottom
            new_h = int(round(w / want))
            off = (h - new_h) // 2
            box = (0, off, w, off + new_h)
            frac = (h - new_h) / h
            side = "height"

        if frac > MAX_CROP:
            raise ValueError("would crop %.0f%% off the %s (limit %.0f%%); "
                             "this cover is the wrong shape for the grid"
                             % (frac * 100, side, MAX_CROP * 100))
        if frac > 0.005:
            notes.append("cropped %.1f%% off the %s to reach 5:8 (%.1f%% per edge)"
                         % (frac * 100, side, frac * 50))

        if not write:
            return notes, 0

        cropped = im.crop(box)
        for tw, th, suffix in SIZES:
            out = cropped.resize((tw, th), Image.LANCZOS)
            out.save(OUT / ("%s%s.jpg" % (slug, suffix)), "JPEG",
                     quality=88, optimize=True, progressive=True)
            out.save(OUT / ("%s%s.webp" % (slug, suffix)), "WEBP", quality=86)
            wrote += 2
    return notes, wrote


def main():
    check_only = "--check" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)

    missing, done, total = [], 0, 0
    for slug in sorted(SOURCES):
        src = find_source(slug)
        if src is None:
            missing.append(slug)
            print("  MISSING  %s" % slug)
            continue
        try:
            notes, wrote = derive(src, slug, write=not check_only)
        except Exception as exc:
            missing.append(slug)
            print("  UNUSABLE %s: %s" % (slug, exc))
            continue
        total += wrote
        done += 1
        print("  %s %-44s <- %s" % ("check" if check_only else "wrote", slug, src.name))
        for n in notes:
            print("           note: %s" % n)

    print("\n  %d of %d covers %s, %d files written"
          % (done, len(SOURCES), "checked" if check_only else "imported", total))
    if missing:
        print("\n  still needed:")
        for s in missing:
            print("    %s" % s)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
