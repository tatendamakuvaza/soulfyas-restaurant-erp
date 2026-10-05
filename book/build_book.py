#!/usr/bin/env python3
"""
build_book.py — build the single-file HTML edition of the book.

Usage:    python3 build_book.py            (no third-party dependencies)

Reads manuscript/*.md and produces Big-Data-Analytics-and-Machine-Learning.html:
one self-contained file with the cover art embedded, a linked table of
contents, part dividers, styled chapters, and a stats colophon.
"""

import os
import re
import glob
import base64
import datetime
from html import escape as html_escape

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
MANUSCRIPT = os.path.join(ROOT, "manuscript")
OUTPUT = os.path.join(ROOT, "Practical-Data-Analysts-Handbook.html")
COVER = os.path.join(ROOT, "assets", "cover.jpg")

BOOK_TITLE = "The Practical Data Analyst's Handbook"
BOOK_SHORT = "The Practical Data Analyst's Handbook"
BOOK_SUBTITLE = ("From Zero to Your First Data Job — A Complete "
                 "Beginner's Course in Excel, SQL, Statistics, Python "
                 "and Power BI")
AUTHOR = "Tatenda Makuvaza"
AUTHOR_TAG = "Data Analyst &middot; Author &middot; Educator"
YEAR = "2026"

PARTS = [
    ("Part I",   "Beginning: You, the Data Analyst",              1,  5),
    ("Part II",  "Excel: Your First Superpower",                  6,  13),
    ("Part III", "SQL: The Language of Data",                     14, 21),
    ("Part IV",  "Statistics Without Fear",                       22, 29),
    ("Part V",   "Python: From Zero to Dangerous",                30, 37),
    ("Part VI",  "Dashboards and Storytelling with Power BI",     38, 43),
    ("Part VII", "Real Projects and Your Portfolio",              44, 49),
    ("Part VIII","Getting the Job",                               50, 56),
    ("Part IX",  "Beyond the Basics",                             57, 62),
]

# ---------------------------------------------------------------------------
# Markdown parsing — same subset as build_pdf.py
# ---------------------------------------------------------------------------

HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
UL_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
H_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")

def parse_blocks(md):
    lines = md.replace("\r\n", "\n").split("\n")
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line, s = lines[i], lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip())
                i += 1
            i += 1
            blocks.append(("code", s[3:].strip(), buf))
            continue
        m = H_RE.match(s)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2)))
            i += 1
            continue
        if HR_RE.match(s):
            blocks.append(("hr",))
            i += 1
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                q = re.sub(r"^\s*>\s?", "", lines[i]).strip()
                if q:
                    buf.append(q)
                i += 1
            blocks.append(("quote", " ".join(buf)))
            continue
        if s.startswith("|") and i + 1 < n and SEP_RE.match(lines[i + 1]):
            header = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append(("table", header, rows))
            continue
        m = UL_RE.match(line)
        if m:
            items = []
            while i < n:
                mm = UL_RE.match(lines[i])
                if not mm:
                    break
                items.append((len(mm.group(1)) // 2, mm.group(2).strip()))
                i += 1
            blocks.append(("ul", items))
            continue
        m = OL_RE.match(line)
        if m:
            items = []
            while i < n:
                mm = OL_RE.match(lines[i])
                if not mm:
                    break
                items.append((len(mm.group(1)) // 2, mm.group(3).strip()))
                i += 1
            blocks.append(("ol", items))
            continue
        buf = [s]
        i += 1
        while i < n:
            nxt, ns = lines[i], lines[i].strip()
            if (not ns or ns.startswith(("#", "```", ">", "|"))
                    or HR_RE.match(ns) or UL_RE.match(nxt) or OL_RE.match(nxt)):
                break
            buf.append(ns)
            i += 1
        blocks.append(("p", " ".join(buf)))
    return blocks

def inline(text):
    t = html_escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"<em>\1</em>", t)
    return t

def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:70]

# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def render_blocks(md):
    out = []
    toc = []
    blocks = parse_blocks(md)
    open_list = None

    def close_list():
        nonlocal open_list
        if open_list:
            out.append("</%s>" % open_list)
            open_list = None

    for blk in blocks:
        kind = blk[0]
        if kind == "h":
            _, level, text = blk
            close_list()
            if level == 1:
                anchor = slug(text)
                toc.append(text)
                out.append('<h1 id="%s">%s</h1>' % (anchor, inline(text)))
            else:
                out.append("<h%d>%s</h%d>" % (level, inline(text), level))
        elif kind == "p":
            close_list()
            out.append("<p>%s</p>" % inline(blk[1]))
        elif kind == "quote":
            close_list()
            out.append("<blockquote>%s</blockquote>" % inline(blk[1]))
        elif kind == "hr":
            close_list()
            out.append("<hr>")
        elif kind == "code":
            close_list()
            body = html_escape("\n".join(blk[2]))
            out.append("<pre><code>%s</code></pre>" % body)
        elif kind == "table":
            close_list()
            _, header, rows = blk
            t = ["<table><thead><tr>"]
            t.extend("<th>%s</th>" % inline(h) for h in header)
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>")
                t.extend("<td>%s</td>" % inline(c)
                         for c in (r + [""] * (len(header) - len(r)))[:len(header)])
                t.append("</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
        elif kind in ("ul", "ol"):
            _, items = blk
            want = "ul" if kind == "ul" else "ol"
            if open_list != want:
                close_list()
                out.append("<%s>" % want)
                open_list = want
            for idx, (level, text) in enumerate(items, 1):
                marker = ("%d." % idx) if (kind == "ol" and level == 0) else None
                if level == 0:
                    out.append("<li>%s</li>" % inline(text))
                else:
                    out.append('<li class="sub">%s</li>' % inline(text))
    close_list()
    return "\n".join(out), toc

CSS = """
:root { --navy:#0b2545; --navy2:#13315c; --gold:#c9a227; --ink:#1f2933;
        --slate:#5d6b7a; --cream:#fdf8ec; --codebg:#f4f6f9; --zebra:#f4f2ea; }
* { box-sizing: border-box; }
body { margin:0; font-family: Georgia, 'Times New Roman', serif; color: var(--ink);
       background:#eef1f5; line-height:1.62; font-size:17px; }
.page { max-width: 760px; margin: 0 auto; background:#fff; padding: 48px 56px;
        box-shadow: 0 0 24px rgba(11,37,69,.12); }
h1 { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: var(--navy);
     font-size: 1.9em; line-height:1.25; margin: 0 0 6px; border-bottom: 3px solid var(--gold);
     padding-bottom: 10px; }
h2 { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: var(--navy);
     font-size: 1.28em; margin-top: 1.6em; }
h3 { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: var(--navy2);
     font-size: 1.08em; margin-top: 1.3em; }
h4 { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: var(--slate);
     font-size: .98em; margin-top: 1.1em; }
p { margin: .7em 0; text-align: justify; }
a { color: #0b6e8f; }
blockquote { background: var(--cream); border-left: 4px solid var(--gold);
             margin: 1em 0; padding: 10px 18px; font-style: italic; color:#4a4433; }
code { font-family: 'DejaVu Sans Mono', Consolas, monospace; font-size: .85em;
       background: var(--codebg); color:#13315c; padding: 1px 5px; border-radius:4px; }
pre { background: var(--codebg); border-left: 4px solid var(--navy); padding: 12px 16px;
      overflow-x: auto; line-height: 1.45; }
pre code { background: none; padding: 0; font-size: .82em; color: var(--ink); }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .88em; }
th { background: var(--navy); color: #fff; font-family: 'Segoe UI', sans-serif;
     text-align: left; padding: 7px 9px; }
td { border: 1px solid #e2e0d6; padding: 6px 9px; vertical-align: top; }
tbody tr:nth-child(even) { background: var(--zebra); }
ul, ol { padding-left: 26px; }
li.sub { list-style-type: '–  '; margin-left: 18px; }
hr { border: none; border-top: 1px solid #e2e0d6; margin: 1.6em 0; }
.cover { position: relative; margin: -48px -56px 34px; height: 78vh; min-height: 480px;
         background: #071630 center/cover no-repeat; display:flex; flex-direction:column;
         align-items:center; justify-content:center; text-align:center; }
.cover .scrim { position:absolute; inset:0; background: rgba(7,22,48,.66); }
.cover .inner { position:relative; color:#fff; padding: 0 30px; }
.cover .kicker { letter-spacing: .35em; font-size: .75em; color:#e8d9a0;
                 font-family:'Segoe UI', sans-serif; }
.cover .title { font-family:'Segoe UI', Helvetica, Arial, sans-serif; font-weight:800;
                font-size: 2.7em; line-height:1.15; margin:.35em 0 .1em; }
.cover .title .amp { color: var(--gold); }
.cover .subtitle { color:#d7e3f4; font-size: 1.02em; max-width: 540px; margin: 1.1em auto 0; }
.cover .rule { width: 90px; height: 3px; background: var(--gold); margin: 1.6em auto; }
.cover .author { font-style: italic; font-size: 1.5em; }
.cover .tag { color:#e8d9a0; font-size:.95em; font-family:'Segoe UI', sans-serif; }
.cover .edition { position:absolute; bottom:22px; left:0; right:0; color:#9fb3d1;
                  font-size:.8em; font-family:'Segoe UI', sans-serif; }
.divider { text-align:center; margin: 70px 0 50px; padding: 40px 0;
           border-top: 2px solid var(--gold); border-bottom: 2px solid var(--gold); }
.divider .label { letter-spacing:.3em; color:#8a6d1c; font-weight:700;
                  font-family:'Segoe UI', sans-serif; font-size:.85em; }
.divider .name { font-family:'Segoe UI', Helvetica, Arial, sans-serif; font-weight:800;
                 color: var(--navy); font-size:1.6em; margin:.4em 0; }
.divider .range { color: var(--slate); font-family:'Segoe UI', sans-serif; font-size:.9em; }
.toc-page { margin-top: 40px; }
.toc-page h1 { border-bottom: none; }
.toc-page .part { font-weight: 700; font-family:'Segoe UI', sans-serif;
                  color: var(--navy); margin: 18px 0 4px; font-size: 1.02em; }
.toc-page a { color: var(--ink); text-decoration: none; }
.toc-page a:hover { color: #0b6e8f; text-decoration: underline; }
.toc-page .ch { display:block; padding: 2px 0 2px 18px; }
.colophon { margin-top: 60px; padding-top: 24px; border-top: 2px solid var(--gold);
            font-size: .92em; color: var(--slate); }
@media print {
  body { background:#fff; font-size: 11.5pt; }
  .page { box-shadow:none; max-width:none; padding: 0; }
  .cover { height: 90vh; margin: 0; }
  a { color: var(--ink); text-decoration: none; }
}
"""

def cover_html():
    bg = ""
    if os.path.exists(COVER):
        with open(COVER, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        bg = "background-image:url(data:image/jpeg;base64,%s);" % b64
    return """
<section class="cover" style="%s">
  <div class="scrim"></div>
  <div class="inner">
    <div class="kicker">A COMPLETE BEGINNER'S COURSE</div>
    <div class="title">The Practical<br><span class="amp">Data Analyst's Handbook</span></div>
    <div class="subtitle">%s</div>
    <div class="rule"></div>
    <div class="author">%s</div>
    <div class="tag">"%s"</div>
  </div>
  <div class="edition">First Edition &middot; %s</div>
</section>
""" % (bg, html_escape(BOOK_SUBTITLE), html_escape(AUTHOR),
       html_escape(AUTHOR_TAG), YEAR)

def load_manuscript():
    docs = []
    front = os.path.join(MANUSCRIPT, "00-front-matter.md")
    if os.path.exists(front):
        docs.append(("front", None, open(front, encoding="utf-8").read()))
    for path in sorted(glob.glob(os.path.join(MANUSCRIPT, "ch[0-9][0-9]-*.md"))):
        num = int(re.match(r"ch(\d+)-", os.path.basename(path)).group(1))
        docs.append(("ch", num, open(path, encoding="utf-8").read()))
    for path in sorted(glob.glob(os.path.join(MANUSCRIPT, "app-[a-z]-*.md"))):
        letter = re.match(r"app-([a-z])-", os.path.basename(path)).group(1)
        docs.append(("app", letter, open(path, encoding="utf-8").read()))
    return docs

def compute_stats(docs):
    words = code = 0
    for _, _, md in docs:
        in_code = False
        for ln in md.split("\n"):
            if ln.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                code += 1
            else:
                words += len(ln.split())
    chapters = sum(1 for k, _, _ in docs if k == "ch")
    apps = sum(1 for k, _, _ in docs if k == "app")
    return words, code, chapters, apps

def main():
    docs = load_manuscript()
    words, code_lines, chapters, apps = compute_stats(docs)
    est_pages = int(round(words / 300.0 + code_lines / 35.0 + 12))

    by_num = {key: md for kind, key, md in docs if kind == "ch"}
    front_md = next((md for k, _, md in docs if k == "front"), None)
    app_docs = [(l, md) for k, l, md in docs if k == "app"]

    # Table of contents
    toc_parts = []
    toc_lines = ['<nav class="toc-page"><h1>Table of Contents</h1><hr>']
    if front_md:
        toc_lines.append('<a class="ch" href="#front-matter">Front Matter</a>')

    def part_toc(name, entries):
        toc_lines.append('<div class="part">%s</div>' % html_escape(name))
        for e in entries:
            toc_lines.append('<a class="ch" href="#%s">%s</a>'
                             % (slug(e), html_escape(e)))

    for label, name, start, end in PARTS:
        entries = []
        for num in range(start, end + 1):
            md = by_num.get(num)
            if md:
                m = re.match(r"#\s+(.+)", md.strip())
                if m:
                    entries.append(m.group(1))
        if entries:
            part_toc("%s — %s" % (label, name), entries)
            toc_parts.append((label, name, start, end))
    if app_docs:
        toc_lines.append('<div class="part">Appendices</div>')
        for _, md in app_docs:
            m = re.match(r"#\s+(.+)", md.strip())
            if m:
                toc_lines.append('<a class="ch" href="#%s">%s</a>'
                                 % (slug(m.group(1)), html_escape(m.group(1))))
    toc_lines.append("</nav>")
    toc_html = "\n".join(toc_lines)

    # Body
    body = []
    if front_md:
        front_html, _ = render_blocks(
            front_md.replace("# Front Matter", "# Front Matter", 1))
        body.append('<section id="front-matter">%s</section>' % front_html)
        body.append('<div class="pagebreak" style="page-break-after:always;"></div>')

    for label, name, start, end in toc_parts:
        body.append('<div class="divider"><div class="label">%s</div>'
                    '<div class="name">%s</div>'
                    '<div class="range">Chapters %d &ndash; %d</div></div>'
                    % (label.upper(), html_escape(name), start, end))
        for num in range(start, end + 1):
            md = by_num.get(num)
            if md:
                html, _ = render_blocks(md)
                body.append(html)
                body.append('<div style="page-break-after:always;"></div>')

    if app_docs:
        body.append('<div class="divider"><div class="label">APPENDICES</div>'
                    '<div class="name">Reference Section</div>'
                    '<div class="range">Quick answers, cheat sheets, solutions '
                    'and practice data</div></div>')
        for _, md in app_docs:
            html, _ = render_blocks(md)
            body.append(html)
            body.append('<div style="page-break-after:always;"></div>')

    parts_present = len(toc_parts)
    today = datetime.date.today().strftime("%d %B %Y")
    colophon = """
<footer class="colophon">
<h3>About this Edition</h3>
<p><strong>%s &mdash; %s</strong> was generated directly from its Markdown
manuscript by build_book.py: one self-contained HTML file with the cover art
embedded, a linked table of contents, and print-friendly styles.</p>
<ul>
<li>Edition: First Edition, %s (compiled %s)</li>
<li>Contents: %d chapters in %d parts, plus %d appendices</li>
<li>Volume: approximately %s words of prose and %d lines of code
(estimated %d print pages)</li>
<li>Companion edition: print-ready PDF via build_pdf.py</li>
</ul>
<p>Thank you for reading this book &mdash; and for teaching from it.
The data is already pouring in somewhere near you.</p>
</footer>
""" % (html_escape(BOOK_TITLE), html_escape(BOOK_SUBTITLE), YEAR, today,
       chapters, parts_present, apps, "{:,}".format(words), code_lines, est_pages)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s &mdash; %s</title>
<style>%s</style>
</head>
<body>
<div class="page">
%s
%s
%s
%s
</div>
</body>
</html>
""" % (html_escape(BOOK_TITLE), html_escape(AUTHOR), CSS, cover_html(),
       toc_html, "\n".join(body), colophon)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(OUTPUT) / 1024.0
    print("Book built: %s" % OUTPUT)
    print("  chapters: %d   appendices: %d" % (chapters, apps))
    print("  prose words: %s   code lines: %d"
          % ("{:,}".format(words), code_lines))
    print("  estimated print pages: ~%d" % est_pages)
    print("  output size: %.1f KB" % size_kb)

if __name__ == "__main__":
    main()
