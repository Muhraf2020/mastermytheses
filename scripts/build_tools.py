#!/usr/bin/env python3
"""
build_tools.py - render the clinical tools and their hub.

Pages are written to tools/<slug>.html plus tools/index.html, using the same
head(), NAV and FOOTER as the rest of the site so a tool is not a visually
separate island.

Everything is self-contained: the calculation is inlined, so a tool page has no
script that can 404 and nothing to load before it can compute.

Validation runs before anything is written, because the failure that matters
here is silent. A widget that references an element it does not contain looks
fine and does nothing when clicked, and that is exactly the bug that shipped
during the phdjourneysimplified port before a check like this existed.

    python scripts/build_tools.py            # write
    python scripts/build_tools.py --check    # validate only
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_site as B          # noqa: E402
from tool_content import TOOLS, STATS_JS   # noqa: E402

REPO = B.REPO
OUT = REPO / "tools"

HUB_TITLE = "Clinical research tools"
HUB_DESC = ("Free calculators for clinical audit, evidence-based practice and "
            "diagnostic accuracy: PICO, NNT, sensitivity and specificity, audit "
            "sample size and run charts. No sign-up.")


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
ID_PATTERNS = [
    re.compile(r"getElementById\(\s*'([A-Za-z0-9_-]+)'\s*\)"),
    re.compile(r'getElementById\(\s*"([A-Za-z0-9_-]+)"\s*\)'),
]


def validate(books_by_slug):
    problems = []
    slugs = [t["slug"] for t in TOOLS]
    if len(set(slugs)) != len(slugs):
        problems.append("duplicate tool slugs")

    for t in TOOLS:
        where = t["slug"]

        # every element the script reaches for must exist in the widget
        present = set(re.findall(r'id="([A-Za-z0-9_-]+)"', t["widget"]))
        wanted = set()
        for pat in ID_PATTERNS:
            wanted |= set(pat.findall(t["script"]))
        # ids the script creates at run time live in the output container
        missing = wanted - present - {"out"}
        if missing:
            problems.append("%s: script uses ids absent from the widget: %s"
                            % (where, ", ".join(sorted(missing))))
        if "out" not in present:
            problems.append("%s: widget has no #out container" % where)

        # the book it sells must exist
        if t["book"] not in books_by_slug:
            problems.append("%s: unknown book slug %r" % (where, t["book"]))

        # related tools must exist
        for rel, _ in t["related"]:
            if rel not in slugs:
                problems.append("%s: related tool %r does not exist" % (where, rel))

        for field in ("title", "description", "h1", "standfirst"):
            if not t.get(field, "").strip():
                problems.append("%s: empty %s" % (where, field))
        if len(t["faq"]) < 3:
            problems.append("%s: fewer than 3 FAQ entries" % where)

        # nothing may point at the sibling sites' tools
        for host in ("gradsummit.com/tools", "phdjourneysimplified.com/tools"):
            if host in t["widget"] + t["script"] + t["explainer"][1]:
                problems.append("%s: links to %s" % (where, host))
    return problems


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def book_cta(book):
    """The book this tool belongs to, as the page's one commercial ask."""
    return """
  <section class="card book-cta">
    <div class="book-cta-cover">{cover}</div>
    <div>
      <p class="eyebrow">The book behind this tool</p>
      <h2 style="font-size:1.15rem;margin:.2rem 0 .4rem"><a href="/books/{slug}.html">{title}</a></h2>
      <p class="sub">{tagline}</p>
      <div class="actions">
        <a class="btn secondary" href="/books/{slug}.html">What&rsquo;s inside</a>
        <a class="btn" href="{buy}" target="_blank" rel="noopener nofollow sponsored">Get it on Amazon</a>
      </div>
    </div>
  </section>""".format(
        cover=B.covers.picture(book, sizes="120px", css="cover", lazy=True),
        slug=book["slug"], title=html.escape(book["title"]),
        tagline=html.escape(book["tagline"]), buy=B.BUY % book["asin"])


def render_tool(t, books_by_slug):
    book = books_by_slug[t["book"]]
    url = "%s/tools/%s.html" % (B.SITE, t["slug"])

    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication",
         "name": t["h1"], "url": url, "applicationCategory": "HealthApplication",
         "operatingSystem": "Any browser",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "author": {"@type": "Person", "name": B.AUTHOR},
         "description": t["description"]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in t["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": B.SITE},
             {"@type": "ListItem", "position": 2, "name": HUB_TITLE,
              "item": "%s/tools/" % B.SITE},
             {"@type": "ListItem", "position": 3, "name": t["h1"], "item": url}]},
    ]

    faq = "\n".join(
        '    <details><summary>%s</summary><p>%s</p></details>'
        % (html.escape(q), html.escape(a)) for q, a in t["faq"])

    related = "\n".join(
        '      <a class="btn secondary" href="/tools/%s.html">%s</a>'
        % (slug, html.escape(label)) for slug, label in t["related"])

    heading, body = t["explainer"]

    return B.head(t["title"], t["description"], "/tools/%s.html" % t["slug"], ld) + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo;
    <a href="/tools/">Tools</a> &rsaquo; <span>{h1}</span></div>

  <h1 class="title" style="font-size:1.9rem;margin:1rem 0 .4rem">{h1}</h1>
  <p class="sub" style="max-width:72ch">{standfirst}</p>

  <section class="card tool" id="tool">{widget}
  </section>

  <section class="card inside">
    <h2>{heading}</h2>
{body}
  </section>

  <section class="card faq" id="faq">
    <h2>Frequently asked questions</h2>
{faq}
  </section>
{cta}

  <div class="hr"></div>
  <div class="bottom-nav">
{related}
      <a class="btn secondary" href="/tools/">All tools</a>
  </div>
</main>

{footer}
<script>
{stats}{script}
</script>
</body>
</html>
""".format(h1=html.escape(t["h1"]), standfirst=html.escape(t["standfirst"]),
           widget=t["widget"].rstrip(), heading=html.escape(heading),
           body=body.rstrip(), faq=faq, related=related,
           cta=book_cta(book), footer=B.FOOTER,
           stats=STATS_JS, script=t["script"])


def render_hub(books_by_slug):
    ld = [{"@context": "https://schema.org", "@type": "ItemList",
           "name": HUB_TITLE,
           "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "name": t["h1"],
                "url": "%s/tools/%s.html" % (B.SITE, t["slug"])}
               for i, t in enumerate(TOOLS)]}]

    cards = "\n".join("""      <article class="card">
        <div class="meta"><span class="badge">{badge}</span></div>
        <div class="title"><a style="text-decoration:none;color:inherit" href="/tools/{slug}.html">{h1}</a></div>
        <div class="sub">{standfirst}</div>
        <div class="actions"><a class="btn" href="/tools/{slug}.html">Open the tool</a></div>
      </article>""".format(
        badge=html.escape(books_by_slug[t["book"]]["short"]),
        slug=t["slug"], h1=html.escape(t["h1"]),
        standfirst=html.escape(t["standfirst"])) for t in TOOLS)

    return B.head("%s | Master My Theses" % HUB_TITLE, HUB_DESC, "/tools/", ld) + """
<main>
  <div class="breadcrumbs"><a href="/">The library</a> &rsaquo; <span>Tools</span></div>
  <h1 class="title" style="font-size:2rem;margin:1rem 0 .5rem">{title}</h1>
  <p class="sub" style="max-width:72ch">
    Free calculators for the arithmetic that comes up in clinical projects: framing an
    answerable question, sizing an audit, reading a diagnostic test, turning a trial
    result into a number a patient can use, and telling improvement from noise.
    Everything runs in your browser. Nothing is uploaded and nothing asks for an email.
  </p>
  <div class="hr"></div>

  <div class="grid grid-3">
{cards}
  </div>

  <div class="hr"></div>
  <div class="bottom-nav">
    <a class="btn secondary" href="/">The library</a>
    <a class="btn secondary" href="/choose.html">Which book do I need?</a>
  </div>
</main>

{footer}
</body>
</html>
""".format(title=html.escape(HUB_TITLE), cards=cards, footer=B.FOOTER)


def main():
    check_only = "--check" in sys.argv
    books = B.LOCAL_BOOKS + B.external_books.load()
    by_slug = {b["slug"]: b for b in books}

    problems = validate(by_slug)
    if problems:
        for p in problems:
            print("  FAIL %s" % p)
        raise SystemExit("\n%d validation problem(s); nothing written." % len(problems))
    print("  validation passed for %d tools" % len(TOOLS))

    pages = {"index.html": render_hub(by_slug)}
    for t in TOOLS:
        pages["%s.html" % t["slug"]] = render_tool(t, by_slug)

    if check_only:
        for name, content in sorted(pages.items()):
            print("  ok (not written) tools/%-34s %6d bytes" % (name, len(content.encode())))
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in sorted(pages.items()):
        (OUT / name).write_text(content, encoding="utf-8")
        print("  wrote tools/%-34s %6d bytes" % (name, len(content.encode())))


if __name__ == "__main__":
    main()
