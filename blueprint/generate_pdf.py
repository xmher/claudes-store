#!/usr/bin/env python3
"""
The Debt Freedom Blueprint — PDF Generator
StackedSheets | Lora + Poppins | Charcoal + Emerald

Converts markdown chapter files into a professionally styled PDF
using ReportLab with custom fonts, branded colors, and premium layout.
"""

import os
import re
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether, NextPageTemplate, Flowable,
    CondPageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String
from reportlab.pdfgen import canvas

# ── Brand Constants ─────────────────────────────────────────────────
CHARCOAL = HexColor('#2B2D31')
EMERALD  = HexColor('#2D8C6F')
SAGE     = HexColor('#F4F7F5')
RED      = HexColor('#C4574B')
LIGHT_GRAY = HexColor('#E8E8E8')
MID_GRAY   = HexColor('#888888')
DARK_GRAY  = HexColor('#555555')
WHITE    = white

PAGE_W, PAGE_H = letter  # 612 x 792 points
MARGIN = 60
CONTENT_W = PAGE_W - 2 * MARGIN

# ── Font Registration ───────────────────────────────────────────────
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')

def register_fonts():
    """Register Lora and Poppins font families."""
    lora_dir = os.path.join(FONT_DIR, 'lora')
    poppins_dir = os.path.join(FONT_DIR, 'poppins')

    font_map = {
        'Lora':           os.path.join(lora_dir, 'Lora-Regular.ttf'),
        'Lora-Bold':      os.path.join(lora_dir, 'Lora-Bold.ttf'),
        'Lora-Italic':    os.path.join(lora_dir, 'Lora-Italic.ttf'),
        'Lora-BoldItalic':os.path.join(lora_dir, 'Lora-BoldItalic.ttf'),
        'Poppins':        os.path.join(poppins_dir, 'Poppins-Regular.ttf'),
        'Poppins-Bold':   os.path.join(poppins_dir, 'Poppins-Bold.ttf'),
        'Poppins-Light':  os.path.join(poppins_dir, 'Poppins-Light.ttf'),
        'Poppins-Medium': os.path.join(poppins_dir, 'Poppins-Medium.ttf'),
        'Poppins-Italic': os.path.join(poppins_dir, 'Poppins-Italic.ttf'),
        'Poppins-BoldItalic': os.path.join(poppins_dir, 'Poppins-BoldItalic.ttf'),
        'Poppins-MediumItalic': os.path.join(poppins_dir, 'Poppins-MediumItalic.ttf'),
        'Poppins-LightItalic': os.path.join(poppins_dir, 'Poppins-LightItalic.ttf'),
    }

    for name, path in font_map.items():
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            try:
                pdfmetrics.registerFont(TTFont(name, path))
            except Exception as e:
                print(f"Warning: Could not register {name}: {e}")
        else:
            print(f"Warning: Font file not found or too small: {path}")

    # Register font families for bold/italic auto-mapping
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    try:
        registerFontFamily('Lora',
                           normal='Lora', bold='Lora-Bold',
                           italic='Lora-Italic', boldItalic='Lora-BoldItalic')
        registerFontFamily('Poppins',
                           normal='Poppins', bold='Poppins-Bold',
                           italic='Poppins-Italic', boldItalic='Poppins-BoldItalic')
    except Exception:
        pass

register_fonts()

# ── Paragraph Styles ────────────────────────────────────────────────

styles = getSampleStyleSheet()

# Body text
BODY = ParagraphStyle(
    'Body', fontName='Poppins', fontSize=10.5, leading=16,
    textColor=CHARCOAL, alignment=TA_JUSTIFY, spaceAfter=9,
    spaceBefore=0
)

# Bold body
BODY_BOLD = ParagraphStyle(
    'BodyBold', parent=BODY, fontName='Poppins-Bold'
)

# Italic body
BODY_ITALIC = ParagraphStyle(
    'BodyItalic', parent=BODY, fontName='Poppins-Italic'
)

# Chapter title (used on chapter opener pages)
CHAPTER_TITLE = ParagraphStyle(
    'ChapterTitle', fontName='Lora-Bold', fontSize=28, leading=34,
    textColor=WHITE, alignment=TA_LEFT, spaceAfter=8
)

# Chapter subtitle
CHAPTER_SUBTITLE = ParagraphStyle(
    'ChapterSubtitle', fontName='Poppins-Light', fontSize=14, leading=20,
    textColor=EMERALD, alignment=TA_LEFT, spaceAfter=0
)

# Section header (## level)
SECTION_HEADER = ParagraphStyle(
    'SectionHeader', fontName='Poppins-Bold', fontSize=13, leading=18,
    textColor=EMERALD, alignment=TA_LEFT, spaceBefore=22, spaceAfter=10
)

# Subsection header (### level)
SUBSECTION_HEADER = ParagraphStyle(
    'SubsectionHeader', fontName='Poppins-Bold', fontSize=11.5, leading=16,
    textColor=CHARCOAL, alignment=TA_LEFT, spaceBefore=16, spaceAfter=8
)

# Sub-subsection header (#### level)
SUBSUBSECTION_HEADER = ParagraphStyle(
    'SubSubsectionHeader', fontName='Poppins-Medium', fontSize=10.5, leading=15,
    textColor=CHARCOAL, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6
)

# Bullet / list item
BULLET = ParagraphStyle(
    'Bullet', fontName='Poppins', fontSize=10.5, leading=15.5,
    textColor=CHARCOAL, alignment=TA_LEFT, leftIndent=20,
    spaceAfter=4, bulletIndent=6, bulletFontName='Poppins',
    bulletFontSize=10.5
)

# Numbered list item
NUMBERED = ParagraphStyle(
    'Numbered', parent=BULLET, leftIndent=24, bulletIndent=0
)

# Blockquote / callout text
CALLOUT_TEXT = ParagraphStyle(
    'CalloutText', fontName='Poppins', fontSize=10, leading=15,
    textColor=CHARCOAL, alignment=TA_LEFT, spaceAfter=4
)

# Table header
TABLE_HEADER = ParagraphStyle(
    'TableHeader', fontName='Poppins-Bold', fontSize=9, leading=12,
    textColor=WHITE, alignment=TA_LEFT
)

# Table cell
TABLE_CELL = ParagraphStyle(
    'TableCell', fontName='Poppins', fontSize=9, leading=12.5,
    textColor=CHARCOAL, alignment=TA_LEFT
)

# Cover styles
COVER_BRAND = ParagraphStyle(
    'CoverBrand', fontName='Poppins-Light', fontSize=11, leading=14,
    textColor=HexColor('#AAAAAA'), alignment=TA_CENTER
)
COVER_TITLE = ParagraphStyle(
    'CoverTitle', fontName='Lora-Bold', fontSize=36, leading=44,
    textColor=WHITE, alignment=TA_CENTER
)
COVER_SUBTITLE = ParagraphStyle(
    'CoverSubtitle', fontName='Poppins-Light', fontSize=16, leading=22,
    textColor=EMERALD, alignment=TA_CENTER
)
COVER_URL = ParagraphStyle(
    'CoverURL', fontName='Poppins-Italic', fontSize=10, leading=14,
    textColor=MID_GRAY, alignment=TA_CENTER
)

# Front matter styles
FM_HEADING = ParagraphStyle(
    'FMHeading', fontName='Lora-Bold', fontSize=22, leading=28,
    textColor=CHARCOAL, alignment=TA_LEFT, spaceBefore=16, spaceAfter=12
)
FM_BODY = ParagraphStyle(
    'FMBody', fontName='Poppins', fontSize=10.5, leading=16,
    textColor=CHARCOAL, alignment=TA_LEFT, spaceAfter=8
)
FM_BODY_ITALIC = ParagraphStyle(
    'FMBodyItalic', parent=FM_BODY, fontName='Poppins-Italic'
)
FM_BODY_BOLD = ParagraphStyle(
    'FMBodyBold', parent=FM_BODY, fontName='Poppins-Bold'
)

TOC_CHAPTER = ParagraphStyle(
    'TOCChapter', fontName='Poppins-Bold', fontSize=11, leading=22,
    textColor=CHARCOAL, alignment=TA_LEFT, leftIndent=0
)
TOC_SUBTITLE = ParagraphStyle(
    'TOCSubtitle', fontName='Poppins-Italic', fontSize=9.5, leading=14,
    textColor=MID_GRAY, alignment=TA_LEFT, leftIndent=10, spaceAfter=8
)
TOC_APPENDIX = ParagraphStyle(
    'TOCAppendix', fontName='Poppins-Medium', fontSize=10, leading=20,
    textColor=CHARCOAL, alignment=TA_LEFT, leftIndent=0
)


# ── Custom Flowables ────────────────────────────────────────────────

class SectionHeaderBar(Flowable):
    """Charcoal rounded rect bar with emerald text for ## headers."""
    def __init__(self, text, width=CONTENT_W):
        Flowable.__init__(self)
        self.text = text
        self.bar_width = width
        self.bar_height = 30
        self.width = width
        self.height = self.bar_height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(CHARCOAL)
        c.roundRect(0, 0, self.bar_width, self.bar_height, 5, fill=1, stroke=0)
        c.setFillColor(EMERALD)
        c.setFont('Poppins-Bold', 12)
        c.drawString(14, 9, self.text)
        c.restoreState()


class CalloutBox(Flowable):
    """Sage rounded rect with emerald left border for tips/stat boxes/blockquotes."""
    def __init__(self, content_flowables, width=CONTENT_W, box_type='tip'):
        Flowable.__init__(self)
        self.content = content_flowables
        self.box_width = width
        self.box_type = box_type
        # Calculate height from content
        self._calc_height()

    def _calc_height(self):
        from reportlab.platypus.doctemplate import LayoutError
        w = self.box_width - 32  # padding
        total = 0
        for f in self.content:
            if hasattr(f, 'wrap'):
                fw, fh = f.wrap(w, 10000)
                total += fh
        self.box_height = total + 24  # padding
        self.width = self.box_width
        self.height = self.box_height + 18  # clearance below

    def draw(self):
        c = self.canv
        c.saveState()

        # Background
        c.setFillColor(SAGE)
        c.roundRect(0, 18, self.box_width, self.box_height, 6, fill=1, stroke=0)

        # Left accent border
        accent = EMERALD if self.box_type != 'stat' else EMERALD
        c.setFillColor(accent)
        c.roundRect(0, 18, 5, self.box_height, 2, fill=1, stroke=0)

        # Draw content
        y = 18 + self.box_height - 14
        inner_w = self.box_width - 32
        for f in self.content:
            fw, fh = f.wrap(inner_w, 10000)
            y -= fh
            f.drawOn(c, 18, y)

        c.restoreState()


class EmeraldLine(Flowable):
    """A thin emerald horizontal rule."""
    def __init__(self, width=CONTENT_W):
        Flowable.__init__(self)
        self.line_width = width
        self.width = width
        self.height = 12

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(EMERALD)
        self.canv.setLineWidth(1.5)
        self.canv.line(0, 6, self.line_width, 6)
        self.canv.restoreState()


class GrayLine(Flowable):
    """A thin gray horizontal rule."""
    def __init__(self, width=CONTENT_W):
        Flowable.__init__(self)
        self.line_width = width
        self.width = width
        self.height = 16

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(LIGHT_GRAY)
        self.canv.setLineWidth(0.75)
        self.canv.line(0, 8, self.line_width, 8)
        self.canv.restoreState()


class ChapterOpenerPage(Flowable):
    """Full-page chapter opener with charcoal background."""
    def __init__(self, chapter_num, title, subtitle):
        Flowable.__init__(self)
        self.chapter_num = chapter_num
        self.title = title
        self.subtitle = subtitle
        self.width = PAGE_W
        self.height = PAGE_H

    def draw(self):
        c = self.canv
        c.saveState()

        # Full charcoal background
        c.setFillColor(CHARCOAL)
        c.rect(-MARGIN, -MARGIN, PAGE_W, PAGE_H, fill=1, stroke=0)

        # Top emerald accent bar
        c.setFillColor(EMERALD)
        c.rect(-MARGIN, PAGE_H - MARGIN - 55, PAGE_W, 6, fill=1, stroke=0)

        # Chapter number
        c.setFillColor(EMERALD)
        c.setFont('Poppins-Medium', 14)
        y_start = PAGE_H - MARGIN - 130
        c.drawString(0, y_start, f'CHAPTER {self.chapter_num}')

        # Small emerald line under chapter number
        c.setStrokeColor(EMERALD)
        c.setLineWidth(2)
        c.line(0, y_start - 10, 80, y_start - 10)

        # Title
        c.setFillColor(WHITE)
        c.setFont('Lora-Bold', 32)
        # Word-wrap title
        title_y = y_start - 55
        words = self.title.split()
        lines = []
        current = ""
        for w in words:
            test = current + " " + w if current else w
            if c.stringWidth(test, 'Lora-Bold', 32) < CONTENT_W:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        for line in lines:
            c.drawString(0, title_y, line)
            title_y -= 42

        # Subtitle
        c.setFillColor(EMERALD)
        c.setFont('Poppins-Light', 14)
        c.drawString(0, title_y - 20, self.subtitle)

        # Bottom emerald accent bar
        c.setFillColor(EMERALD)
        c.rect(-MARGIN, -MARGIN + 45, PAGE_W, 6, fill=1, stroke=0)

        # Brand at bottom
        c.setFillColor(MID_GRAY)
        c.setFont('Poppins-Light', 9)
        c.drawCentredString(CONTENT_W / 2, -MARGIN + 25,
                            'The Debt Freedom Blueprint · StackedSheets')

        c.restoreState()


# ── Page Templates ──────────────────────────────────────────────────

def cover_page_template(canvas, doc):
    """Draw the cover page background."""
    canvas.saveState()

    # Full charcoal background
    canvas.setFillColor(CHARCOAL)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Top emerald accent bar
    canvas.setFillColor(EMERALD)
    canvas.rect(0, PAGE_H - 50, PAGE_W, 6, fill=1, stroke=0)

    # Brand: S T A C K E D S H E E T S
    canvas.setFillColor(HexColor('#AAAAAA'))
    canvas.setFont('Poppins-Light', 11)
    brand = 'S  T  A  C  K  E  D  S  H  E  E  T  S'
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 85, brand)

    # Thin line under brand
    canvas.setStrokeColor(HexColor('#555555'))
    canvas.setLineWidth(0.5)
    bw = canvas.stringWidth(brand, 'Poppins-Light', 11)
    canvas.line(PAGE_W / 2 - bw / 2, PAGE_H - 95,
                PAGE_W / 2 + bw / 2, PAGE_H - 95)

    # Bottom emerald accent bar
    canvas.setFillColor(EMERALD)
    canvas.rect(0, 44, PAGE_W, 6, fill=1, stroke=0)

    # URL at bottom
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Poppins-Italic', 10)
    canvas.drawCentredString(PAGE_W / 2, 24, 'stackedsheets.etsy.com')

    canvas.restoreState()


def body_header_footer(canvas, doc):
    """Draw header and footer on body pages."""
    canvas.saveState()
    page_num = doc.page

    # Header bar
    canvas.setFillColor(CHARCOAL)
    canvas.rect(0, PAGE_H - 42, PAGE_W, 42, fill=1, stroke=0)

    # Header text
    canvas.setFillColor(EMERALD)
    canvas.setFont('Poppins-Medium', 9)
    canvas.drawString(MARGIN, PAGE_H - 28, 'The Debt Freedom Blueprint')
    canvas.setFillColor(HexColor('#888888'))
    canvas.setFont('Poppins-Light', 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 28, 'StackedSheets')

    # Footer bar
    canvas.setFillColor(CHARCOAL)
    canvas.rect(0, 0, PAGE_W, 32, fill=1, stroke=0)

    # Footer text
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Poppins-Light', 8)
    canvas.drawCentredString(PAGE_W / 2, 12, f'Page {page_num}')

    canvas.restoreState()


def blank_page(canvas, doc):
    """Blank page (for cover, chapter openers)."""
    pass


# ── Markdown Parser ─────────────────────────────────────────────────

def clean_inline(text):
    """Convert markdown inline formatting to ReportLab XML tags."""
    # Bold + italic (***text*** or ___text___)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic (*text*)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # Inline code (`code`)
    text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9" color="#C4574B">\1</font>', text)
    # Links [text](url) - just show text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Escape ampersands and angle brackets for XML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Restore our XML tags
    text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
    text = text.replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>')
    text = text.replace('&lt;font ', '<font ').replace('&lt;/font&gt;', '</font>')
    # Fix font tags that got escaped
    text = re.sub(r'<font ([^>]*?)&gt;', r'<font \1>', text)
    return text


def parse_table(lines):
    """Parse a markdown table into a list of rows."""
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # Skip separator rows
            if all(re.match(r'^[-:]+$', c) for c in cells):
                continue
            rows.append(cells)
    return rows


def build_table_flowable(rows, col_widths=None):
    """Build a ReportLab Table from parsed rows."""
    if not rows:
        return None

    # Convert cells to Paragraphs
    table_data = []
    for i, row in enumerate(rows):
        style = TABLE_HEADER if i == 0 else TABLE_CELL
        table_data.append([Paragraph(clean_inline(cell), style) for cell in row])

    n_cols = max(len(r) for r in table_data)
    # Pad rows to have same number of columns
    for row in table_data:
        while len(row) < n_cols:
            row.append(Paragraph('', TABLE_CELL))

    if col_widths is None:
        col_w = CONTENT_W / n_cols
        col_widths = [col_w] * n_cols

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Style
    style_cmds = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), CHARCOAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Poppins-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        # Body rows
        ('FONTNAME', (0, 1), (-1, -1), 'Poppins'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), CHARCOAL),
        # Alternating row colors
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        # Grid
        ('LINEBELOW', (0, 0), (-1, 0), 1, EMERALD),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, LIGHT_GRAY),
        ('LINEBELOW', (0, -1), (-1, -1), 1, CHARCOAL),
    ]

    # Alternating sage rows
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), SAGE))

    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def is_checkbox_line(line):
    """Check if a line is a checkbox item."""
    return bool(re.match(r'^[-*]\s*\[[ x☐✓]\]', line.strip()))


def parse_markdown_to_flowables(md_text, is_front_matter=False):
    """Parse markdown text into a list of ReportLab flowables."""
    flowables = []
    lines = md_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal rule (---)
        if re.match(r'^---+$', stripped):
            flowables.append(Spacer(1, 6))
            flowables.append(GrayLine())
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # H1 (# title) - used for chapter titles, skip for body (handled by opener)
        if stripped.startswith('# ') and not stripped.startswith('## '):
            # Skip H1 in chapter files - we handle these with the chapter opener
            i += 1
            continue

        # H2 (## header) - Section header bar
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            if is_front_matter:
                flowables.append(Spacer(1, 16))
                flowables.append(Paragraph(clean_inline(text), FM_HEADING))
                flowables.append(Spacer(1, 4))
            else:
                flowables.append(Spacer(1, 18))
                flowables.append(SectionHeaderBar(text))
                flowables.append(Spacer(1, 12))
            i += 1
            continue

        # H3 (### header)
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            flowables.append(Paragraph(clean_inline(text), SUBSECTION_HEADER))
            i += 1
            continue

        # H4 (#### header)
        if stripped.startswith('#### '):
            text = stripped[5:].strip()
            flowables.append(Paragraph(clean_inline(text), SUBSUBSECTION_HEADER))
            i += 1
            continue

        # Table
        if stripped.startswith('|') and i + 1 < len(lines):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            rows = parse_table(table_lines)
            if rows:
                tbl = build_table_flowable(rows)
                if tbl:
                    flowables.append(Spacer(1, 6))
                    flowables.append(tbl)
                    flowables.append(Spacer(1, 10))
            continue

        # Blockquote / callout (> text)
        if stripped.startswith('> '):
            callout_lines = []
            while i < len(lines) and (lines[i].strip().startswith('> ') or lines[i].strip() == '>'):
                text = lines[i].strip()
                if text == '>':
                    callout_lines.append('')
                else:
                    callout_lines.append(text[2:])
                i += 1

            # Determine box type
            full_text = ' '.join(callout_lines)
            box_type = 'tip'
            if 'STAT BOX' in full_text:
                box_type = 'stat'
            elif 'NOTE FROM THE AUTHOR' in full_text:
                box_type = 'author'

            # Build content paragraphs
            content_flowables = []
            for cl in callout_lines:
                if cl.strip():
                    content_flowables.append(
                        Paragraph(clean_inline(cl.strip()), CALLOUT_TEXT)
                    )
                else:
                    content_flowables.append(Spacer(1, 4))

            if content_flowables:
                flowables.append(Spacer(1, 8))
                flowables.append(CalloutBox(content_flowables, CONTENT_W, box_type))
                flowables.append(Spacer(1, 4))
            continue

        # Checkbox items (- [ ] or - [x])
        if is_checkbox_line(stripped):
            checkbox_text = re.sub(r'^[-*]\s*\[[ ]\]\s*', '☐  ', stripped)
            checkbox_text = re.sub(r'^[-*]\s*\[[x✓]\]\s*', '☑  ', checkbox_text)
            flowables.append(Paragraph(clean_inline(checkbox_text), BULLET))
            i += 1
            continue

        # Unordered list (- or * bullet)
        if re.match(r'^[-*]\s+', stripped) and not re.match(r'^---', stripped):
            text = re.sub(r'^[-*]\s+', '', stripped)
            # Collect continuation lines
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^[-*#>|]', lines[i].strip()) and not lines[i].strip().startswith('##'):
                if lines[i].startswith('   ') or lines[i].startswith('\t'):
                    text += ' ' + lines[i].strip()
                    i += 1
                else:
                    break
            flowables.append(Paragraph('•  ' + clean_inline(text), BULLET))
            continue

        # Ordered list (1. 2. etc.)
        m = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if m:
            num = m.group(1)
            text = m.group(2)
            # Collect continuation lines
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^\d+\.', lines[i].strip()) and not re.match(r'^[-*#>|]', lines[i].strip()):
                if lines[i].startswith('   ') or lines[i].startswith('\t'):
                    text += ' ' + lines[i].strip()
                    i += 1
                else:
                    break
            flowables.append(
                Paragraph(f'<b>{num}.</b>  {clean_inline(text)}', NUMBERED)
            )
            continue

        # Regular paragraph - collect consecutive lines
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            if not next_stripped:
                break
            if next_stripped.startswith('#') or next_stripped.startswith('>') or \
               next_stripped.startswith('|') or next_stripped.startswith('---') or \
               re.match(r'^[-*]\s', next_stripped) or re.match(r'^\d+\.\s', next_stripped):
                break
            para_lines.append(next_stripped)
            i += 1

        text = ' '.join(para_lines)
        style = FM_BODY if is_front_matter else BODY
        if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
            text = text[1:-1]
            style = FM_BODY_ITALIC if is_front_matter else BODY_ITALIC
        flowables.append(Paragraph(clean_inline(text), style))

    return flowables


# ── Document Builder ────────────────────────────────────────────────

def build_cover_flowables():
    """Build the cover page content."""
    flowables = []
    flowables.append(Spacer(1, 200))
    flowables.append(Paragraph('THE DEBT FREEDOM', COVER_TITLE))
    flowables.append(Paragraph('BLUEPRINT', COVER_TITLE))
    flowables.append(Spacer(1, 20))
    flowables.append(Paragraph(
        'A Step-by-Step System to Eliminate Your Debt — For Good',
        COVER_SUBTITLE
    ))
    flowables.append(Spacer(1, 600))  # Push to end
    return flowables


def build_chapter_opener(chapter_num, title, subtitle):
    """Build a chapter opener page."""
    return [
        NextPageTemplate('blank'),
        PageBreak(),
        ChapterOpenerPage(chapter_num, title, subtitle),
        NextPageTemplate('body'),
        PageBreak(),
    ]


def extract_chapter_info(md_text):
    """Extract chapter number, title, subtitle from markdown."""
    lines = md_text.strip().split('\n')

    title = ""
    subtitle = ""
    chapter_num = ""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('## '):
            # e.g. "# Chapter 1 — The Debt Landscape"
            title_text = stripped[2:]
            m = re.match(r'Chapter\s+(\d+)\s*[—–-]\s*(.+)', title_text)
            if m:
                chapter_num = m.group(1)
                title = m.group(2).strip()
            else:
                title = title_text
        elif stripped.startswith('## ') and not subtitle:
            subtitle = stripped[3:].strip()
            break

    return chapter_num, title, subtitle


def build_pdf():
    """Main function to build the complete PDF."""
    output_path = os.path.join(os.path.dirname(__file__),
                               'TheDebtFreedomBlueprint_StackedSheets.pdf')
    chapters_dir = os.path.join(os.path.dirname(__file__), 'chapters')

    # Create document
    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=60,
        bottomMargin=50,
        title='The Debt Freedom Blueprint',
        author='StackedSheets',
    )

    # Frames
    cover_frame = Frame(
        MARGIN, 50, CONTENT_W, PAGE_H - 110,
        id='cover',
        showBoundary=0
    )

    body_frame = Frame(
        MARGIN, 46, CONTENT_W, PAGE_H - 115,
        id='body',
        showBoundary=0
    )

    blank_frame = Frame(
        0, 0, PAGE_W, PAGE_H,
        id='blank',
        leftPadding=MARGIN,
        rightPadding=MARGIN,
        topPadding=0,
        bottomPadding=0,
        showBoundary=0
    )

    # Page templates
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=[cover_frame],
                     onPage=cover_page_template),
        PageTemplate(id='body', frames=[body_frame],
                     onPage=body_header_footer),
        PageTemplate(id='blank', frames=[blank_frame],
                     onPage=blank_page),
    ])

    # ── Build story ─────────────────────────────────────────────
    story = []

    # 1. COVER PAGE
    story.extend(build_cover_flowables())

    # 2. FRONT MATTER
    story.append(NextPageTemplate('body'))
    story.append(PageBreak())

    fm_path = os.path.join(os.path.dirname(__file__), '00-front-matter.md')
    if os.path.exists(fm_path):
        with open(fm_path, 'r') as f:
            fm_text = f.read()
        # Split front matter into sections and render
        # Remove the main H1 title (already on cover)
        fm_text = re.sub(r'^#\s+THE DEBT FREEDOM BLUEPRINT\s*\n', '', fm_text)
        fm_text = re.sub(r'^##\s+A Step-by-Step.*\n', '', fm_text)
        fm_text = re.sub(r'^\*\*By StackedSheets\*\*\s*\n', '', fm_text)

        story.extend(parse_markdown_to_flowables(fm_text, is_front_matter=True))

    # 3. CHAPTERS
    chapter_files = sorted([
        f for f in os.listdir(chapters_dir)
        if f.endswith('.md') and f[:2].isdigit()
    ])

    for cf in chapter_files:
        filepath = os.path.join(chapters_dir, cf)
        with open(filepath, 'r') as f:
            md = f.read()

        chapter_num, title, subtitle = extract_chapter_info(md)

        if chapter_num:
            # Chapter opener page
            story.extend(build_chapter_opener(chapter_num, title, subtitle))
        else:
            # Non-chapter content (appendices, closing)
            story.append(PageBreak())

            # For appendices and closing, extract the title
            first_line = md.strip().split('\n')[0]
            if first_line.startswith('# '):
                appendix_title = first_line[2:].strip()
                story.append(Spacer(1, 10))
                story.append(SectionHeaderBar(appendix_title))
                story.append(Spacer(1, 16))

        # Remove the H1 and first H2 (subtitle) since they're on the opener
        body_md = md
        body_md = re.sub(r'^#\s+[^\n]+\n', '', body_md, count=1)
        if chapter_num:
            # Remove the subtitle H2 that matches what's on the opener
            body_md = re.sub(r'^##\s+' + re.escape(subtitle) + r'\s*\n', '', body_md, count=1)

        story.extend(parse_markdown_to_flowables(body_md))

    # BUILD
    print(f"Building PDF: {output_path}")
    doc.build(story)
    print(f"Done! PDF saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")

    return output_path


if __name__ == '__main__':
    build_pdf()
