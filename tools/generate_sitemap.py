#!/usr/bin/env python3
import os
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = os.environ.get("SITE_DOMAIN", "https://YOUR-DOMAIN/").rstrip("/") + "/"
pages = []
for p in ROOT.rglob("*.html"):
    if ".github" in p.parts or "node_modules" in p.parts:
        continue
    pages.append(p.relative_to(ROOT).as_posix())

def loc_for(relpath: str) -> str:
    return DOMAIN if relpath == "index.html" else urljoin(DOMAIN, relpath)

urlset = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for rel in sorted(pages):
    urlset.append("  <url>")
    urlset.append(f"    <loc>{loc}</loc>".format(loc=loc_for(rel)))
    urlset.append("  </url>")
urlset.append("</urlset>\n")
(Path(ROOT) / "sitemap.xml").write_text("\n".join(urlset), encoding="utf-8")
print("Generated sitemap.xml with", len(pages), "URLs")
