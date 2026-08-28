#!/usr/bin/env python3
"""
build_site.py - generate mastermytheses.com: the complete 26-book library.

WHAT THIS SITE IS FOR
---------------------
Until 2026-08-28 this domain held nine book pages that were shorter, older,
self-canonicalising copies of pages on gradsummit.com. Two sites, one owner, the
same nine books, the same slugs, both claiming to be the original. It had no
inbound links and did not appear in search, which is the outcome that arrangement
earns.

It now does something neither other site does:

  * It is the ONLY place all 26 books exist together, across four series.
  * It is the ONLY home for 8 of them. The Clinical Practice & Applied Research
    workbooks (5) and Healthcare Research Simplified (3) had no web presence
    anywhere before this. Those pages are wholly original content.
  * The 18 books catalogued elsewhere get short cards linking to their canonical
    pages. No description is duplicated.
  * The library shelving, the chooser and the reading pathways are original
    editorial content that exists nowhere else.

The two clinical series also serve a different reader — clinicians rather than
generic graduate researchers — with a different search vocabulary (clinical
audit, EBP project, CARE, SPIRIT, CFIR). That is the second reason these pages
cannot cannibalise the other two sites.

    python scripts/build_site.py [--check]
"""

import argparse
import html

import covers
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import external_books  # noqa: E402
from local_books import LOCAL_BOOKS  # noqa: E402
from navigation import CHOOSER, PATHWAYS  # noqa: E402
from book_detail import DETAIL  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SITE = "https://www.mastermytheses.com"
AUTHOR = "Rafiq Muhammad, MD, MIHMEP, PhD"
BUY = "https://www.amazon.com/dp/%s"

SHELVES = [
    ("plan", "Plan and design the study",
     "Framing the question, choosing a design, and writing the proposal or protocol."),
    ("evidence", "Literature and evidence synthesis",
     "Searching, screening, appraising and synthesising what is already known."),
    ("fieldwork", "Data collection and fieldwork",
     "Instruments, interviews, recruitment and the management of the data you gather."),
    ("analysis", "Analysis",
     "Choosing and running the right analysis, qualitative or quantitative."),
    ("writing", "Writing and publishing",
     "Turning finished work into a chapter, a manuscript, and a publication."),
    ("clinical", "Clinical practice projects",
     "Audit, quality improvement, evidence-based practice and implementation, for clinicians."),
]

NAV = """  <header class="site">
    <div class="wrap">
      <div class="brand"><a href="/" style="color:inherit;text-decoration:none">Master My Theses</a></div>
      <nav aria-label="Primary">
        <a href="/">The library</a>
        <a href="/choose.html">Which book?</a>
        <a href="/pathways.html">Pathways</a>
        <a href="/about.html">About</a>
      </nav>
    </div>
  </header>"""

FOOTER = """<footer>
  <div class="site-footer-inner">
    <div class="site-footer-copy">&copy; <span class="footer-year"></span> Rafiq Muhammad, PhD. All rights reserved.</div>
    <nav class="site-footer-links" aria-label="Footer">
      <a href="/">The library</a>
      <a href="/choose.html">Which book?</a>
      <a href="/pathways.html">Pathways</a>
      <a href="https://www.gradsummit.com/" rel="noopener">GradSummit</a>
      <a href="https://researchmadepractical.com/" rel="noopener">Research Made Practical</a>
    </nav>
  </div>
  <script>document.querySelectorAll('.footer-year').forEach(function (el) { el.textContent = new Date().getFullYear(); });</script>
</footer>"""


def head(title, description, path, extra_ld=None,
         robots="index, follow, max-snippet:-1, max-image-preview:large"):
    url = SITE + path
    e = lambda v: html.escape(v, quote=True)
    ld = "\n".join(
        '  <script type="application/ld+json">\n%s\n  </script>'
        % json.dumps(b, indent=2, ensure_ascii=False) for b in (extra_ld or []))
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="{author}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Master My Theses">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <link rel="manifest" href="/site.webmanifest">
{ld}
</head>
<body>
{nav}
""".format(t=e(title), d=e(description), url=url, author=e(AUTHOR), ld=ld, nav=NAV,
           robots=robots)


def card_external(b):
    """A pointer, not a description. The full page lives on the other site."""
    return """      <article class="card">
{cover}        <div class="meta"><span class="badge">{series}</span></div>
        <div class="title"><a style="text-decoration:none;color:inherit" href="{canonical}" target="_blank" rel="noopener">{title}</a></div>
        <div class="sub">{tagline}</div>
        <div class="actions">
          <a class="btn secondary" href="{canonical}" target="_blank" rel="noopener">Details on {home}</a>
          <a class="btn" href="{buy}" target="_blank" rel="noopener nofollow sponsored">Amazon</a>
        </div>
      </article>""".format(
        series=html.escape(b["series"]), canonical=b["canonical"],
        title=html.escape(b["title"]), tagline=html.escape(b["tagline"]),
        home=b["home"], buy=BUY % b["isbn"],
        cover=covers.card_cover(b, b["canonical"], external=True))


def card_local(b):
    t = "%d fill-in templates" % b["templates"] if b.get("templates") else "Step-by-step guide"
    return """      <article class="card">
{cover}        <div class="meta"><span class="badge">{series}</span><span class="badge">{t}</span></div>
        <div class="title"><a style="text-decoration:none;color:inherit" href="/books/{slug}.html">{title}</a></div>
        <div class="sub">{tagline}</div>
        <div class="actions">
          <a class="btn secondary" href="/books/{slug}.html">What&rsquo;s inside</a>
          <a class="btn" href="{buy}" target="_blank" rel="noopener nofollow sponsored">Amazon</a>
        </div>
      </article>""".format(
        series=html.escape(b["series"]), t=t, slug=b["slug"],
        title=html.escape(b["title"]), tagline=html.escape(b["tagline"]),
        buy=BUY % b["asin"],
        cover=covers.card_cover(b, "/books/%s.html" % b["slug"]))


def build_index(books):
    ld = [{
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": SITE + "/#organization",
             "name": "Master My Theses", "url": SITE + "/",
             "founder": {"@id": SITE + "/#author"}},
            {"@type": "Person", "@id": SITE + "/#author", "name": AUTHOR,
             "jobTitle": "Physician-researcher and author",
             "sameAs": ["https://www.gradsummit.com/about/",
                        "https://researchmadepractical.com/",
                        "https://phdjourneysimplified.com/"]},
            {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
             "name": "Master My Theses", "inLanguage": "en",
             "publisher": {"@id": SITE + "/#organization"}},
        ],
    }, {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "The complete research and clinical writing library",
        "numberOfItems": len(books),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "url": b.get("canonical") or "%s/books/%s.html" % (SITE, b["slug"]),
             "name": b["title"]}
            for i, b in enumerate(books)
        ],
    }]

    shelves_html = []
    for key, name, blurb in SHELVES:
        on_shelf = [b for b in books if key in b["stages"]]
        if not on_shelf:
            continue
        cards = "\n\n".join(
            card_local(b) if b.get("asin") else card_external(b) for b in on_shelf)
        shelves_html.append(
            '  <h2 id="{k}" style="margin:2.5rem 0 .3rem">{n}</h2>\n'
            '  <p class="sub" style="max-width:70ch;margin:0 0 1.2rem">{b}</p>\n'
            '  <section class="grid grid-3">\n{c}\n  </section>'.format(
                k=key, n=html.escape(name), b=html.escape(blurb), c=cards))

    series_counts = {}
    for b in books:
        series_counts[b["series"]] = series_counts.get(b["series"], 0) + 1
    series_list = "".join(
        "<li><strong>%s</strong> &mdash; %d book%s</li>"
        % (html.escape(s), n, "" if n == 1 else "s")
        for s, n in sorted(series_counts.items(), key=lambda x: -x[1]))

    return head(
        "The complete library — 26 research and clinical writing books",
        "Every book in the Mastering Research, Research Made Practical, Clinical "
        "Practice and Healthcare Research series, shelved by what you are trying to do.",
        "/", ld) + """
<main>
  <h1 class="title" style="font-size:2.1rem;margin:1rem 0 .5rem">The complete library</h1>
  <p class="sub" style="max-width:72ch">
    Twenty-six books across four series, by Rafiq Muhammad, MD, MIHMEP, PhD &mdash;
    shelved by what you are actually trying to do rather than by which series they
    belong to. Some are guides you read; some are workbooks you fill in.
  </p>
  <ul class="feature-list" style="max-width:72ch">{series_list}</ul>
  <div class="bottom-nav">
    <a class="btn" href="/choose.html">Which book do I need?</a>
    <a class="btn secondary" href="/pathways.html">Reading pathways</a>
  </div>
  <div class="hr"></div>

{shelves}

  <div class="hr"></div>
  <section class="card inside">
    <h2>Where each book lives</h2>
    <p>
      The clinical and healthcare series are published here. The
      <strong>Mastering Research</strong> books are catalogued on
      <a href="https://www.gradsummit.com/books/" target="_blank" rel="noopener">GradSummit</a>,
      alongside free guides and tools, and the
      <strong>Research Made Practical</strong> workbooks on
      <a href="https://researchmadepractical.com/" target="_blank" rel="noopener">researchmadepractical.com</a>.
      This page is the one place the whole library appears together.
    </p>
  </section>
</main>

{footer}
</body>
</html>
""".format(series_list=series_list, shelves="\n\n".join(shelves_html), footer=FOOTER)


def build_book(b, siblings):
    url = "/books/%s.html" % b["slug"]
    ld = [{
        "@context": "https://schema.org",
        "@type": "Book",
        "name": b["title"],
        "description": b["tagline"],
        "author": {"@type": "Person", "name": AUTHOR, "@id": SITE + "/#author"},
        "inLanguage": "en",
        "url": SITE + url,
        "isbn": b.get("paperback_isbn") or None,
        "sameAs": BUY % b["asin"],
        "publisher": {"@type": "Organization", "name": "Research Made Practical"},
        "isPartOf": {"@type": "BookSeries", "name": b["series"]},
    }, {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "The library", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": b["short"], "item": SITE + url},
        ],
    }]
    ld[0] = {k: v for k, v in ld[0].items() if v is not None}

    d = DETAIL.get(b["slug"])
    if not d:
        raise SystemExit(
            "%s has no entry in book_detail.py. A page without it runs to roughly 250 "
            "words, which is too thin to rank — the whole reason these eight books "
            "needed a home here." % b["slug"])

    # The FAQ is rendered once as <details> and once as FAQPage structured data,
    # from the same source, so the two cannot disagree.
    ld.append({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in d["faq"]
        ],
    })

    who = "\n".join("      <li>%s</li>" % html.escape(w) for w in d["who"])
    inside = "\n".join("      <li>%s</li>" % html.escape(i) for i in d["inside"])
    faq = "\n".join(
        '    <details>\n      <summary>%s</summary>\n      <p>%s</p>\n    </details>'
        % (html.escape(q), html.escape(a)) for q, a in d["faq"])

    outcomes = "\n".join("      <li>%s</li>" % html.escape(o) for o in b["outcomes"])
    frameworks = ", ".join(html.escape(f) for f in b["frameworks"])
    templates = ('<span class="badge">%d fill-in templates</span>' % b["templates"]
                 if b.get("templates") else "")
    others = [s for s in siblings if s["slug"] != b["slug"]][:3]
    related = "\n".join(
        '    <a class="btn secondary" href="/books/%s.html">%s</a>' % (s["slug"], html.escape(s["short"]))
        for s in others)

    return head(
        "%s | Master My Theses" % b["short"],
        b["tagline"], url, ld) + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo; <span>{short}</span></div>

  <div class="book-hero">
    {detail_cover}
    <div class="book-hero-body">
      <h1 class="title" style="font-size:1.9rem;margin:1rem 0 .4rem">{title}</h1>
      <p class="sub" style="max-width:72ch">{tagline}</p>
      <div class="meta" style="margin:.6rem 0 1rem">
        <span class="badge">{series}</span>{templates}<span class="badge">{audience}</span>
      </div>

      <div class="actions">
        <a class="btn" href="{buy}" target="_blank" rel="noopener nofollow sponsored">Get it on Amazon</a>
      </div>
    </div>
  </div>

  <div class="hr"></div>

  <section class="card inside">
    <h2>The problem it solves</h2>
    <p>{problem}</p>
    <h2 style="margin-top:1.5rem">How it works</h2>
    <p>{approach}</p>
  </section>

  <section class="card inside" style="margin-top:1.25rem">
    <h2>Who it is for</h2>
    <ul class="feature-list">
{who}
    </ul>
    <p><strong>Who should look elsewhere.</strong> {not_for}</p>
  </section>

  <section class="card inside" style="margin-top:1.25rem">
    <h2>What is inside</h2>
    <ul class="feature-list">
{inside}
    </ul>
  </section>

  <section class="card inside" style="margin-top:1.25rem">
    <h2>What you will have finished</h2>
    <ul class="feature-list">
{outcomes}
    </ul>
  </section>

  <section class="card inside" style="margin-top:1.25rem">
    <h2>What this adds to the free guidance</h2>
    <p>{differs}</p>
    <p class="sub" style="margin-top:1rem">
      Built on {frameworks}. Original tools that operationalise the published
      standards and point to the free official sources.
    </p>
  </section>

  <section class="card faq" style="margin-top:1.5rem">
    <h2>Frequently asked questions</h2>
{faq}
  </section>

  <div class="hr"></div>
  <h2 style="margin:0 0 .8rem">Also in this series</h2>
  <div class="bottom-nav">
{related}
    <a class="btn secondary" href="/">The whole library</a>
  </div>
</main>

{footer}
</body>
</html>
""".format(short=html.escape(b["short"]), title=html.escape(b["title"]),
           tagline=html.escape(b["tagline"]), series=html.escape(b["series"]),
           templates=templates, audience=html.escape(b["audience"]),
           buy=BUY % b["asin"], problem=html.escape(b["problem"]),
           approach=html.escape(b["approach"]), outcomes=outcomes,
           who=who, not_for=html.escape(d["not_for"]), inside=inside,
           differs=html.escape(d["differs"]), faq=faq,
           frameworks=frameworks, related=related, footer=FOOTER,
           detail_cover=covers.picture(b, sizes=covers.SIZES_DETAIL,
                                       css="cover book-hero-cover", lazy=False))


def _by_slug(books):
    return {b["slug"]: b for b in books}


def _link(b):
    """A book link, pointing wherever that book actually lives."""
    href = b.get("canonical") or "/books/%s.html" % b["slug"]
    ext = ' target="_blank" rel="noopener"' if b.get("canonical") else ""
    return '<a href="%s"%s>%s</a>' % (href, ext, html.escape(b["title"]))


def _resolve(slugs, by, where):
    missing = [s for s in slugs if s not in by]
    if missing:
        raise SystemExit("%s references unknown book(s): %s" % (where, ", ".join(missing)))
    return [by[s] for s in slugs]


def build_books_index(books):
    """/books/ - every title once, grouped by series.

    Nothing on the site links here, but it is the URL people guess: it mirrors
    gradsummit.com/books/, and it is the natural parent of every
    /books/<slug>.html. Without an index.html, GitHub Pages serves the 404 page
    for the whole directory.

    It is noindex, follow. The homepage already lists these twenty-six books and
    targets the same query, so a second indexable page of the same titles would
    compete with it rather than add anything. Crawlers still follow the links
    out. tools/generate_sitemap.py already skips pages carrying noindex, so this
    stays out of the sitemap with no change needed there.

    The homepage groups books by the job they do and repeats a title across
    shelves. This lists each book exactly once, by series, which is what someone
    who typed /books/ is looking for.
    """
    seen, order, groups = set(), [], {}
    for b in books:
        if b["slug"] in seen:
            continue
        seen.add(b["slug"])
        series = b["series"]
        if series not in groups:
            groups[series] = []
            order.append(series)
        groups[series].append(b)

    sections = []
    for series in order:
        items = sorted(groups[series], key=lambda x: x["title"].lower())
        cards = "\n".join(
            card_external(b) if b.get("canonical") else card_local(b) for b in items)
        sections.append(
            '  <h2 style="font-size:1.25rem;margin:2rem 0 .15rem">%s</h2>\n'
            '  <p class="sub" style="margin:0 0 1rem">%d book%s</p>\n'
            '  <div class="grid grid-3">\n%s\n  </div>'
            % (html.escape(series), len(items), "" if len(items) == 1 else "s", cards))

    return head(
        "Every book | Master My Theses",
        "All %d books across four series: the doctoral guides, the Research Made "
        "Practical workbooks, the clinical practice workbooks and the healthcare "
        "research guides." % len(seen),
        "/books/",
        robots="noindex, follow") + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo; <span>Every book</span></div>
  <h1 class="title" style="font-size:2rem;margin:1rem 0 .5rem">Every book</h1>
  <p class="sub" style="max-width:72ch">
    All {n} titles, each listed once, grouped by series. If you would rather start
    from the problem you are stuck on, the <a href="/choose.html">chooser</a> maps
    situations to books, and the <a href="/pathways.html">pathways</a> put them in
    a reading order.
  </p>
  <div class="hr"></div>

{sections}

  <div class="hr"></div>
  <div class="bottom-nav">
    <a class="btn secondary" href="/">The library by topic</a>
    <a class="btn secondary" href="/choose.html">Which book do I need?</a>
    <a class="btn secondary" href="/pathways.html">Reading pathways</a>
  </div>
</main>

{footer}
</body>
</html>
""".format(n=len(seen), sections="\n\n".join(sections), footer=FOOTER)


def build_choose(books):
    by = _by_slug(books)
    rows = []
    for situation, advice, slugs in CHOOSER:
        picks = _resolve(slugs, by, "chooser")
        items = "".join("<li>%s</li>" % _link(b) for b in picks)
        rows.append(
            '  <section class="card inside" style="margin-bottom:1rem">\n'
            '    <h2 style="font-size:1.15rem">%s</h2>\n    <p>%s</p>\n'
            '    <ul class="feature-list">%s</ul>\n  </section>'
            % (html.escape(situation), html.escape(advice), items))

    return head(
        "Which research book do I need?",
        "Find the book by what you are stuck on: design, literature, interviews, coding, "
        "statistics, a proposal, an audit, an EBP project, or publication.",
        "/choose.html") + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo; <span>Which book?</span></div>
  <h1 class="title" style="font-size:2rem;margin:1rem 0 .5rem">Which book do I need?</h1>
  <p class="sub" style="max-width:72ch">
    Twenty-six books is too many to browse. Find the line below that sounds like your
    week and start there. Each answer names the one or two books that do that specific
    job &mdash; not the whole series.
  </p>
  <div class="hr"></div>

{rows}

  <div class="hr"></div>
  <div class="bottom-nav">
    <a class="btn secondary" href="/">Browse the whole library</a>
    <a class="btn secondary" href="/pathways.html">Reading pathways</a>
  </div>
</main>

{footer}
</body>
</html>
""".format(rows="\n\n".join(rows), footer=FOOTER)


def build_pathways(books):
    by = _by_slug(books)
    blocks = []
    for name, blurb, slugs in PATHWAYS:
        picks = _resolve(slugs, by, "pathway '%s'" % name)
        steps = "".join(
            "<li><strong>%d.</strong> %s</li>" % (i + 1, _link(b)) for i, b in enumerate(picks))
        blocks.append(
            '  <section class="card inside" style="margin-bottom:1rem">\n'
            '    <h2 style="font-size:1.2rem">%s</h2>\n    <p>%s</p>\n'
            '    <ol class="feature-list" style="list-style:none;padding-left:0">%s</ol>\n'
            '  </section>' % (html.escape(name), html.escape(blurb), steps))

    return head(
        "Reading pathways — which order to read them in",
        "Ordered reading tracks across the library: the doctorate start to finish, the "
        "clinician's first project, evidence synthesis, and first publication.",
        "/pathways.html") + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo; <span>Pathways</span></div>
  <h1 class="title" style="font-size:2rem;margin:1rem 0 .5rem">Reading pathways</h1>
  <p class="sub" style="max-width:72ch">
    Most of these books stand alone, but some are written to be read in sequence &mdash;
    the clinical series in particular, where each workbook assumes the one before it.
    These are the orders that work.
  </p>
  <div class="hr"></div>

{blocks}

  <div class="hr"></div>
  <div class="bottom-nav">
    <a class="btn secondary" href="/choose.html">Which book do I need?</a>
    <a class="btn secondary" href="/">Browse the whole library</a>
  </div>
</main>

{footer}
</body>
</html>
""".format(blocks="\n\n".join(blocks), footer=FOOTER)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--allow-missing-covers", action="store_true",
                    help="build even though some books have no cover image; "
                         "their cards fall back to text only")
    args = ap.parse_args()

    ext = external_books.load()
    books = LOCAL_BOOKS + ext
    print("library: %d books (%d published here, %d linked out)"
          % (len(books), len(LOCAL_BOOKS), len(ext)))

    # A grid where some cards carry a cover and others do not reads as broken,
    # so a missing cover stops the build rather than shipping quietly.
    absent = covers.missing(books)
    if absent:
        print("covers: %d of %d present, missing:" % (len(books) - len(absent), len(books)))
        for slug in absent:
            print("  %s" % slug)
        if not args.allow_missing_covers:
            raise SystemExit(
                "Refusing to build. Add the covers (see incoming-covers/README.md, "
                "then run tools/import_clinical_covers.py), or pass "
                "--allow-missing-covers to build text-only cards for these.")
    else:
        print("covers: all %d present" % len(books))

    pages = {
        "index.html": build_index(books),
        "books/index.html": build_books_index(books),
        "choose.html": build_choose(books),
        "pathways.html": build_pathways(books),
    }
    for b in LOCAL_BOOKS:
        siblings = [s for s in LOCAL_BOOKS if s["series"] == b["series"]]
        pages["books/%s.html" % b["slug"]] = build_book(b, siblings)

    if args.check:
        for name, content in sorted(pages.items()):
            print("  ok (not written) %-52s %6d bytes" % (name, len(content.encode())))
        return

    # The nine duplicated book pages come down — that is the point of the rebuild —
    # but their URLs are in the live sitemap and may be linked or bookmarked, so
    # they are replaced with redirect stubs rather than deleted outright.
    #
    # GitHub Pages cannot issue a 301, so each stub carries a canonical pointing at
    # the book's real home plus a meta refresh. The canonical is what matters: it
    # tells a crawler the content moved and consolidates any accumulated signal onto
    # gradsummit, instead of leaving nine 404s behind.
    local_slugs = {b["slug"] for b in LOCAL_BOOKS}
    ext_by_slug = {b["slug"]: b for b in ext}
    stubs = 0
    for old in sorted((REPO / "books").glob("*.html")):
        # books/index.html is the directory listing this loop knows nothing
        # about; without this it would be treated as an unrecognised book and
        # deleted on every build.
        if old.name == "index.html":
            continue
        if old.stem in local_slugs:
            continue
        target = ext_by_slug.get(old.stem, {}).get("canonical")
        if not target:
            old.unlink()
            print("  removed %s (no canonical home found)" % old.name)
            continue
        old.write_text(
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<title>Moved — {t}</title>\n'
            '<link rel="canonical" href="{u}">\n'
            '<meta name="robots" content="noindex, follow">\n'
            '<meta http-equiv="refresh" content="0; url={u}">\n'
            '</head>\n<body>\n'
            '<p>This book is now catalogued at <a href="{u}">{u}</a>.</p>\n'
            '<script>location.replace("{u}");</script>\n'
            '</body>\n</html>\n'.format(t=html.escape(ext_by_slug[old.stem]["title"]), u=target),
            encoding="utf-8", newline="\n")
        stubs += 1
    if stubs:
        print("replaced %d duplicated page(s) with canonical redirect stubs" % stubs)

    for name, content in sorted(pages.items()):
        out = REPO / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8", newline="\n")
        print("  wrote %-52s %6d bytes" % (name, len(content.encode())))


if __name__ == "__main__":
    main()
