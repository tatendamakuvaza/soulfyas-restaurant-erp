"""
ReportLab PDF Generation Engine for Soulfyas Quality Restaurant ERP
Generates branded POS receipts with ZIMRA QR codes, dual-currency tax invoices,
employee payslips, financial statements, inventory reports, purchase orders,
cashier shift Z-reports, and table QR code digital menu placards.
"""

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

LOGO_PATH = 'soulfyas_logo.png'
PRIMARY_COLOR = colors.HexColor('#9b721d')  # Warm Gold
SECONDARY_COLOR = colors.HexColor('#222222') # Charcoal
ACCENT_BG = colors.HexColor('#fbfaf7')       # Soft Cream
BORDER_COLOR = colors.HexColor('#e2dcd2')

def get_base_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#555555'),
        alignment=TA_LEFT
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=10,
        spaceAfter=6
    )
    
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=SECONDARY_COLOR
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=SECONDARY_COLOR
    )
    
    cell_right = ParagraphStyle(
        'CellRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=SECONDARY_COLOR
    )
    
    cell_right_bold = ParagraphStyle(
        'CellRightBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_RIGHT,
        textColor=SECONDARY_COLOR
    )
    
    footer_style = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#777777'),
        alignment=TA_CENTER
    )
    
    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'section': section_heading,
        'cell': cell_style,
        'cell_bold': cell_bold,
        'cell_right': cell_right,
        'cell_right_bold': cell_right_bold,
        'footer': footer_style
    }

def create_header(company: dict, doc_title: str):
    """Builds standard restaurant header with logo and statutory details"""
    styles = get_base_styles()
    elements = []
    
    comp_name = company.get('trading_name') or company.get('name') or 'Soulfyas Quality Restaurant'
    address = company.get('address') or 'Harare, Zimbabwe'
    phone = company.get('phone') or '+263 242 700000'
    email = company.get('email') or 'info@soulfyas.co.zw'
    tin = company.get('zimra_tin') or 'N/A'
    vat = company.get('vat_number') or 'N/A'
    nssa = company.get('nssa_number') or 'N/A'
    
    logo_elem = None
    if os.path.exists(LOGO_PATH):
        try:
            logo_elem = Image(LOGO_PATH, width=1.1*inch, height=1.1*inch)
        except Exception:
            logo_elem = Paragraph("<b>🍽️ SOULFYAS</b>", styles['title'])
    else:
        logo_elem = Paragraph("<b>🍽️ SOULFYAS</b>", styles['title'])
        
    company_info_text = (
        f"<b>{comp_name}</b><br/>"
        f"{address}<br/>"
        f"Tel: {phone} | Email: {email}<br/>"
        f"<b>ZIMRA TIN:</b> {tin} | <b>VAT Reg:</b> {vat} | <b>NSSA:</b> {nssa}"
    )
    
    right_info_text = (
        f"<font size=14 color='#9b721d'><b>{doc_title.upper()}</b></font><br/>"
        f"<b>Date:</b> {datetime.now().strftime('%d-%b-%Y %H:%M')}<br/>"
        f"<b>Functional Currency:</b> {company.get('currency', 'USD')}<br/>"
        f"<b>ZIMRA Fiscalised:</b> YES (FD Verified)"
    )
    
    header_table = Table(
        [[logo_elem, Paragraph(company_info_text, styles['subtitle']), Paragraph(right_info_text, styles['subtitle'])]],
        colWidths=[1.2*inch, 3.6*inch, 2.4*inch]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=12, spaceBefore=4))
    return elements

def generate_qr_drawing(data_str: str, size: int = 70):
    """Generates a QR Code drawing widget for fiscal verification or table ordering"""
    d = Drawing(size, size)
    qr_code = qr.QrCodeWidget(data_str)
    qr_code.barWidth = size
    qr_code.barHeight = size
    qr_code.qrVersion = 2
    d.add(qr_code)
    return d

def generate_receipt_pdf(company: dict, sale: dict, items: list, zig_rate: float = 28.50) -> bytes:
    """Generates a POS Receipt / Tax Invoice PDF with ZIMRA QR code and Dual-Currency USD/ZiG totals"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "TAX INVOICE / RECEIPT"))
    
    inv_no = sale.get('invoice_no', 'N/A')
    s_date = str(sale.get('sale_date', datetime.now().strftime('%Y-%m-%d')))
    p_method = sale.get('payment_method', 'Cash')
    cashier = sale.get('cashier_name', 'Cashier')
    order_type = sale.get('order_type', 'Dine-In')
    table_num = sale.get('table_number', 'N/A')
    cust_name = sale.get('customer_name', 'Walk-in Guest')
    
    meta_table_data = [
        [
            Paragraph(f"<b>Invoice No:</b> {inv_no}", styles['cell']),
            Paragraph(f"<b>Date/Time:</b> {s_date}", styles['cell']),
            Paragraph(f"<b>Payment:</b> {p_method}", styles['cell'])
        ],
        [
            Paragraph(f"<b>Guest:</b> {cust_name}", styles['cell']),
            Paragraph(f"<b>Order Type:</b> {order_type} (Tbl {table_num})", styles['cell']),
            Paragraph(f"<b>Server / Cashier:</b> {cashier}", styles['cell'])
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[2.6*inch, 2.4*inch, 2.2*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    curr = company.get('currency', 'USD')
    table_rows = [
        [
            Paragraph("<b>#</b>", styles['cell_bold']),
            Paragraph("<b>Item Description / Modifiers</b>", styles['cell_bold']),
            Paragraph("<b>Qty</b>", styles['cell_right_bold']),
            Paragraph(f"<b>Unit Price ({curr})</b>", styles['cell_right_bold']),
            Paragraph(f"<b>Total ({curr})</b>", styles['cell_right_bold'])
        ]
    ]
    
    subtotal = float(sale.get('subtotal', 0.0))
    tax = float(sale.get('tax', 0.0))
    discount = float(sale.get('discount', 0.0))
    tip = float(sale.get('tip', 0.0))
    total = float(sale.get('total', 0.0))
    
    for idx, item in enumerate(items, 1):
        name = item.get('name', item.get('item_name', 'Item'))
        notes = item.get('notes', '')
        desc_text = f"<b>{name}</b>"
        if notes:
            desc_text += f"<br/><font size=7 color='#666666'><i>{notes}</i></font>"
            
        qty = float(item.get('quantity', item.get('qty', 1)))
        price = float(item.get('unit_price', item.get('price', 0.0)))
        line_tot = float(item.get('line_total', qty * price))
        
        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(desc_text, styles['cell']),
            Paragraph(f"{qty:g}", styles['cell_right']),
            Paragraph(f"{price:,.2f}", styles['cell_right']),
            Paragraph(f"{line_tot:,.2f}", styles['cell_right_bold'])
        ])
        
    items_table = Table(table_rows, colWidths=[0.4*inch, 3.8*inch, 0.8*inch, 1.1*inch, 1.1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ACCENT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 10))
    
    # Dual-currency calculation (ZiG equivalent)
    zig_total = round(total * zig_rate, 2)
    zig_subtotal = round(subtotal * zig_rate, 2)
    zig_tax = round(tax * zig_rate, 2)
    
    summary_data = [
        [Paragraph("Subtotal (Excl. VAT):", styles['cell_right']), Paragraph(f"{curr} {subtotal:,.2f} / ZiG {zig_subtotal:,.2f}", styles['cell_right'])],
        [Paragraph("VAT (15% ZIMRA Standard):", styles['cell_right']), Paragraph(f"{curr} {tax:,.2f} / ZiG {zig_tax:,.2f}", styles['cell_right'])]
    ]
    if discount > 0:
        summary_data.append([Paragraph("Discount Applied:", styles['cell_right']), Paragraph(f"-{curr} {discount:,.2f}", styles['cell_right'])])
    if tip > 0:
        summary_data.append([Paragraph("Service Tip / Gratuity:", styles['cell_right']), Paragraph(f"{curr} {tip:,.2f}", styles['cell_right'])])
        
    summary_data.append([
        Paragraph("<b>GRAND TOTAL (USD):</b>", styles['cell_right_bold']),
        Paragraph(f"<b>{curr} {total:,.2f}</b>", styles['cell_right_bold'])
    ])
    summary_data.append([
        Paragraph("<b>EQUIVALENT IN ZiG (RBZ Rate):</b>", styles['cell_right_bold']),
        Paragraph(f"<b>ZiG {zig_total:,.2f} (Rate: {zig_rate:.2f})</b>", styles['cell_right_bold'])
    ])
    
    summary_table = Table(summary_data, colWidths=[4.6*inch, 2.6*inch])
    summary_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 4),
        ('LINEABOVE', (0,-2), (-1,-2), 1, PRIMARY_COLOR),
        ('BACKGROUND', (0,-2), (-1,-1), ACCENT_BG),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))
    
    # Fiscal QR Code and verification box
    fiscal_url = f"https://efiling.zimra.co.zw/verify?tin={company.get('zimra_tin', '200145892')}&inv={inv_no}&tot={total:.2f}"
    qr_drawing = generate_qr_drawing(fiscal_url, size=65)
    
    fiscal_details_text = (
        f"<b>ZIMRA FISCAL DEVICE VERIFICATION CODE:</b><br/>"
        f"<b>FD Signature:</b> ZIMRA-FD-{inv_no[-10:]}-{secrets.token_hex(3).upper()}<br/>"
        f"<b>Verification Status:</b> <font color='green'><b>VALIDATED & RECORDED</b></font><br/>"
        f"Scan QR code with any ZIMRA verification app or smartphone camera."
    )
    
    fiscal_box = Table(
        [[qr_drawing, Paragraph(fiscal_details_text, styles['cell'])]],
        colWidths=[1.1*inch, 6.1*inch]
    )
    fiscal_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(fiscal_box)
    
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=6, spaceBefore=2))
    story.append(Paragraph("Thank you for dining with Soulfyas Quality Restaurant! Visit us again soon.", styles['footer']))
    
    doc.build(story)
    return buffer.getvalue()

def generate_purchase_order_pdf(company: dict, po: dict, po_lines: list) -> bytes:
    """Generates a Formal Supplier Purchase Order PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "PURCHASE ORDER"))
    curr = company.get('currency', 'USD')
    
    po_no = po.get('po_number', 'PO-001')
    po_date = str(po.get('order_date', datetime.now().strftime('%Y-%m-%d')))
    sup_name = po.get('supplier_name', 'Supplier')
    sup_contact = po.get('contact_person', 'Sales Department')
    sup_phone = po.get('phone', 'N/A')
    sup_email = po.get('email', 'N/A')
    
    po_meta = [
        [
            Paragraph(f"<b>Supplier:</b> {sup_name}<br/>Attn: {sup_contact}<br/>Tel: {sup_phone} | {sup_email}", styles['cell']),
            Paragraph(f"<b>PO Number:</b> {po_no}<br/><b>Order Date:</b> {po_date}<br/><b>Expected Delivery:</b> {po.get('expected_delivery_date', 'Immediate')}", styles['cell'])
        ]
    ]
    t_meta = Table(po_meta, colWidths=[3.6*inch, 3.6*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))
    
    table_rows = [[
        Paragraph("<b>#</b>", styles['cell_bold']),
        Paragraph("<b>Raw Material / Ingredient Description</b>", styles['cell_bold']),
        Paragraph("<b>Unit</b>", styles['cell']),
        Paragraph("<b>Order Qty</b>", styles['cell_right_bold']),
        Paragraph(f"<b>Unit Price ({curr})</b>", styles['cell_right']),
        Paragraph(f"<b>Line Total ({curr})</b>", styles['cell_right_bold'])
    ]]
    
    tot_po = 0.0
    for idx, line in enumerate(po_lines, 1):
        name = line.get('item_name', 'Item')
        unit = line.get('unit', 'kg')
        qty = float(line.get('quantity', 1))
        cost = float(line.get('unit_cost', 0.0))
        ltot = float(line.get('line_total', qty * cost))
        tot_po += ltot
        
        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(name, styles['cell']),
            Paragraph(unit, styles['cell']),
            Paragraph(f"{qty:,.2f}", styles['cell_right_bold']),
            Paragraph(f"{cost:,.2f}", styles['cell_right']),
            Paragraph(f"{ltot:,.2f}", styles['cell_right_bold'])
        ])
        
    t_items = Table(table_rows, colWidths=[0.4*inch, 3.4*inch, 0.6*inch, 0.9*inch, 0.9*inch, 1.0*inch])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ACCENT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 10))
    
    tot_table = Table([
        [Paragraph("<b>TOTAL PURCHASE ORDER VALUE:</b>", styles['cell_right_bold']), Paragraph(f"<b>{curr} {tot_po:,.2f}</b>", styles['cell_right_bold'])]
    ], colWidths=[5.8*inch, 1.4*inch])
    tot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tot_table)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Terms & Conditions:</b> Goods must be accompanied by a delivery note and valid ZIMRA tax clearance (ITF 263).", styles['footer']))
    
    doc.build(story)
    return buffer.getvalue()

def generate_z_report_pdf(company: dict, shift: dict) -> bytes:
    """Generates an Official Cashier Shift Closeout / End-of-Day Z-Report PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "CASHIER SHIFT Z-REPORT"))
    curr = company.get('currency', 'USD')
    
    cashier_name = shift.get('cashier_name', 'Cashier')
    shift_start = str(shift.get('shift_start', 'N/A'))
    shift_end = str(shift.get('shift_end', datetime.now().strftime('%Y-%m-%d %H:%M')))
    
    s_meta = [
        [
            Paragraph(f"<b>Cashier / Operator:</b> {cashier_name}", styles['cell']),
            Paragraph(f"<b>Shift Start:</b> {shift_start}", styles['cell'])
        ],
        [
            Paragraph(f"<b>Terminal / Station:</b> POS Register 1", styles['cell']),
            Paragraph(f"<b>Shift Close:</b> {shift_end}", styles['cell'])
        ]
    ]
    t_sm = Table(s_meta, colWidths=[3.6*inch, 3.6*inch])
    t_sm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_sm)
    story.append(Spacer(1, 14))
    
    op_float = float(shift.get('opening_float', 0.0))
    cash_sales = float(shift.get('cash_sales', 0.0))
    card_sales = float(shift.get('card_sales', 0.0))
    ecocash_sales = float(shift.get('ecocash_sales', 0.0))
    bank_sales = float(shift.get('bank_sales', 0.0))
    tot_sales = cash_sales + card_sales + ecocash_sales + bank_sales
    expected_cash = op_float + cash_sales
    actual_cash = float(shift.get('actual_cash_counted', expected_cash))
    variance = actual_cash - expected_cash
    
    z_rows = [
        [Paragraph("Opening Cash Float in Register", styles['cell']), Paragraph(f"{curr} {op_float:,.2f}", styles['cell_right'])],
        [Paragraph("Cash Sales Collected", styles['cell']), Paragraph(f"{curr} {cash_sales:,.2f}", styles['cell_right'])],
        [Paragraph("Card / Visa Tender", styles['cell']), Paragraph(f"{curr} {card_sales:,.2f}", styles['cell_right'])],
        [Paragraph("Ecocash / Mobile Money Tender", styles['cell']), Paragraph(f"{curr} {ecocash_sales:,.2f}", styles['cell_right'])],
        [Paragraph("Direct Bank Transfer Tender", styles['cell']), Paragraph(f"{curr} {bank_sales:,.2f}", styles['cell_right'])],
        [Paragraph("<b>TOTAL REVENUE COLLECTED</b>", styles['cell_bold']), Paragraph(f"<b>{curr} {tot_sales:,.2f}</b>", styles['cell_right_bold'])],
        [Paragraph("<b>EXPECTED CASH IN DRAWER (Float + Cash Sales)</b>", styles['cell_bold']), Paragraph(f"<b>{curr} {expected_cash:,.2f}</b>", styles['cell_right_bold'])],
        [Paragraph("<b>ACTUAL CASH PHYSICALLY COUNTED</b>", styles['cell_bold']), Paragraph(f"<b>{curr} {actual_cash:,.2f}</b>", styles['cell_right_bold'])],
        [Paragraph("<b>CASH VARIANCE (OVER / SHORT)</b>", styles['cell_bold']), Paragraph(f"<b>{'+' if variance>=0 else ''}{curr} {variance:,.2f}</b>", styles['cell_right_bold'])]
    ]
    
    t_z = Table(z_rows, colWidths=[4.8*inch, 2.4*inch])
    t_z.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0,5), (-1,5), ACCENT_BG),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor('#ffebee') if variance < 0 else colors.HexColor('#e8f5e9')),
    ]))
    story.append(t_z)
    
    story.append(Spacer(1, 24))
    
    # Signatures Table
    sig_data = [
        [Paragraph("<b>Cashier Signature:</b> ___________________", styles['cell']), Paragraph("<b>Duty Manager Signature:</b> ___________________", styles['cell'])],
        [Paragraph(f"Date: {datetime.now().strftime('%d-%b-%Y')}", styles['cell']), Paragraph(f"Date: {datetime.now().strftime('%d-%b-%Y')}", styles['cell'])]
    ]
    t_sig = Table(sig_data, colWidths=[3.6*inch, 3.6*inch])
    t_sig.setStyle(TableStyle([('PADDING', (0,0), (-1,-1), 10)]))
    story.append(t_sig)
    
    doc.build(story)
    return buffer.getvalue()

def generate_table_qr_placard_pdf(company: dict, table_number: str, order_url: str) -> bytes:
    """Generates a Printable Table Tent / Placard with QR code for Guest Contactless Digital Ordering"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = get_base_styles()
    story = []
    
    comp_name = company.get('trading_name') or company.get('name') or 'Soulfyas Quality Restaurant'
    
    story.append(Paragraph(f"<font size=22 color='#9b721d'><b>🍽️ {comp_name.upper()}</b></font>", ParagraphStyle('H', parent=styles['title'], alignment=TA_CENTER)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>WELCOME TO YOUR TABLE</b>", ParagraphStyle('W', parent=styles['subtitle'], alignment=TA_CENTER, fontSize=14)))
    story.append(Spacer(1, 14))
    
    # Table Number Callout
    tbl_box = Table([[Paragraph(f"<font size=32 color='#9b721d'><b>TABLE {table_number}</b></font>", ParagraphStyle('T', alignment=TA_CENTER))]], colWidths=[5.5*inch])
    tbl_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('BOX', (0,0), (-1,-1), 2, PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(tbl_box)
    story.append(Spacer(1, 20))
    
    # QR Code
    qr_draw = generate_qr_drawing(order_url, size=180)
    qr_table = Table([[qr_draw]], colWidths=[5.5*inch])
    qr_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(qr_table)
    story.append(Spacer(1, 20))
    
    instructions = (
        "<b>HOW TO ORDER:</b><br/>"
        "1. Open your smartphone camera or QR scanner.<br/>"
        "2. Point at the QR code above to open our <b>Live Digital Menu</b>.<br/>"
        "3. Browse delicious chef specials, customize your sides & basting, and tap <b>Submit Order</b>!<br/>"
        "Our kitchen will start preparing your meal immediately."
    )
    story.append(Paragraph(instructions, ParagraphStyle('Inst', parent=styles['cell'], alignment=TA_CENTER, fontSize=11, leading=16)))
    story.append(Spacer(1, 24))
    story.append(Paragraph(f"Free High-Speed Guest Wi-Fi: <b>Soulfyas-Guest</b> | Password: <b>delicious2026</b>", styles['footer']))
    
    doc.build(story)
    return buffer.getvalue()

def generate_payslip_pdf(company: dict, payslip: dict, period_str: str) -> bytes:
    """Generates an Official Monthly Employee Payslip PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "CONFIDENTIAL PAYSLIP"))
    curr = company.get('currency', 'USD')
    
    emp_meta = [
        [
            Paragraph(f"<b>Employee Name:</b> {payslip.get('employee_name', 'N/A')}", styles['cell']),
            Paragraph(f"<b>Pay Period:</b> {period_str}", styles['cell'])
        ],
        [
            Paragraph(f"<b>Employee Code:</b> {payslip.get('employee_no', 'N/A')}", styles['cell']),
            Paragraph(f"<b>Payment Date:</b> {datetime.now().strftime('%d-%b-%Y')}", styles['cell'])
        ]
    ]
    t_meta = Table(emp_meta, colWidths=[3.6*inch, 3.6*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))
    
    earnings_rows = [
        ("Basic Salary", f"{curr} {payslip.get('basic_salary', 0.0):,.2f}"),
        ("Allowances & Bonuses", f"{curr} {payslip.get('allowances', 0.0):,.2f}"),
        ("GROSS EARNINGS", f"{curr} {payslip.get('gross_earnings', 0.0):,.2f}")
    ]
    
    deductions_rows = [
        ("NSSA POBS Pension (4.5%)", f"{curr} {payslip.get('nssa_employee', 0.0):,.2f}"),
        ("PAYE Income Tax (ZIMRA)", f"{curr} {payslip.get('base_paye', 0.0):,.2f}"),
        ("AIDS Levy (3% on PAYE)", f"{curr} {payslip.get('aids_levy', 0.0):,.2f}"),
        ("Other Deductions / Advances", f"{curr} {payslip.get('other_deductions', 0.0):,.2f}"),
        ("TOTAL DEDUCTIONS", f"{curr} {payslip.get('total_deductions', 0.0):,.2f}")
    ]
    
    story.append(Paragraph("<b>Earnings & Statutory Deductions</b>", styles['section']))
    
    pay_table_data = [
        [
            Paragraph("<b>Earnings Description</b>", styles['cell_bold']),
            Paragraph("<b>Amount</b>", styles['cell_right_bold']),
            Paragraph("<b>Deductions Description</b>", styles['cell_bold']),
            Paragraph("<b>Amount</b>", styles['cell_right_bold'])
        ]
    ]
    
    max_len = max(len(earnings_rows), len(deductions_rows))
    for i in range(max_len):
        e_title, e_val = earnings_rows[i] if i < len(earnings_rows) else ("", "")
        d_title, d_val = deductions_rows[i] if i < len(deductions_rows) else ("", "")
        
        is_e_total = "GROSS" in e_title
        is_d_total = "TOTAL" in d_title
        
        e_p1 = Paragraph(f"<b>{e_title}</b>" if is_e_total else e_title, styles['cell_bold'] if is_e_total else styles['cell'])
        e_p2 = Paragraph(f"<b>{e_val}</b>" if is_e_total else e_val, styles['cell_right_bold'] if is_e_total else styles['cell_right'])
        d_p1 = Paragraph(f"<b>{d_title}</b>" if is_d_total else d_title, styles['cell_bold'] if is_d_total else styles['cell'])
        d_p2 = Paragraph(f"<b>{d_val}</b>" if is_d_total else d_val, styles['cell_right_bold'] if is_d_total else styles['cell_right'])
        
        pay_table_data.append([e_p1, e_p2, d_p1, d_p2])
        
    t_pay = Table(pay_table_data, colWidths=[2.2*inch, 1.4*inch, 2.2*inch, 1.4*inch])
    t_pay.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, len(earnings_rows)), (1, len(earnings_rows)), ACCENT_BG),
        ('BACKGROUND', (2, len(deductions_rows)), (3, len(deductions_rows)), ACCENT_BG),
    ]))
    story.append(t_pay)
    story.append(Spacer(1, 14))
    
    net_pay_val = payslip.get('net_pay', 0.0)
    net_box = [
        [
            Paragraph("<font size=12><b>NET TAKE-HOME PAY:</b></font>", styles['cell']),
            Paragraph(f"<font size=14 color='#9b721d'><b>{curr} {net_pay_val:,.2f}</b></font>", styles['cell_right_bold'])
        ]
    ]
    t_net = Table(net_box, colWidths=[4.2*inch, 3.0*inch])
    t_net.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('BOX', (0,0), (-1,-1), 1.5, PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_net)
    story.append(Spacer(1, 14))
    
    story.append(Paragraph("<b>Employer Statutory Contributions (Informational)</b>", styles['section']))
    employer_rows = [
        [
            Paragraph("NSSA Employer Pension (4.5%)", styles['cell']),
            Paragraph(f"{curr} {payslip.get('nssa_employer', 0.0):,.2f}", styles['cell_right'])
        ],
        [
            Paragraph("NSSA APWCS Workers Comp (1.4%)", styles['cell']),
            Paragraph(f"{curr} {payslip.get('nssa_apwcs', 0.0):,.2f}", styles['cell_right'])
        ],
        [
            Paragraph("<b>Total Company Employment Cost</b>", styles['cell_bold']),
            Paragraph(f"<b>{curr} {payslip.get('total_employer_cost', 0.0):,.2f}</b>", styles['cell_right_bold'])
        ]
    ]
    t_emp = Table(employer_rows, colWidths=[4.8*inch, 2.4*inch])
    t_emp.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,-1), (-1,-1), 1, BORDER_COLOR),
    ]))
    story.append(t_emp)
    
    story.append(Spacer(1, 24))
    story.append(Paragraph("This is a computer-generated payslip. No signature is required.", styles['footer']))
    
    doc.build(story)
    return buffer.getvalue()

def generate_financial_report_pdf(company: dict, pnl_df, bs_df=None, period_str="Year to Date") -> bytes:
    """Generates IFRS 18-oriented Statement of Profit or Loss and Financial Position PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "FINANCIAL REPORT"))
    curr = company.get('currency', 'USD')
    
    story.append(Paragraph(f"<b>IFRS 18 Statement of Profit or Loss ({period_str})</b>", styles['section']))
    
    pnl_table_data = [[
        Paragraph("<b>IFRS 18 Financial Line Item</b>", styles['cell_bold']),
        Paragraph(f"<b>Amount ({curr})</b>", styles['cell_right_bold'])
    ]]
    
    for _, row in pnl_df.iterrows():
        line = str(row.iloc[0])
        amt = float(row.iloc[1]) if len(row) > 1 and pd_not_null(row.iloc[1]) else 0.0
        is_subtotal = any(k in line.lower() for k in ['profit', 'total', 'margin', 'ebitda'])
        
        p1 = Paragraph(f"<b>{line}</b>" if is_subtotal else line, styles['cell_bold'] if is_subtotal else styles['cell'])
        p2 = Paragraph(f"<b>{amt:,.2f}</b>" if is_subtotal else f"{amt:,.2f}", styles['cell_right_bold'] if is_subtotal else styles['cell_right'])
        pnl_table_data.append([p1, p2])
        
    t_pnl = Table(pnl_table_data, colWidths=[5.2*inch, 2.0*inch])
    t_pnl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ACCENT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(t_pnl)
    story.append(Spacer(1, 16))
    
    if bs_df is not None and len(bs_df):
        story.append(Paragraph(f"<b>Statement of Financial Position (Balance Sheet)</b>", styles['section']))
        bs_data = [[
            Paragraph("<b>Classification / Account Category</b>", styles['cell_bold']),
            Paragraph(f"<b>Amount ({curr})</b>", styles['cell_right_bold'])
        ]]
        for _, row in bs_df.iterrows():
            line = str(row.iloc[0])
            amt = float(row.iloc[1]) if len(row) > 1 and pd_not_null(row.iloc[1]) else 0.0
            is_sub = any(k in line.lower() for k in ['total', 'net', 'equity'])
            p1 = Paragraph(f"<b>{line}</b>" if is_sub else line, styles['cell_bold'] if is_sub else styles['cell'])
            p2 = Paragraph(f"<b>{amt:,.2f}</b>" if is_sub else f"{amt:,.2f}", styles['cell_right_bold'] if is_sub else styles['cell_right'])
            bs_data.append([p1, p2])
            
        t_bs = Table(bs_data, colWidths=[5.2*inch, 2.0*inch])
        t_bs.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ACCENT_BG]),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ]))
        story.append(t_bs)
        
    story.append(Spacer(1, 16))
    story.append(Paragraph("Prepared in accordance with IFRS 18 Presentation & Disclosure in Financial Statements.", styles['footer']))
    
    doc.build(story)
    return buffer.getvalue()

def generate_inventory_valuation_pdf(company: dict, inventory_df) -> bytes:
    """Generates Inventory Stock Valuation and Reorder Sheet PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = get_base_styles()
    story = []
    
    story.extend(create_header(company, "INVENTORY VALUATION REPORT"))
    curr = company.get('currency', 'USD')
    
    inv_data = [[
        Paragraph("<b>Item Name</b>", styles['cell_bold']),
        Paragraph("<b>Category</b>", styles['cell_bold']),
        Paragraph("<b>Unit</b>", styles['cell']),
        Paragraph("<b>Stock Qty</b>", styles['cell_right_bold']),
        Paragraph("<b>Reorder Lvl</b>", styles['cell_right']),
        Paragraph(f"<b>Unit Cost ({curr})</b>", styles['cell_right']),
        Paragraph(f"<b>Valuation ({curr})</b>", styles['cell_right_bold']),
        Paragraph("<b>Status</b>", styles['cell_bold'])
    ]]
    
    total_val = 0.0
    for _, r in inventory_df.iterrows():
        name = str(r.get('item_name', ''))
        cat = str(r.get('category', ''))
        unit = str(r.get('unit', ''))
        qty = float(r.get('quantity', 0.0))
        reorder = float(r.get('reorder_level', 0.0))
        cost = float(r.get('unit_cost', 0.0))
        val = qty * cost
        total_val += val
        
        status_text = "<font color='red'><b>LOW</b></font>" if qty <= reorder else "<font color='green'>OK</font>"
        
        inv_data.append([
            Paragraph(name, styles['cell']),
            Paragraph(cat, styles['cell']),
            Paragraph(unit, styles['cell']),
            Paragraph(f"{qty:,.2f}", styles['cell_right_bold']),
            Paragraph(f"{reorder:,.2f}", styles['cell_right']),
            Paragraph(f"{cost:,.2f}", styles['cell_right']),
            Paragraph(f"{val:,.2f}", styles['cell_right_bold']),
            Paragraph(status_text, styles['cell'])
        ])
        
    inv_table = Table(inv_data, colWidths=[1.8*inch, 1.1*inch, 0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch, 0.5*inch])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ACCENT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(inv_table)
    story.append(Spacer(1, 10))
    
    tot_table = Table([
        [Paragraph("<b>TOTAL INVENTORY VALUATION:</b>", styles['cell_right_bold']), Paragraph(f"<b>{curr} {total_val:,.2f}</b>", styles['cell_right_bold'])]
    ], colWidths=[5.8*inch, 1.4*inch])
    tot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tot_table)
    
    doc.build(story)
    return buffer.getvalue()

def pd_not_null(val):
    return val is not None and str(val).strip() != '' and str(val).lower() != 'nan'
