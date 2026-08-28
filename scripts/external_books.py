# -*- coding: utf-8 -*-
"""
external_books.py - the eighteen books catalogued on the other two sites.

These are NOT described in full here. Each gets a short card that links out to
its canonical page:

    Mastering Research (9)       -> gradsummit.com/books/<slug>/
    Research Made Practical (9)  -> researchmadepractical.com/<slug>

That is the whole reason this site can exist alongside those two. Nine near-copies
of gradsummit's book pages used to live here, self-canonicalising, competing with
longer originals on a site with far more authority. Replacing them with cards that
point home removes the competition and keeps every book reachable.

Titles and subtitles are read from the sibling repositories at build time rather
than retyped, so they cannot drift. Two of the workbook titles were wrong on their
own site until 2026-08-28, when they were corrected against the published Amazon
listings; a hand-maintained third copy here would have preserved the error.
"""

import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRADSUMMIT = Path(os.environ.get("GRADSUMMIT_REPO", REPO.parent / "gradsummit"))
RMP = Path(os.environ.get("RMP_REPO", REPO.parent / "research-made-practical"))

SERIES_MASTERING = "Mastering Research"
SERIES_PRACTICAL = "Research Made Practical Workbooks"

# Which shelf each book belongs on in the library. Keyed by slug so a renamed
# file fails loudly in build_site.py rather than silently landing in "other".
STAGES = {
    # Mastering Research
    "phd-journey-simplified": ["plan"],
    "research-design-simplified": ["plan"],
    "research-proposal-writing-simplified": ["plan"],
    "literature-review-simplified-2e": ["evidence"],
    "literature-review-simplified-1e": ["evidence"],
    "dissertation-literature-review-sprint": ["evidence"],
    "qda-with-chatgpt-and-qualcoder": ["analysis"],
    "ai-powered-scholar": ["plan", "writing"],
    "write-and-publish-scientific-paper": ["writing"],
    # Research Made Practical workbooks
    "dissertation": ["plan"],
    "statistical-test": ["analysis"],
    "qualitative": ["analysis"],
    "systematic-review": ["evidence"],
    "academic-writing": ["writing"],
    "interview": ["fieldwork"],
    "mixed-methods": ["plan", "analysis"],
    "grant-writing": ["plan"],
    "data-collection": ["fieldwork"],
}


def _text(pattern, source, default=""):
    m = re.search(pattern, source, re.S)
    if not m:
        return default
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def _read(page, title_pat, sub_pat, buy_pat):
    s = page.read_text(encoding="utf-8", errors="ignore")
    isbn = re.search(buy_pat, s)
    return _text(title_pat, s), _text(sub_pat, s), (isbn.group(1) if isbn else None)


def load():
    """Every external book, or a clear failure if a repo is missing."""
    books = []

    if not GRADSUMMIT.is_dir():
        raise SystemExit("gradsummit repo not found: %s (set GRADSUMMIT_REPO)" % GRADSUMMIT)
    for page in sorted((GRADSUMMIT / "books").glob("*.html")):
        if page.stem == "index":
            continue
        title, sub, isbn = _read(
            page, r"<h1[^>]*>(.*?)</h1>", r'class="sub"[^>]*>(.*?)</div>',
            r"go/book/([0-9A-Z]+)")
        books.append({
            "slug": page.stem,
            "series": SERIES_MASTERING,
            "title": title,
            "tagline": sub,
            "isbn": isbn,
            "canonical": "https://www.gradsummit.com/books/%s/" % page.stem,
            "home": "gradsummit.com",
            "stages": STAGES.get(page.stem, []),
        })

    if not RMP.is_dir():
        raise SystemExit("research-made-practical repo not found: %s (set RMP_REPO)" % RMP)
    for page in sorted(RMP.glob("*.html")):
        if page.stem == "index":
            continue
        title, sub, isbn = _read(
            page, r"<h1[^>]*>(.*?)</h1>", r'name="description" content="([^"]*)"',
            r"amazon\.com/dp/([0-9A-Z]+)")
        books.append({
            "slug": page.stem,
            "series": SERIES_PRACTICAL,
            "title": title,
            "tagline": sub,
            "isbn": isbn,
            "canonical": "https://researchmadepractical.com/%s" % page.stem,
            "home": "researchmadepractical.com",
            "stages": STAGES.get(page.stem, []),
        })

    missing = [b["slug"] for b in books if not b["stages"]]
    if missing:
        raise SystemExit(
            "no shelf assigned for: %s\nAdd them to STAGES in external_books.py."
            % ", ".join(missing))
    unnamed = [b["slug"] for b in books if not b["title"]]
    if unnamed:
        raise SystemExit("could not read a title for: %s" % ", ".join(unnamed))
    return books
