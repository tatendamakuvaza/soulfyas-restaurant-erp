#!/usr/bin/env python3
"""
build_pdf.py — typeset the manuscript into a print-ready PDF book.

Usage:    python3 build_pdf.py
Requires: pip install reportlab    (fonts are bundled in assets/fonts)

Reads manuscript/*.md (same order as build_book.py) and produces
Big-Data-Analytics-and-Machine-Learning.pdf: 7x10 inch textbook trim,
full-bleed cover, running headers, centred page numbers, a linked table of
contents with real page numbers, and PDF outline bookmarks.
"""

import os
import re
import glob
import datetime
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib.pagesizes import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle,
                                NextPageTemplate, XPreformatted)
from reportlab.platypus.tableofcontents import TableOfContents

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
MANUSCRIPT = os.path.join(ROOT, "manuscript")
OUTPUT = os.path.join(ROOT, "Practical-Data-Analysts-Handbook.pdf")
FONTS = os.path.join(ROOT, "assets", "fonts")
COVER = os.path.join(ROOT, "assets", "cover.jpg")

BOOK_TITLE = "The Practical Data Analyst's Handbook"
BOOK_SHORT = "The Practical Data Analyst's Handbook"
BOOK_SUBTITLE = ("From Zero to Your First Data Job — A Complete "
                 "Beginner's Course in Excel, SQL, Statistics, Python "
                 "and Power BI")
AUTHOR = "Tatenda Makuvaza"
AUTHOR_TAG = "The Big Data Analyst"
YEAR = "2026"

PAGE_W, PAGE_H = 7 * inch, 10 * inch
ML, MR, MT, MB = 0.68 * inch, 0.64 * inch, 0.68 * inch, 0.62 * inch
AVAIL = PAGE_W - ML - MR

NAVY = HexColor("#0b2545")
NAVY2 = HexColor("#13315c")
GOLD = HexColor("#c9a227")
INK = HexColor("#1f2933")
SLATE = HexColor("#5d6b7a")
CREAM = HexColor("#fdf8ec")
CODEBG = HexColor("#f4f6f9")
ZEBRA = HexColor("#f4f2ea")
GRID = HexColor("#e2e0d6")
GRAY = HexColor("#6b7280")

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
# Fonts
# ---------------------------------------------------------------------------

def register_fonts():
    specs = [
        ("Serif",   "DejaVuSerif.ttf",             "DejaVuSerif-Bold.ttf",
                    "DejaVuSerif-Italic.ttf",      "DejaVuSerif-BoldItalic.ttf"),
        ("Sans",    "DejaVuSans.ttf",              "DejaVuSans-Bold.ttf",
                    "DejaVuSans-Oblique.ttf",      "DejaVuSans-BoldOblique.ttf"),
        ("Mono",    "DejaVuSansMono.ttf",          "DejaVuSansMono-Bold.ttf",
                    "DejaVuSansMono.ttf",          "DejaVuSansMono-Bold.ttf"),
    ]
    for family, normal, bold, italic, bold_italic in specs:
        pdfmetrics.registerFont(TTFont(family, os.path.join(FONTS, normal)))
        pdfmetrics.registerFont(TTFont(family + "-B", os.path.join(FONTS, bold)))
        pdfmetrics.registerFont(TTFont(family + "-I", os.path.join(FONTS, italic)))
        pdfmetrics.registerFont(TTFont(family + "-BI", os.path.join(FONTS, bold_italic)))
        registerFontFamily(family, normal=family, bold=family + "-B",
                           italic=family + "-I", boldItalic=family + "-BI")

# ---------------------------------------------------------------------------
# Markdown parsing (blocks) — same subset as build_book.py
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

# ---------------------------------------------------------------------------
# Inline markdown -> ReportLab markup
# ---------------------------------------------------------------------------

def inline(text, code_size=7.9):
    t = xml_escape(text)
    stash = []

    def _stash(m):
        stash.append(m.group(1))
        return "\x00%d\x00" % (len(stash) - 1)

    t = re.sub(r"`([^`]+)`", _stash, t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               r'<a href="\2" color="#0b6e8f">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"<i>\1</i>", t)
    for j, code in enumerate(stash):
        t = t.replace("\x00%d\x00" % j,
                      '<font face="Mono" size="%.1f" color="#13315c">%s</font>'
                      % (code_size, code))
    return t

def wrap_code_lines(lines, width=88):
    import textwrap
    out = []
    for ln in lines:
        if len(ln) <= width:
            out.append(ln if ln.strip() else " ")
        else:
            out.extend(textwrap.wrap(ln, width=width, subsequent_indent="    ",
                                     break_long_words=True, break_on_hyphens=False)
                       or [" "])
    return out

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def build_styles():
    S = {}
    S["PartLine"] = ParagraphStyle("PartLine", fontName="Serif-I", fontSize=9.5,
                                   leading=13, textColor=SLATE, spaceAfter=12)
    S["ChapterTitle"] = ParagraphStyle("ChapterTitle", fontName="Sans-B", fontSize=17,
                                       leading=21.5, textColor=NAVY, spaceAfter=8,
                                       keepWithNext=1)
    S["PartTitle"] = ParagraphStyle("PartTitle", fontName="Sans-B", fontSize=21,
                                    leading=26, textColor=NAVY, alignment=TA_CENTER)
    S["H2"] = ParagraphStyle("H2", fontName="Sans-B", fontSize=11.8, leading=15,
                             textColor=NAVY, spaceBefore=13, spaceAfter=5,
                             keepWithNext=1)
    S["H3"] = ParagraphStyle("H3", fontName="Sans-B", fontSize=10.3, leading=13.2,
                             textColor=NAVY2, spaceBefore=9, spaceAfter=3.5,
                             keepWithNext=1)
    S["H4"] = ParagraphStyle("H4", fontName="Sans-B", fontSize=9.4, leading=12,
                             textColor=SLATE, spaceBefore=7, spaceAfter=2.5,
                             keepWithNext=1)
    S["Body"] = ParagraphStyle("Body", fontName="Serif", fontSize=9.4, leading=13.3,
                               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5)
    S["Quote"] = ParagraphStyle("Quote", fontName="Serif", fontSize=9.1, leading=12.8,
                                textColor=HexColor("#4a4433"), alignment=TA_LEFT)
    S["Bullet0"] = ParagraphStyle("Bullet0", parent=S["Body"], alignment=TA_LEFT,
                                  leftIndent=14, bulletIndent=3, spaceAfter=2.6,
                                  bulletFontName="Serif", bulletFontSize=9.4)
    S["Bullet1"] = ParagraphStyle("Bullet1", parent=S["Body"], alignment=TA_LEFT,
                                  leftIndent=26, bulletIndent=15, spaceAfter=2.6,
                                  bulletFontName="Serif", bulletFontSize=9.4)
    S["Cell"] = ParagraphStyle("Cell", fontName="Serif", fontSize=7.5, leading=9.8,
                               textColor=INK)
    S["CellHdr"] = ParagraphStyle("CellHdr", fontName="Sans-B", fontSize=7.3,
                                  leading=9.4, textColor=white)
    S["Code"] = ParagraphStyle("Code", fontName="Mono", fontSize=7.4, leading=10,
                               textColor=INK)
    S["Label"] = ParagraphStyle("Label", fontName="Sans-B", fontSize=9,
                                leading=12, textColor=HexColor("#8a6d1c"),
                                alignment=TA_CENTER)
    S["Range"] = ParagraphStyle("Range", fontName="Sans", fontSize=8.5, leading=11,
                                textColor=SLATE, alignment=TA_CENTER, spaceBefore=8)
    S["TOCTitle"] = ParagraphStyle("TOCTitle", fontName="Sans-B", fontSize=17,
                                   leading=21, textColor=NAVY, spaceAfter=14)
    return S

STYLES = None

# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------

def make_table(header, rows):
    data = [[Paragraph(inline(h, code_size=7.2), STYLES["CellHdr"]) for h in header]]
    for r in rows:
        data.append([Paragraph(inline(c, code_size=7.2), STYLES["Cell"])
                     for c in (r + [""] * (len(header) - len(r)))[:len(header)]])
    ncols = len(header)
    weights = []
    for j in range(ncols):
        cells = [header[j]] + [(r[j] if j < len(r) else "") for r in rows]
        weights.append(min(55, max(6, max(len(c) for c in cells))))
    total = float(sum(weights))
    colw = [AVAIL * w / total for w in weights]
    t = Table(data, colWidths=colw, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ZEBRA]),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]))
    return t

def make_code(lines):
    wrapped = wrap_code_lines(lines)
    data = [[XPreformatted(xml_escape(l), STYLES["Code"])] for l in wrapped]
    t = Table(data, colWidths=[AVAIL], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
    ]))
    return t

def make_quote(text):
    p = Paragraph(inline(text), STYLES["Quote"])
    t = Table([[p]], colWidths=[AVAIL], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6.5),
    ]))
    return t

def hr_flowable(color=GRID, thick=0.8, before=10, after=8):
    from reportlab.platypus import Flowable

    class HR(Flowable):
        def __init__(self):
            super().__init__()
            self.width = AVAIL
            self.height = before + after + thick

        def draw(self):
            self.canv.setStrokeColor(color)
            self.canv.setLineWidth(thick)
            self.canv.line(0, after, self.width, after)

    return HR()

def render_doc(md):
    story = []
    blocks = parse_blocks(md)
    for blk in blocks:
        kind = blk[0]
        if kind == "h":
            _, level, text = blk
            if level == 1:
                story.append(Paragraph(inline(text, code_size=12), STYLES["ChapterTitle"]))
                story.append(hr_flowable(GOLD, 1.6, before=2, after=10))
            elif level == 2:
                story.append(Paragraph(inline(text), STYLES["H2"]))
            elif level == 3:
                story.append(Paragraph(inline(text), STYLES["H3"]))
            else:
                story.append(Paragraph(inline(text), STYLES["H4"]))
        elif kind == "p":
            story.append(Paragraph(inline(blk[1]), STYLES["Body"]))
        elif kind == "quote":
            story.append(Spacer(1, 4))
            story.append(make_quote(blk[1]))
            story.append(Spacer(1, 6))
        elif kind == "hr":
            story.append(hr_flowable(GRID, 0.8, before=9, after=9))
        elif kind == "code":
            story.append(Spacer(1, 4))
            story.append(make_code(blk[2]))
            story.append(Spacer(1, 6))
        elif kind == "table":
            story.append(Spacer(1, 4))
            story.append(make_table(blk[1], blk[2]))
            story.append(Spacer(1, 6))
        elif kind in ("ul", "ol"):
            _, items = blk
            for idx, (level, text) in enumerate(items, 1):
                if kind == "ul":
                    style = STYLES["Bullet0" if level == 0 else "Bullet1"]
                    bullet = "\u2022" if level == 0 else "\u2013"
                else:
                    style = STYLES["Bullet0" if level == 0 else "Bullet1"]
                    bullet = "%d." % idx if level == 0 else "\u2013"
                story.append(Paragraph(inline(text), style, bulletText=bullet))
            story.append(Spacer(1, 3))
    return story

# ---------------------------------------------------------------------------
# Document template
# ---------------------------------------------------------------------------

def paint_footer(canv, doc):
    canv.saveState()
    canv.setFont("Sans", 8)
    canv.setFillColor(GRAY)
    canv.drawCentredString(PAGE_W / 2.0, MB - 18, str(canv.getPageNumber()))
    canv.restoreState()

def paint_content_end(canv, doc):
    if getattr(doc, "_chapter_start_page", 0) == doc.page:
        return
    canv.saveState()
    header = getattr(doc, "_header_left", "")
    if header:
        canv.setFont("Sans", 6.8)
        canv.setFillColor(HexColor("#8a94a3"))
        canv.drawString(ML, PAGE_H - MT + 16, header[:78])
        canv.drawRightString(PAGE_W - MR, PAGE_H - MT + 16, BOOK_SHORT)
        canv.setStrokeColor(GRID)
        canv.setLineWidth(0.5)
        canv.line(ML, PAGE_H - MT + 11, PAGE_W - MR, PAGE_H - MT + 11)
    canv.restoreState()

def paint_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(HexColor("#071630"))
    canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    if os.path.exists(COVER):
        try:
            canv.drawImage(COVER, 0, 0, width=PAGE_W, height=PAGE_H,
                           preserveAspectRatio=True, anchor="c")
        except Exception:
            pass
    canv.setFillColor(HexColor("#071630"))
    try:
        canv.setFillAlpha(0.66)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canv.setFillAlpha(1)
    except Exception:
        pass

    center = PAGE_W / 2.0

    canv.setFillColor(HexColor("#f5d9a8"))
    canv.setFont("Sans", 9)
    canv.drawCentredString(center, PAGE_H - 2.55 * inch, "A COMPLETE BEGINNER'S COURSE",
                           charSpace=3)

    canv.setFillColor(white)
    canv.setFont("Sans-B", 27)
    canv.drawCentredString(center, PAGE_H - 3.12 * inch, "The Practical")
    canv.setFillColor(GOLD)
    canv.drawCentredString(center, PAGE_H - 3.58 * inch, "Data Analyst's Handbook")

    canv.setFillColor(HexColor("#d9efe9"))
    canv.setFont("Sans", 9.6)
    canv.drawCentredString(center, PAGE_H - 4.35 * inch, "From Zero to Your First Data Job in")
    canv.drawCentredString(center, PAGE_H - 4.62 * inch, "Excel, SQL, Statistics, Python and Power BI")

    canv.setFillColor(GOLD)
    canv.rect(center - 45, PAGE_H - 5.25 * inch, 90, 2.5, stroke=0, fill=1)

    canv.setFillColor(white)
    canv.setFont("Serif-I", 15.5)
    canv.drawCentredString(center, PAGE_H - 5.85 * inch, AUTHOR)
    canv.setFillColor(HexColor("#e8d9a0"))
    canv.setFont("Sans", 9.5)
    canv.drawCentredString(center, PAGE_H - 6.2 * inch, '"%s"' % AUTHOR_TAG)

    canv.setFillColor(HexColor("#9fb3d1"))
    canv.setFont("Sans", 8.2)
    canv.drawCentredString(center, 1.15 * inch, "First Edition  \u00b7  %s" % YEAR)
    canv.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._header_left = ""
        self._chapter_start_page = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            if sn in ("ChapterTitle", "PartTitle"):
                text = flowable.getPlainText()
                key = "k" + re.sub(r"\W+", "-", text)[:60]
                level = 0 if (sn == "PartTitle" or text.startswith("Front Matter")) else 1
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (level, text, self.page, key))
                self.canv.addOutlineEntry(text, key, level, 0)
                self._header_left = text
                self._chapter_start_page = self.page

# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

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

def part_divider(label, name, start, end):
    return [
        NextPageTemplate("Divider"),
        PageBreak(),
        Spacer(1, 2.5 * inch),
        Paragraph(label.upper(), STYLES["Label"]),
        Spacer(1, 14),
        Paragraph(inline(name), STYLES["PartTitle"]),
        Spacer(1, 10),
        Paragraph("Chapters %d \u2013 %d" % (start, end), STYLES["Range"]),
        hr_flowable(GOLD, 2.0, before=16, after=0),
    ]

def main():
    global STYLES
    register_fonts()
    STYLES = build_styles()

    docs = load_manuscript()
    words, code_lines, chapters, apps = compute_stats(docs)
    est_pages = int(round(words / 300.0 + code_lines / 35.0 + 12))

    doc = BookDoc(OUTPUT, pagesize=(PAGE_W, PAGE_H),
                  title="%s — %s" % (BOOK_TITLE, AUTHOR),
                  author="%s — %s" % (AUTHOR, AUTHOR_TAG),
                  subject=BOOK_SUBTITLE,
                  creator="build_pdf.py (ReportLab)")

    body_frame = Frame(ML, MB, AVAIL, PAGE_H - MT - MB, id="body",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    full_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                       leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[full_frame], onPage=paint_cover),
        PageTemplate(id="FrontMatter", frames=[body_frame], onPage=paint_footer),
        PageTemplate(id="Content", frames=[body_frame], onPage=paint_footer,
                     onPageEnd=paint_content_end),
        PageTemplate(id="Divider", frames=[body_frame], onPage=paint_footer),
    ])

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC0", fontName="Sans-B", fontSize=10, leading=15,
                       textColor=NAVY, spaceBefore=10),
        ParagraphStyle("TOC1", fontName="Serif", fontSize=9, leading=13.4,
                       textColor=INK, leftIndent=16, firstLineIndent=-16),
    ]
    toc.dotsMinLevel = 0

    story = []
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate("FrontMatter"))
    story.append(PageBreak())

    story.append(Paragraph("Table of Contents", STYLES["TOCTitle"]))
    story.append(hr_flowable(GOLD, 2.0, before=2, after=14))
    story.append(toc)
    story.append(NextPageTemplate("FrontMatter"))
    story.append(PageBreak())

    by_num = {}
    for kind, key, md in docs:
        if kind == "ch":
            by_num[key] = md

    front_md = next((md for k, _, md in docs if k == "front"), None)
    if front_md:
        story.extend(render_doc(front_md))

    app_docs = [(k, letter, md) for k, letter, md in docs if k == "app"]

    for label, name, start, end in PARTS:
        if not any(num in by_num for num in range(start, end + 1)):
            continue
        story.extend(part_divider(label, name, start, end))
        first = True
        for num in range(start, end + 1):
            md = by_num.get(num)
            if md is None:
                continue
            if first:
                story.append(NextPageTemplate("Content"))
                first = False
            story.append(PageBreak())
            story.extend(render_doc(md))

    if app_docs:
        story.extend([
            NextPageTemplate("Divider"),
            PageBreak(),
            Spacer(1, 2.5 * inch),
            Paragraph("APPENDICES", STYLES["Label"]),
            Spacer(1, 14),
            Paragraph("Reference Section", STYLES["PartTitle"]),
            Spacer(1, 10),
            Paragraph("Quick answers, cheat sheets, solutions and practice data",
                      STYLES["Range"]),
            hr_flowable(GOLD, 2.0, before=16, after=0),
        ])
        for _, letter, md in app_docs:
            story.append(NextPageTemplate("Content"))
            story.append(PageBreak())
            story.extend(render_doc(md))

    parts_present = sum(1 for _, _, start, end in PARTS
                        if any(n in by_num for n in range(start, end + 1)))
    today = datetime.date.today().strftime("%d %B %Y")
    colophon_md = (
        "# About this Edition\n\n"
        "*Production notes*\n\n"
        "**%s — %s** was typeset directly from its Markdown manuscript with "
        "build_pdf.py (ReportLab): 7 x 10 inch textbook trim, running headers, "
        "a linked table of contents, and PDF outline bookmarks.\n\n"
        "- Edition: First Edition, %s (compiled %s)\n"
        "- Contents: %d chapters in %d parts, plus %d appendices\n"
        "- Volume: approximately %s words of prose and %d lines of code "
        "(estimated %d print pages)\n"
        "- Toolchain: Markdown manuscript, build_book.py (HTML edition), "
        "build_pdf.py (this PDF)\n"
        "- Typeface: DejaVu (serif body, sans display, mono code)\n\n"
        "To rebuild either edition after editing the manuscript, run "
        "`python3 build_book.py` then `python3 build_pdf.py`. "
        "The companion HTML edition is screen-optimised and regenerates in seconds.\n\n"
        "Thank you for reading this book — and for teaching from it. "
        "The data is already pouring in somewhere near you.\n"
        % (BOOK_TITLE, BOOK_SUBTITLE, YEAR, today, chapters, parts_present, apps,
           "{:,}".format(words), code_lines, est_pages)
    )
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())
    story.extend(render_doc(colophon_md))

    doc.multiBuild(story)
    size_kb = os.path.getsize(OUTPUT) / 1024.0
    print("PDF built: %s" % OUTPUT)
    print("  pages: %d   size: %.1f KB" % (doc.page, size_kb))
    print("  chapters: %d   appendices: %d   words: %s   code lines: %d"
          % (chapters, apps, "{:,}".format(words), code_lines))

if __name__ == "__main__":
    main()
