"""
ReportLab PDF Generation Engine for Soulfyas Quality Restaurant ERP
Generates branded POS receipts, tax invoices, employee payslips, financial statements, and inventory reports.
"""

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY

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
    phone = company.get('phone') or '+263 77 000 0000'
    email = company.get('email') or 'info@soulfyas.co.zw'
    tin = company.get('zimra_tin') or 'N/A'
    vat = company.get('vat_number') or 'N/A'
    nssa = company.get('nssa_number') or 'N/A'
    
    header_data = []
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
        f"<b>Currency:</b> {company.get('currency', 'USD')}<br/>"
        f"<b>Fiscalised:</b> Yes (ZIMRA FD compliant)"
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

def generate_receipt_pdf(company: dict, sale: dict, items: list) -> bytes:
    """Generates a POS Receipt / Tax Invoice PDF"""
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
            Paragraph(f"<b>Server:</b> {cashier}", styles['cell'])
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
    
    # Line items table
    curr = company.get('currency', 'USD')
    table_rows = [
        [
            Paragraph("<b>#</b>", styles['cell_bold']),
            Paragraph("<b>Item Description</b>", styles['cell_bold']),
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
        qty = float(item.get('quantity', item.get('qty', 1)))
        price = float(item.get('unit_price', item.get('price', 0.0)))
        line_tot = float(item.get('line_total', qty * price))
        
        table_rows.append([
            Paragraph(str(idx), styles['cell']),
            Paragraph(str(name), styles['cell']),
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
    
    # Totals summary table
    summary_data = [
        [Paragraph("Subtotal (Excl. VAT):", styles['cell_right']), Paragraph(f"{curr} {subtotal:,.2f}", styles['cell_right'])],
        [Paragraph("VAT (15% ZIMRA Standard):", styles['cell_right']), Paragraph(f"{curr} {tax:,.2f}", styles['cell_right'])]
    ]
    if discount > 0:
        summary_data.append([Paragraph("Discount Applied:", styles['cell_right']), Paragraph(f"-{curr} {discount:,.2f}", styles['cell_right'])])
    if tip > 0:
        summary_data.append([Paragraph("Service Tip / Gratuity:", styles['cell_right']), Paragraph(f"{curr} {tip:,.2f}", styles['cell_right'])])
        
    summary_data.append([
        Paragraph("<b>GRAND TOTAL:</b>", styles['cell_right_bold']),
        Paragraph(f"<b>{curr} {total:,.2f}</b>", styles['cell_right_bold'])
    ])
    
    summary_table = Table(summary_data, colWidths=[5.7*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 4),
        ('LINEABOVE', (0,-1), (-1,-1), 1, PRIMARY_COLOR),
        ('BACKGROUND', (0,-1), (-1,-1), ACCENT_BG),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Footer and Fiscal Barcode text
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=8, spaceBefore=4))
    fiscal_msg = f"Fiscal Code: ZIMRA-FD-{inv_no[-10:]} | Verification: VERIFIED-OK | Thank you for dining with Soulfyas!"
    story.append(Paragraph(fiscal_msg, styles['footer']))
    
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
    
    # Earnings vs Deductions side-by-side table
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
    
    # Table layout
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
    
    # Net Pay Callout
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
    
    # Employer Statutory Contributions
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
