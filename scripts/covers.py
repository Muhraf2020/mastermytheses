# -*- coding: utf-8 -*-
"""
covers.py - the one place that knows which image belongs to which book.

Three groups of books share one grid, and their covers arrived by three routes:

  local (8)          <slug>       imported from incoming-covers/ by
                                  tools/import_clinical_covers.py
  gradsummit (9)     <slug>       already in the repo from the original site
  Research Made      rmp-<slug>   copied from the sibling gradsummit repo, which
  Practical (9)                   derived them from the 1600x2560 originals

The rmp- prefix exists because a workbook slug like "dissertation" would
otherwise sit one underscore away from "dissertation-literature-review-sprint".

Every book must resolve to four files, so a card can never render a broken
image. missing() reports what is absent; build_site.py refuses to build without
--allow-missing-covers so a half-covered grid cannot ship by accident.
"""

import html
from pathlib import Path

IMG_DIR = Path(__file__).resolve().parent.parent / "assets" / "img"
IMG_URL = "/assets/img"

# Widths that exist on disk for every cover, smallest first.
WIDTHS = [(600, "-600"), (938, "")]

# How wide a card renders, so the browser picks the right file. Mirrors the
# .grid-3 breakpoints in assets/css/styles.css: 3 columns, 2 under 1024px,
# 1 under 640px.
SIZES = "(max-width: 640px) 92vw, (max-width: 1024px) 44vw, 30vw"
SIZES_DETAIL = "(max-width: 640px) 60vw, 220px"


def basename(book):
    """Image basename for a book dict, without extension."""
    if book.get("home") == "researchmadepractical.com":
        return "rmp-" + book["slug"]
    return book["slug"]


def exists(book):
    b = basename(book)
    return all((IMG_DIR / ("%s%s%s" % (b, suffix, ext))).exists()
               for _, suffix in WIDTHS for ext in (".jpg", ".webp"))


def missing(books):
    """Slugs whose four variants are not all present."""
    return [b["slug"] for b in books if not exists(b)]


def _srcset(base, ext):
    return ", ".join("%s/%s%s%s %dw" % (IMG_URL, base, suffix, ext, w)
                     for w, suffix in WIDTHS)


def picture(book, sizes=SIZES, css="cover", lazy=True, detail=False):
    """The <picture> for one book. Returns "" when the cover is absent, so a
    build run with --allow-missing-covers degrades to the old text-only card
    rather than emitting a broken image."""
    if not exists(book):
        return ""
    base = basename(book)
    alt = "Cover of %s" % html.escape(book["title"], quote=True)
    w, h = (938, 1500)
    img = (
        '<img class="%s" src="%s/%s-600.jpg" srcset="%s" sizes="%s" '
        'width="%d" height="%d" %sdecoding="async" alt="%s">'
        % (css, IMG_URL, base, _srcset(base, ".jpg"), sizes, w, h,
           'loading="lazy" ' if lazy else "", alt)
    )
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s">%s</picture>'
            % (_srcset(base, ".webp"), sizes, img))


def card_cover(book, href, external=False):
    """Cover for a grid card, linked to the same place as the card title.

    The anchor is aria-hidden with tabindex=-1: the title immediately below is
    the same link, and without this every book would present twice to a screen
    reader. Sighted users still get a clickable cover.
    """
    pic = picture(book)
    if not pic:
        return ""
    rel = ' target="_blank" rel="noopener"' if external else ""
    return ('        <a class="cover-link" href="%s"%s tabindex="-1" aria-hidden="true">%s</a>\n'
            % (href, rel, pic))
