#!/usr/bin/env python3
"""Checks every link on the portfolio and the first page of every hosted project.

Run from the repo root:  python3 tools/check_links.py [--local]
  default   reads the pages from the live site
  --local   reads the root pages from this checkout (links are still checked on the web)

Prints a Markdown report. Exit code 1 when something is broken, so a workflow can open an issue.
"Blocked" means the host refuses automated visitors (LinkedIn does); it is listed, not counted as broken.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://maryamjaberi.github.io/"
ROOT_PAGES = ["", "fa/", "case/dour.html", "case/wellbeing-check.html", "fa/case/dour.html", "fa/case/wellbeing-check.html", "cv.html"]
UA = "Mozilla/5.0 (portfolio link check; +https://maryamjaberi.github.io/)"
BLOCKED = {401, 403, 429, 999}          # the host answered, but not to a robot
SKIP = ("mailto:", "tel:", "data:", "javascript:", "#")
ATTR = re.compile(r'(?<![\w-])(?:href|src)="([^"]+)"')   # not data-src="…"


def fetch(url, want_body=False):
    """Returns (status, body). status 0 = no answer at all."""
    for attempt in range(2):
        try:
            req = urllib.request.Request(url.split("#")[0], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, (r.read().decode("utf-8", "replace") if want_body else "")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception:
            if attempt:
                return 0, ""
    return 0, ""


def links_in(html, page_url):
    found = set()
    for raw in ATTR.findall(html):
        if raw.startswith(SKIP) or "${" in raw or "{{" in raw:
            continue  # in-page anchors, mail links and JavaScript templates
        url = urllib.parse.urljoin(page_url, raw)
        if urllib.parse.urlparse(url).path in ("", "/") and "fonts.g" in url:
            continue  # <link rel=preconnect> to a font host is not a page
        found.add(url)
    return found


def main():
    local = "--local" in sys.argv
    projects = json.loads((ROOT / "assets/projects.json").read_text(encoding="utf-8"))
    pages = [SITE + p for p in ROOT_PAGES] + [p["url"] for p in projects if p["url"]]
    where = {}       # link -> pages that carry it
    dead_pages = []
    for page in dict.fromkeys(pages):
        rel = page[len(SITE):]
        if local and (rel in ROOT_PAGES):
            f = ROOT / (rel + "index.html" if rel.endswith("/") or rel == "" else rel)
            status, html = 200, f.read_text(encoding="utf-8")
        else:
            status, html = fetch(page, want_body=True)
        if status != 200:
            dead_pages.append((status, page))
            continue
        for url in links_in(html, page):
            where.setdefault(url, []).append(rel or "/")
    with ThreadPoolExecutor(10) as ex:
        results = dict(zip(where, ex.map(lambda u: fetch(u)[0], where)))
    broken = sorted((s, u) for u, s in results.items() if s != 200 and s not in BLOCKED)
    blocked = sorted((s, u) for u, s in results.items() if s in BLOCKED)
    print(f"Checked {len(pages)} pages and {len(results)} links.\n")
    if dead_pages or broken:
        print("## Broken\n")
        for s, u in dead_pages:
            print(f"- `{s or 'no answer'}` page {u}")
        for s, u in broken:
            print(f"- `{s or 'no answer'}` {u} (on: {', '.join(sorted(set(where[u])))})")
        print()
    if blocked:
        print("## Blocked to robots (open these by hand once in a while)\n")
        for s, u in blocked:
            print(f"- `{s}` {u}")
        print()
    if not (dead_pages or broken):
        print("Everything that can be checked answers 200.")
    return 1 if (dead_pages or broken) else 0


if __name__ == "__main__":
    sys.exit(main())
