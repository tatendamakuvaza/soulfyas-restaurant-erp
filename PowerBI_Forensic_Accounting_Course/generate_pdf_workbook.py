import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

PDF_PATH = "/home/user/soulfyas-restaurant-erp/PowerBI_Forensic_Accounting_Course/Forensic_Accounting_PowerBI_Workbook_Tatenda_Makuvaza.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        # We skip headers and footers on the cover page (Page 1)
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont('Helvetica-Bold', 7.5)
            self.setFillColor(colors.HexColor('#1E3A8A')) # Navy
            self.drawString(54, 754, "POWER BI FOR FORENSIC ACCOUNTING & AUDIT INTELLIGENCE")
            
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#64748B')) # Slate
            self.drawRightString(558, 754, "Course Participant: Tatenda Makuvaza")
            
            # Header rule
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.75)
            self.line(54, 746, 558, 746)
            
            # Running Footer
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.75)
            self.line(54, 46, 558, 46)
            
            self.setFont('Helvetica-Bold', 7)
            self.setFillColor(colors.HexColor('#991B1B')) # Crimson confidential flag
            self.drawString(54, 34, "CONFIDENTIAL & PROPRIETARY — FORENSIC AUDIT TRAINING DATASET")
            
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#475569'))
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 34, page_text)
            
            self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=56
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette
    NAVY = colors.HexColor('#1E3A8A')
    SLATE = colors.HexColor('#1E293B')
    MUTED = colors.HexColor('#64748B')
    CRIMSON = colors.HexColor('#991B1B')
    EMERALD = colors.HexColor('#065F46')
    BG_LIGHT = colors.HexColor('#F8FAFC')
    BORDER_LIGHT = colors.HexColor('#E2E8F0')
    BOX_ALERT_BG = colors.HexColor('#FEF2F2')
    BOX_TIP_BG = colors.HexColor('#F0FDF4')
    BOX_CODE_BG = colors.HexColor('#F1F5F9')

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        textColor=NAVY,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=MUTED,
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=SLATE,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'TaskH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=CRIMSON,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=SLATE,
        spaceAfter=3.5
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.2,
        textColor=colors.HexColor('#0F172A')
    )
    
    alert_box_style = ParagraphStyle(
        'AlertBoxStyle',
        parent=body_style,
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#7F1D1D')
    )

    tip_box_style = ParagraphStyle(
        'TipBoxStyle',
        parent=body_style,
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#064E3B')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=8.8,
        textColor=SLATE
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        fontSize=7.5,
        textColor=colors.white
    )

    def make_callout(text, box_type="alert", title=""):
        bg_col = BOX_ALERT_BG if box_type == "alert" else BOX_TIP_BG
        border_col = colors.HexColor('#F87171') if box_type == "alert" else colors.HexColor('#34D399')
        p_style = alert_box_style if box_type == "alert" else tip_box_style
        
        content = []
        if title:
            t_style = ParagraphStyle('CTitle', parent=p_style, fontName='Helvetica-Bold', fontSize=7.8, leading=9.8)
            content.append(Paragraph(f"<b>{title}</b>", t_style))
            content.append(Spacer(1, 1.5))
        content.append(Paragraph(text, p_style))
        
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_col),
            ('BOX', (0,0), (-1,-1), 0.75, border_col),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5.5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5.5),
        ]))
        return t

    def make_code_box(code_text):
        p = Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BOX_CODE_BG),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        return t

    story = []

    # =========================================================================
    # PAGE 1: COVER / TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("POWER BI FOR FORENSIC ACCOUNTING & AUDIT INTELLIGENCE", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Comprehensive Hands-On Masterclass, Practical Labs & Fraud Investigation Dossier", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8, spaceBefore=0))

    meta_data = [
        [Paragraph("<b>Course Participant:</b>", table_cell_bold), Paragraph("Tatenda Makuvaza (Forensic Accounting & Financial Audit Specialist)", table_cell)],
        [Paragraph("<b>Dataset & Corporation:</b>", table_cell_bold), Paragraph("Apex Horizon Global Corp — Audited ERP Ledgers (FY2024 - FY2025)", table_cell)],
        [Paragraph("<b>Relational Architecture:</b>", table_cell_bold), Paragraph("Star Schema: 5 Fact Tables, 6 Dimension Tables (25,830 Total Records)", table_cell)],
        [Paragraph("<b>Mathematical Verification:</b>", table_cell_bold), Paragraph("General Ledger Total Debits = $77,628,218.12 | Total Credits = $77,628,218.12 (Discrepancy: $0.00)", table_cell)],
        [Paragraph("<b>Embedded Fraud Scenarios:</b>", table_cell_bold), Paragraph("7 Engineered Fraud & Irregularity Cases ($1,412,297.51 Total Exposure)", table_cell)],
        [Paragraph("<b>Workbook Deliverables:</b>", table_cell_bold), Paragraph("25 Step-by-Step Hands-On Tasks, Forensic DAX Guide, and Answer Verification Key", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[130, 374])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    welcome_text = (
        "<b>Welcome, Tatenda Makuvaza!</b> This masterclass is specifically structured for forensic accountants who want to leverage "
        "Microsoft Power BI to build automated audit tools, detect fraudulent financial patterns, and perform rigorous forensic reviews. "
        "Rather than working with superficial sample files, you will work with a fully balanced, relational enterprise ledger containing "
        "General Ledger journal entries, Accounts Payable invoices, Accounts Receivable billing, Employee T&E reimbursements, and Bank Statements.<br/><br/>"
        "As you progress through the 25 hands-on lab tasks, you will uncover 7 active forensic audit anomalies, including split invoicing schemes, "
        "conflicts of interest with shell vendors, duplicate payment exploits, weekend manual journal plugs, fictitious expense claims, and unauthorized commercial discount leakage."
    )
    story.append(Paragraph(welcome_text, body_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Course Curriculum & Learning Roadmap:</b>", h2_style))
    toc_data = [
        [Paragraph("<b>Module / Chapter</b>", table_header), Paragraph("<b>Key Concepts & Learning Objectives</b>", table_header), Paragraph("<b>Tasks</b>", table_header)],
        [Paragraph("<b>Chapter 1: Forensic Data Architecture</b>", table_cell_bold), Paragraph("Star Schema Modeling, Fact vs Dimension tables, 1-to-many single direction filtering", table_cell), Paragraph("Overview", table_cell)],
        [Paragraph("<b>Chapter 2: Power Query ETL Labs</b>", table_cell_bold), Paragraph("Data Ingestion, type enforcement, whitespace trimming, off-hours flag engineering, entity matching", table_cell), Paragraph("Tasks 1–5", table_cell)],
        [Paragraph("<b>Chapter 3: Core Accounting DAX</b>", table_cell_bold), Paragraph("Trial Balance, Income Statement (P&L), Balance Sheet, Gross Margin, AR Aging, YoY Variance", table_cell), Paragraph("Tasks 6–10", table_cell)],
        [Paragraph("<b>Chapter 4: AP & Procurement Audit</b>", table_cell_bold), Paragraph("Split Invoicing (<$5k limit), Shell Vendor Bank Matching, Duplicate Invoices, PO Compliance", table_cell), Paragraph("Tasks 11–15", table_cell)],
        [Paragraph("<b>Chapter 5: GL & T&E Fraud Audit</b>", table_cell_bold), Paragraph("Weekend/Midnight Manual JEs, Unapproved Plugs, Fictitious T&E velocity, Benford's Law Analysis", table_cell), Paragraph("Tasks 16–20", table_cell)],
        [Paragraph("<b>Chapter 6: Commercial Revenue Fraud</b>", table_cell_bold), Paragraph("Quarter-End Quota Gaming, Unauthorized Discounts (>20%), Row-Level Security, Capstone Dashboard", table_cell), Paragraph("Tasks 21–25", table_cell)],
        [Paragraph("<b>Chapter 7: Forensic Evidence & Solutions</b>", table_cell_bold), Paragraph("Case Resolution Dossier ($1.41M Exposure), Full DAX Solution Library, Model Verification Matrix", table_cell), Paragraph("Solutions", table_cell)]
    ]
    toc_table = Table(toc_data, colWidths=[140, 314, 50])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: FORENSIC DATA ARCHITECTURE & STAR SCHEMA
    # =========================================================================
    story.append(Paragraph("Chapter 1: Forensic Data Architecture & Star Schema", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "In forensic auditing, single-table flat files are dangerous: they blend transactional event rows with entity attributes, "
        "leading to duplicated totals, slower DAX performance, and obscured audit trails. In Power BI, we implement a <b>Star Schema</b>, "
        "placing quantitative transactions in <b>Fact Tables</b> surrounded by descriptive lookup entities in <b>Dimension Tables</b>.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Enterprise Data Inventory (Located in the <code>/data/</code> Directory):</b>", h2_style))
    
    inv_data = [
        [Paragraph("<b>CSV File Name</b>", table_header), Paragraph("<b>Type</b>", table_header), Paragraph("<b>Rows</b>", table_header), Paragraph("<b>Key Column(s)</b>", table_header), Paragraph("<b>Audit Significance & Description</b>", table_header)],
        [Paragraph("<code>Dim_Date.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("731", table_cell), Paragraph("Date_Key, Date", table_cell), Paragraph("2024-2025 Calendar with Fiscal Periods, Quarter, and Is_Weekend flags.", table_cell)],
        [Paragraph("<code>Dim_Chart_of_Accounts.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("32", table_cell), Paragraph("Account_Number", table_cell), Paragraph("COA with Account Class, Subclass, Normal Balance, and Sensitive flag.", table_cell)],
        [Paragraph("<code>Dim_Cost_Centers.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("7", table_cell), Paragraph("Cost_Center_ID", table_cell), Paragraph("7 operating departments, heads of department, and FY24/25 budgets.", table_cell)],
        [Paragraph("<code>Dim_Employees.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("40", table_cell), Paragraph("Employee_ID", table_cell), Paragraph("Employee master with manager hierarchy, residential address, bank account, limits.", table_cell)],
        [Paragraph("<code>Dim_Vendors.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("50", table_cell), Paragraph("Vendor_ID", table_cell), Paragraph("Approved vendor list with Tax ID, bank account, payment terms, risk rating.", table_cell)],
        [Paragraph("<code>Dim_Customers.csv</code>", table_cell_bold), Paragraph("Dim", table_cell), Paragraph("50", table_cell), Paragraph("Customer_ID", table_cell), Paragraph("Client master across 5 regions with credit limits and industry sectors.", table_cell)],
        [Paragraph("<code>Fact_GL_Journal_Entries.csv</code>", table_cell_bold), Paragraph("Fact", table_cell), Paragraph("18,579", table_cell), Paragraph("Journal_ID, Line_ID", table_cell), Paragraph("Balanced double-entry journal ledger ($77.63M debits/credits).", table_cell)],
        [Paragraph("<code>Fact_Vendor_Invoices_AP.csv</code>", table_cell_bold), Paragraph("Fact", table_cell), Paragraph("1,734", table_cell), Paragraph("Invoice_ID", table_cell), Paragraph("AP invoices ($8.48M spend), PO match status, approver ID, payment terms.", table_cell)],
        [Paragraph("<code>Fact_Sales_Invoices_AR.csv</code>", table_cell_bold), Paragraph("Fact", table_cell), Paragraph("2,881", table_cell), Paragraph("Sales_Invoice_ID", table_cell), Paragraph("Customer invoices ($32.07M gross/net sales), discount amounts, rep IDs.", table_cell)],
        [Paragraph("<code>Fact_Employee_Expenses_TE.csv</code>", table_cell_bold), Paragraph("Fact", table_cell), Paragraph("1,833", table_cell), Paragraph("Expense_ID", table_cell), Paragraph("T&E reimbursement claims, merchants, receipt attachment flags.", table_cell)],
        [Paragraph("<code>Fact_Bank_Statements.csv</code>", table_cell_bold), Paragraph("Fact", table_cell), Paragraph("72", table_cell), Paragraph("Bank_Trans_ID", table_cell), Paragraph("Monthly treasury bank statement feed for cash account #1010 reconciliation.", table_cell)]
    ]
    
    inv_table = Table(inv_data, colWidths=[120, 32, 36, 110, 206])
    inv_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(inv_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Model View Relationship Map (All 1-to-Many Single-Direction Filtering):</b>", h2_style))
    
    rel_data = [
        [Paragraph("<b>Primary Dimension (1)</b>", table_header), Paragraph("<b>Target Fact Table (*)</b>", table_header), Paragraph("<b>Key Join Column</b>", table_header), Paragraph("<b>Cardinality & Direction</b>", table_header)],
        [Paragraph("<code>Dim_Date [Date]</code>", table_cell), Paragraph("<code>Fact_GL_Journal_Entries [Posting_Date]</code>", table_cell), Paragraph("Date → Posting_Date", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Date [Date]</code>", table_cell), Paragraph("<code>Fact_Vendor_Invoices_AP [Invoice_Date]</code>", table_cell), Paragraph("Date → Invoice_Date", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Date [Date]</code>", table_cell), Paragraph("<code>Fact_Sales_Invoices_AR [Invoice_Date]</code>", table_cell), Paragraph("Date → Invoice_Date", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Date [Date]</code>", table_cell), Paragraph("<code>Fact_Employee_Expenses_TE [Expense_Date]</code>", table_cell), Paragraph("Date → Expense_Date", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Chart_of_Accounts [Account_Number]</code>", table_cell), Paragraph("<code>Fact_GL_Journal_Entries [Account_Number]</code>", table_cell), Paragraph("Account_Number", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Cost_Centers [Cost_Center_ID]</code>", table_cell), Paragraph("<code>Fact_GL_Journal_Entries [Cost_Center_ID]</code>", table_cell), Paragraph("Cost_Center_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Cost_Centers [Cost_Center_ID]</code>", table_cell), Paragraph("<code>Fact_Vendor_Invoices_AP [Cost_Center_ID]</code>", table_cell), Paragraph("Cost_Center_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Vendors [Vendor_ID]</code>", table_cell), Paragraph("<code>Fact_Vendor_Invoices_AP [Vendor_ID]</code>", table_cell), Paragraph("Vendor_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Customers [Customer_ID]</code>", table_cell), Paragraph("<code>Fact_Sales_Invoices_AR [Customer_ID]</code>", table_cell), Paragraph("Customer_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Employees [Employee_ID]</code>", table_cell), Paragraph("<code>Fact_Employee_Expenses_TE [Employee_ID]</code>", table_cell), Paragraph("Employee_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)],
        [Paragraph("<code>Dim_Employees [Employee_ID]</code>", table_cell), Paragraph("<code>Fact_Sales_Invoices_AR [Sales_Rep_ID]</code>", table_cell), Paragraph("Employee_ID → Sales_Rep_ID", table_cell), Paragraph("1:* | Single (Dim → Fact)", table_cell)]
    ]
    
    rel_table = Table(rel_data, colWidths=[130, 140, 120, 114])
    rel_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(rel_table)
    story.append(Spacer(1, 4))

    alert_text = (
        "<b>Forensic Golden Rule:</b> Never enable Bi-Directional cross-filtering across multiple Fact tables. "
        "Bi-directional filtering creates ambiguity in filter propagation, degrades performance, and can generate artificial duplicate aggregations. "
        "Keep filter flows moving in one direction: from Dimension tables outward to Fact tables."
    )
    story.append(make_callout(alert_text, "alert", "CRITICAL MODELING STANDARD"))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: POWER QUERY ETL & DATA CLEANSING LABS (TASKS 1-5)
    # =========================================================================
    story.append(Paragraph("Chapter 2: Power Query (ETL) & Data Cleansing Labs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "In forensic investigations, raw source data cannot be trusted blindly. Fraudsters often manipulate whitespace, casing, "
        "and time stamps to evade automated controls. Perform these 5 essential ETL tasks in <b>Power Query Editor</b>:",
        body_style
    ))
    story.append(Spacer(1, 2))

    tasks_mod1 = [
        ("Task 1.1: Automated Folder Ingestion & Data Type Verification",
         "1. In Power BI Desktop, navigate to <b>Home > Get Data > Folder</b> and point to the <code>/data/</code> folder.<br/>"
         "2. Ensure all 11 tables are loaded. Verify that <code>Date</code> columns are typed as <b>Date</b>, dollar amounts as <b>Fixed Decimal Number ($)</b>, and Account Numbers (e.g., 1010, 2010) as <b>Text</b>.<br/>"
         "<i>Why is typing Account Numbers as Text critical?</i> (Prevents Power BI from accidentally summing account codes as numbers in visuals)."),

        ("Task 1.2: Mark Official Date Table & Build Chronological Hierarchies",
         "1. In Data View, select <code>Dim_Date</code>. In the ribbon, select <b>Table Tools > Mark as Date Table</b> with identifier <code>Date</code>.<br/>"
         "2. Select <code>Month_Name</code>, navigate to <b>Column Tools > Sort by Column</b>, and select <code>Month_Num</code>. This ensures calendar charts display months in proper chronological sequence rather than alphabetical order.<br/>"
         "3. Create a 4-level Date Hierarchy: <code>Fiscal_Year > Fiscal_Quarter > Month_Name > Date</code>."),

        ("Task 1.3: Forensic Whitespace Trimming (Exposing Duplicate Exploit)",
         "1. In Power Query Editor, open <code>Fact_Vendor_Invoices_AP</code>.<br/>"
         "2. Right-click the <code>Invoice_ID</code> column and select <b>Transform > Trim</b> and <b>Transform > Clean</b>.<br/>"
         "<b>Forensic Investigation Finding:</b> Notice invoice <code>AP-INV-92011 </code> contained a sneaky trailing space! Without trimming, traditional VLOOKUP or relational joins treat it as a distinct invoice, allowing a duplicate payment of <b>$19,750.50</b> to be processed unchecked."),

        ("Task 1.4: Feature Engineering — Off-Hours & Weekend Posting Flags",
         "1. In <code>Fact_GL_Journal_Entries</code>, split the <code>Posting_Timestamp</code> column by space delimiter into <code>Posting_Date_Only</code> and <code>Posting_Time</code>.<br/>"
         "2. Navigate to <b>Add Column > Custom Column</b> named <code>Is_Off_Hours_Posting</code> with the M formula:<br/>"
         "<code>if (Time.Hour([Posting_Time]) < 7 or Time.Hour([Posting_Time]) >= 19) or [Is_Weekend] = 1 then 1 else 0</code>.<br/>"
         "This flags all journal adjustments made late at night or over weekends for immediate forensic review."),

        ("Task 1.5: Cross-Entity Matching Merge (Employee vs. Vendor Master)",
         "1. In Power Query, select <b>Home > Merge Queries as New</b>.<br/>"
         "2. Select <code>Dim_Employees</code> on top and <code>Dim_Vendors</code> on the bottom, joining on <code>Bank_Account_Number</code> with an <b>Inner Join</b>.<br/>"
         "<b>Forensic Discovery Check:</b> Identify the exact employee and vendor match! (Employee <b>EMP-118 David Vance</b> and Vendor <b>VND-1038 Apex Global Consulting</b> share bank account <code>ACCT-US-908812</code> and residential address <code>742 Evergreen Terrace</code>).")
    ]

    for title, desc in tasks_mod1:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 1))

    tip_mod1 = (
        "<b>Power Query Audit Best Practice:</b> Always rename Applied Steps to reflect your investigative hypothesis "
        "(e.g., <code>Trimmed_AP_Invoice_Keys</code>, <code>Flagged_Off_Hours_Timestamps</code>, <code>Merged_Employee_Vendor_Bank_Match</code>). "
        "This ensures that court evidence and audit workpapers maintain a complete, reproducible chain of custody."
    )
    story.append(make_callout(tip_mod1, "tip", "AUDIT TRAIL BEST PRACTICE"))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: CORE FINANCIAL & ACCOUNTING DAX MEASURES (TASKS 6-10)
    # =========================================================================
    story.append(Paragraph("Chapter 3: Core Accounting & Financial DAX Formulas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "Create a dedicated blank measures table named <code>_Forensic_Measures</code> in Power BI Desktop (via <b>Enter Data</b>). "
        "Implement the following financial and double-entry accounting measures:",
        body_style
    ))
    story.append(Spacer(1, 2))

    core_dax_blocks = [
        ("1. Double-Entry Balance Validator Measures",
         "Total Debits = SUM(Fact_GL_Journal_Entries[Debit])\n"
         "Total Credits = SUM(Fact_GL_Journal_Entries[Credit])\n"
         "GL Net Discrepancy Check = [Total Debits] - [Total Credits]\n"
         "GL Balance Status = IF(ROUND([GL Net Discrepancy Check], 2) = 0, \"✅ BALANCED TO THE CENT\", \"🚨 IMBALANCE: \" & FORMAT([GL Net Discrepancy Check], \"$#,##0.00\"))"),

        ("2. Trial Balance Net Activity & P&L Core Metrics",
         "GL Net Activity = SUMX(Dim_Chart_of_Accounts, IF(Dim_Chart_of_Accounts[Normal_Balance] = \"Debit\", [Total Debits] - [Total Credits], [Total Credits] - [Total Debits]))\n"
         "Gross Commercial Revenue = SUM(Fact_Sales_Invoices_AR[Gross_Sales_Amount])\n"
         "Total Sales Discounts   = SUM(Fact_Sales_Invoices_AR[Discount_Amount])\n"
         "Net Sales Revenue       = SUM(Fact_Sales_Invoices_AR[Net_Sales_Amount])\n"
         "Total Cost of Goods Sold = SUM(Fact_Sales_Invoices_AR[Cost_of_Sales])\n"
         "Gross Profit             = [Net Sales Revenue] - [Total Cost of Goods Sold]\n"
         "Gross Margin %           = DIVIDE([Gross Profit], [Net Sales Revenue], 0)"),

        ("3. Operating Expenses & EBITDA Operating Income",
         "Total Operating Expenses = CALCULATE([Total Debits] - [Total Credits], Dim_Chart_of_Accounts[Account_Subclass] = \"Operating Expenses\")\n"
         "EBITDA Operating Income  = [Gross Profit] - [Total Operating Expenses]")
    ]

    for title, code_txt in core_dax_blocks:
        story.append(Paragraph(f"<b>{title}</b>", h3_style))
        story.append(make_code_box(code_txt))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Module 2 Hands-On Tasks (Financial Performance Dashboards):</b>", h2_style))

    tasks_mod2 = [
        ("Task 6: Interactive Double-Entry Trial Balance Matrix",
         "Build a Matrix visual with <code>Account_Class > Account_Subclass > Account_Name</code> on Rows. Add <code>[Total Debits]</code>, <code>[Total Credits]</code>, and <code>[GL Net Activity]</code> to Values.<br/>"
         "<b>Verification Checkpoint:</b> Confirm that Total Debits equal exactly <b>$77,628,218.12</b> and Total Credits equal <b>$77,628,218.12</b> (Discrepancy = $0.00)."),

        ("Task 7: Dynamic Income Statement (P&L) with YoY Growth",
         "Create a visual showing Net Sales Revenue ($32.07M), COGS ($16.61M), Gross Profit ($15.46M, 48.2%), and Operating Expenses.<br/>"
         "Add a DAX measure for <code>Net Revenue YoY %</code> comparing FY2025 to FY2024."),

        ("Task 8: Cost Center Budget vs. Actual Variance Gauge",
         "Create a Gauge visual comparing department actual spend against <code>Budget_FY24</code> and <code>Budget_FY25</code> from <code>Dim_Cost_Centers</code>. Which departments exceeded budget?"),

        ("Task 9: Accounts Receivable Aging & Bad Debt Exposure",
         "Build a 100% Stacked Bar chart breaking down outstanding AR invoices across aging buckets (Current, 1-30, 31-60, 61-90, 90+ days). Total bad debt written off = $42,100+."),

        ("Task 10: Vendor Spend Pareto Curve (80/20 Rule)",
         "Build a Line & Clustered Column Chart calculating cumulative spend % across vendors to identify the top 20% critical vendor concentration.")
    ]

    for title, desc in tasks_mod2:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: ACCOUNTS PAYABLE & PROCUREMENT FORENSIC AUDIT (TASKS 11-15)
    # =========================================================================
    story.append(Paragraph("Chapter 4: Accounts Payable & Procurement Forensic Audit", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "Procurement fraud accounts for over 30% of enterprise occupational fraud losses (ACFE Report to the Nations). "
        "In this module, you will write specialized forensic DAX measures to detect split purchases, ghost shell vendors, and duplicate billings.",
        body_style
    ))
    story.append(Spacer(1, 2))

    ap_dax_blocks = [
        ("Forensic DAX 1: Split Invoice Structuring Below Approval Limit ($5,000 Threshold)",
         "-- Detects invoices structured between $4,850 and $4,999 to bypass departmental VP authorization limit\n"
         "Count Split Invoices (<$5k Limit) = CALCULATE(COUNTROWS(Fact_Vendor_Invoices_AP), Fact_Vendor_Invoices_AP[Invoice_Amount] >= 4850, Fact_Vendor_Invoices_AP[Invoice_Amount] < 5000)\n"
         "Split Invoices Total Spend = CALCULATE(SUM(Fact_Vendor_Invoices_AP[Invoice_Amount]), Fact_Vendor_Invoices_AP[Invoice_Amount] >= 4850, Fact_Vendor_Invoices_AP[Invoice_Amount] < 5000)"),

        ("Forensic DAX 2: Potential Duplicate Payments Measure",
         "Duplicate Invoiced Spend = \n"
         "SUMX(\n"
         "    SUMMARIZE(Fact_Vendor_Invoices_AP, Fact_Vendor_Invoices_AP[Vendor_ID], Fact_Vendor_Invoices_AP[Invoice_Amount],\n"
         "              \"InvoiceCount\", COUNT(Fact_Vendor_Invoices_AP[Invoice_ID]), \"SumAmount\", SUM(Fact_Vendor_Invoices_AP[Invoice_Amount])),\n"
         "    IF([InvoiceCount] > 1, [SumAmount] - ([SumAmount] / [InvoiceCount]), 0)\n"
         ")")
    ]

    for title, code_txt in ap_dax_blocks:
        story.append(Paragraph(f"<b>{title}</b>", h3_style))
        story.append(make_code_box(code_txt))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Module 3 Practical Tasks (AP & Procurement Audit):</b>", h2_style))

    tasks_mod3 = [
        ("Task 11: Exposing the Split Invoicing Scheme (CloudSphere Solutions VND-1042)",
         "Filter <code>Fact_Vendor_Invoices_AP</code> for vendor <code>CloudSphere Solutions LLC (VND-1042)</code>.<br/>"
         "<b>Forensic Investigation Findings:</b> <b>48 invoices</b> totaling <b>$236,412.88</b> approved by <b>EMP-103 Marcus Brody</b> (VP Commercial Sales) structured between $4,853.11 and $4,992.47 to bypass Brody's $5,000 limit with 0 PO matching."),

        ("Task 12: Exposing Conflict of Interest & Shell Vendor (Apex Global Consulting VND-1038)",
         "In your data model, examine <code>Apex Global Consulting Ltd (VND-1038)</code>.<br/>"
         "<b>Forensic Investigation Findings:</b> <b>13 invoices</b> totaling <b>$266,129.04</b> paid with 0 PO. Created and approved by <b>EMP-118 David Vance</b> (Senior Procurement Officer), sharing identical bank account <code>ACCT-US-908812</code> and address <code>742 Evergreen Terrace</code>!"),

        ("Task 13: Detecting Duplicate Invoice Payments (Summit Logistics VND-1015)",
         "Create a Table visual filtered on <code>Vendor_ID = 'VND-1015'</code> displaying <code>Invoice_ID</code>, <code>Invoice_Date</code>, <code>Invoice_Amount</code>, and <code>Payment_Method</code>.<br/>"
         "<b>Forensic Discovery:</b> 4 duplicate invoice pairs paid twice ($18,450.00, $24,800.00, $19,750.50, $31,200.00) totaling <b>$94,200.50</b> in excess paid."),

        ("Task 14: Non-PO Emergency Disbursement Audit",
         "Calculate % of AP spend with <code>Is_PO_Matched = 'No'</code>. Supply Chain (CC-500) and Sales (CC-300) account for the vast majority of non-PO disbursements."),

        ("Task 15: Dynamic Vendor Fraud Risk Scorecard",
         "Create a calculated measure assigning a 1-100 Risk Score based on High Risk Rating (+30), Split Invoicing (+30), Non-PO Payments (+20), and Duplicate History (+20).")
    ]

    for title, desc in tasks_mod3:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: GENERAL LEDGER & T&E FRAUD AUDIT (TASKS 16-20)
    # =========================================================================
    story.append(Paragraph("Chapter 5: General Ledger & Travel Expense Fraud Audit", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "Manual journal entries and employee expense claims are primary vehicles used to conceal fraudulent disbursements and manipulate financial statements. "
        "Use Power BI to detect unauthorized weekend adjustments and fictitious expense velocity spikes.",
        body_style
    ))
    story.append(Spacer(1, 2))

    gl_dax_blocks = [
        ("Forensic DAX 3: Weekend & Off-Hours Manual Journal Adjustments",
         "-- Quantifies manual journal adjustments posted on weekends or between 20:00 and 06:00\n"
         "Weekend Manual JEs Total = CALCULATE(SUM(Fact_GL_Journal_Entries[Debit]), Fact_GL_Journal_Entries[Is_Manual] = 1, Dim_Date[Is_Weekend] = 1)\n"
         "Unapproved Suspicious Adjustments = CALCULATE(SUM(Fact_GL_Journal_Entries[Debit]), Fact_GL_Journal_Entries[Is_Manual] = 1, ISBLANK(Fact_GL_Journal_Entries[Approved_By]) || Fact_GL_Journal_Entries[Approved_By] = \"\")"),

        ("Forensic DAX 4: Missing Receipt Rate in Travel & Entertainment (T&E)",
         "Missing Receipt Claims Amount = CALCULATE(SUM(Fact_Employee_Expenses_TE[Claim_Amount]), Fact_Employee_Expenses_TE[Receipt_Attached] = \"No\")\n"
         "Missing Receipt % = DIVIDE([Missing Receipt Claims Amount], SUM(Fact_Employee_Expenses_TE[Claim_Amount]), 0)")
    ]

    for title, code_txt in gl_dax_blocks:
        story.append(Paragraph(f"<b>{title}</b>", h3_style))
        story.append(make_code_box(code_txt))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Module 4 Practical Tasks (GL & T&E Investigation):</b>", h2_style))

    tasks_mod4 = [
        ("Task 16: Weekend & Off-Hours Manual Journal Entry Investigation",
         "Filter <code>Fact_GL_Journal_Entries</code> for <code>Is_Manual = 1</code> and <code>Dim_Date [Is_Weekend] = 1</code>.<br/>"
         "<b>Forensic Findings:</b> <b>8 unique manual entries</b> debited exactly <b>$533,000.00</b>, posted by <b>EMP-105 Elena Rostova</b> on Saturday nights (23:35-23:55) with <b>blank approvers</b>!"),

        ("Task 17: Deep-Dive Audit of Account 9100 (Miscellaneous Expense)",
         "Drill down into Account <code>9100 (Miscellaneous & Sundry Expense)</code>. Notice round-dollar debit spikes ($45k, $62k, $78k, $49k, $67k, $95k) offsetting cash account 1010."),

        ("Task 18: Exposing Fictitious T&E Claims Velocity Spike (Julian Thorne EMP-129)",
         "In <code>Fact_Employee_Expenses_TE</code>, create a Matrix with <code>Employee_ID</code> on Rows, and <code>Claim Count</code>, <code>Total Amount</code>, and <code>Missing Receipt Count</code>.<br/>"
         "<b>Forensic Findings:</b> Julian Thorne submitted <b>208 claims totaling $30,410.19</b> on consecutive weekends with <b>100% missing receipts</b> structured between $142.50 and $149.95 to evade the mandatory $150 receipt rule!"),

        ("Task 19: Benford's Law First-Digit Distribution Visual",
         "Create a Bar Chart displaying the frequency distribution of the first digit (1-9) of GL expense debits compared to Benford's Law theoretical benchmarks (Digit 1 = 30.1%, Digit 2 = 17.6%). Account 9100 exhibits massive artificial clustering in digits 4, 6, and 7."),

        ("Task 20: GL to Bank Treasury Cash Reconciliation",
         "Build a reconciliation matrix comparing <code>Fact_Bank_Statements</code> monthly net deposits/withdrawals against General Ledger cash account <code>1010</code>. Verify that unreconciled timing differences are flagged automatically.")
    ]

    for title, desc in tasks_mod4:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: COMMERCIAL REVENUE FRAUD & CAPSTONE DASHBOARD (TASKS 21-25)
    # =========================================================================
    story.append(Paragraph("Chapter 6: Commercial Revenue Fraud & Capstone Dashboard", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "Commercial revenue fraud often involves sales reps offering unauthorized steep discounts to reach commission quotas or collude with favored buyers. "
        "In this module, you will quantify commercial margin leakage, establish Row-Level Security, and build the Executive Capstone Dashboard.",
        body_style
    ))
    story.append(Spacer(1, 2))

    rev_dax_blocks = [
        ("Forensic DAX 5: Unauthorized High-Discount Margin Leakage",
         "-- Quantifies total revenue lost to sales discounts exceeding the 15% corporate maximum policy\n"
         "Unauthorized High Discounts Amount = CALCULATE(SUM(Fact_Sales_Invoices_AR[Discount_Amount]), Fact_Sales_Invoices_AR[Discount_Percentage] > 0.15)\n"
         "High Discount Invoices Count = CALCULATE(COUNTROWS(Fact_Sales_Invoices_AR), Fact_Sales_Invoices_AR[Discount_Percentage] > 0.15)")
    ]

    for title, code_txt in rev_dax_blocks:
        story.append(Paragraph(f"<b>{title}</b>", h3_style))
        story.append(make_code_box(code_txt))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Module 5 Practical Tasks & Capstone Build:</b>", h2_style))

    tasks_mod5 = [
        ("Task 21: Sales Rep Discount Policy Deviation (Rachel Zane EMP-133)",
         "Build a Scatter Plot with Sales Reps on Details, <code>Gross Sales</code> on X-Axis, and <code>Average Discount %</code> on Y-Axis.<br/>"
         "<b>Forensic Findings:</b> While company sales reps average a <b>3.1%</b> discount rate, <b>Rachel Zane (EMP-133)</b> averages <b>7.4%</b> overall and has <b>55 invoices</b> with extreme discounts exceeding 20%."),

        ("Task 22: Correlating Quarter-End Timing with Extreme Discounts",
         "Plot Rachel Zane's discount percentages over time on a Line Chart with <code>Dim_Date [Date]</code>.<br/>"
         "Notice the unmistakable surge in discounts (30% to 42%) occurring exclusively in the final 10 days of Q1 (March), Q2 (June), Q3 (September), and Q4 (December) — classic quota manipulation!"),

        ("Task 23: Commercial Margin Leakage Dollar Impact",
         "Calculate the total net revenue lost to Rachel Zane's unauthorized discount spikes. Total high-discount loss = <b>$252,144.90</b>."),

        ("Task 24: Enterprise Row-Level Security (RLS) Configuration",
         "In Power BI Desktop ribbon, navigate to <b>Modeling > Manage Roles</b>. Create two roles:<br/>"
         "1. <b>Department_Manager:</b> DAX Filter on <code>Dim_Cost_Centers</code>: <code>[Cost_Center_ID] = USERPRINCIPALNAME()</code>.<br/>"
         "2. <b>Forensic_Auditor:</b> No filter (full unrestricted visibility across all 11 tables).<br/>"
         "Test the roles using <b>View as Roles</b> to ensure security rules enforce strict segregation."),

        ("Task 25: Master Forensic Intelligence Capstone Dashboard",
         "Construct a publication-grade, 4-page Power BI Dashboard report:<br/>"
         "• <b>Page 1: Executive Audit Summary:</b> KPI Cards for Total Debits/Credits, Net Sales, Total AP, and Discovered Fraud Exposure ($1.41M).<br/>"
         "• <b>Page 2: Accounts Payable Fraud Engine:</b> Split invoice scatter plot, Shell vendor bank match table, Duplicate invoice tracker.<br/>"
         "• <b>Page 3: General Ledger Journal Anomaly Matrix:</b> Weekend/Off-hours heatmap, Account 9100 drill-down, Benford's Law bar chart.<br/>"
         "• <b>Page 4: T&E & Commercial Leakage:</b> Sales rep discount outliers, Julian Thorne weekend expense velocity tracker.")
    ]

    for title, desc in tasks_mod5:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 1))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: FORENSIC AUDIT EVIDENCE REPORT & CASE DOSSIER
    # =========================================================================
    story.append(Paragraph("Chapter 7: Forensic Audit Evidence Summary & Case Dossier", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "The following forensic investigation dossier summarizes the 7 fraud and irregularity schemes uncovered across Apex Horizon Global Corp. "
        "Use this evidence table to verify your analytical findings and prepare executive audit briefs.",
        body_style
    ))
    story.append(Spacer(1, 2))

    fraud_summary_data = [
        [Paragraph("<b>Scheme & Case Name</b>", table_header), Paragraph("<b>Key Perpetrator(s)</b>", table_header), Paragraph("<b>Financial Exposure</b>", table_header), Paragraph("<b>Audit Evidence Trail & Modus Operandi</b>", table_header)],
        [
            Paragraph("<b>Case 1: Split Invoicing Structuring</b>", table_cell_bold),
            Paragraph("Marcus Brody<br/>(EMP-103, VP Sales)", table_cell),
            Paragraph("<b>$236,412.88</b><br/>(48 Invoices)", table_cell),
            Paragraph("Invoices from CloudSphere Solutions (VND-1042) billed at $4,850-$4,995 in rapid 2-day clusters to bypass Brody's $5,000 approval limit. Zero formal PO matching.", table_cell)
        ],
        [
            Paragraph("<b>Case 2: Ghost Shell Vendor & Conflict of Interest</b>", table_cell_bold),
            Paragraph("David Vance<br/>(EMP-118, Procurement)", table_cell),
            Paragraph("<b>$266,129.04</b><br/>(13 Invoices)", table_cell),
            Paragraph("David Vance registered shell company Apex Global Consulting (VND-1038) using his personal residence (742 Evergreen Terr) and bank account (ACCT-US-908812). Billed vague advisory retainers with immediate terms.", table_cell)
        ],
        [
            Paragraph("<b>Case 3: Duplicate Invoices & Overpayments</b>", table_cell_bold),
            Paragraph("Summit Logistics<br/>(VND-1015)", table_cell),
            Paragraph("<b>$94,200.50</b><br/>(4 Duplicate Pairs)", table_cell),
            Paragraph("Duplicate freight invoices submitted with slight variations (trailing spaces, 'DUP' and 'A' suffixes) paid twice via EFT and Check runs.", table_cell)
        ],
        [
            Paragraph("<b>Case 4: Off-Hours Manual Journal Plugs</b>", table_cell_bold),
            Paragraph("Elena Rostova<br/>(EMP-105, Senior GL)", table_cell),
            Paragraph("<b>$533,000.00</b><br/>(8 Manual JEs)", table_cell),
            Paragraph("Manual journal entries posted on Saturday nights (23:35-23:55) debiting Account 9100 (Miscellaneous) and crediting Operating Cash (1010). No manager approval attached.", table_cell)
        ],
        [
            Paragraph("<b>Case 5: Fictitious Weekend T&E Claims</b>", table_cell_bold),
            Paragraph("Julian Thorne<br/>(EMP-129, Sales Rep)", table_cell),
            Paragraph("<b>$30,410.19</b><br/>(208 Claims)", table_cell),
            Paragraph("208 consecutive weekend dining/lounge claims submitted at $142-$149.95 to stay just below the mandatory $150 receipt audit rule. 100% missing receipts.", table_cell)
        ],
        [
            Paragraph("<b>Case 6: Unauthorized High Discounts</b>", table_cell_bold),
            Paragraph("Rachel Zane<br/>(EMP-133, Key Accounts)", table_cell),
            Paragraph("<b>$252,144.90</b><br/>(55 Invoices > 20%)", table_cell),
            Paragraph("Applied unauthorized discounts of 30% to 42% at quarter-ends (March, June, Sept, Dec) to artificially inflate volume and achieve performance bonus thresholds.", table_cell)
        ],
        [
            Paragraph("<b>TOTAL FINANCIAL EXPOSURE IDENTIFIED</b>", table_cell_bold),
            Paragraph("<b>Multiple Internal Actors</b>", table_cell_bold),
            Paragraph("<b>$1,412,297.51</b>", table_cell_bold),
            Paragraph("Comprehensive internal control failure requiring immediate CFO notification, vendor freeze, and internal control segregation of duties (SoD) redesign.", table_cell)
        ]
    ]

    fraud_table = Table(fraud_summary_data, colWidths=[110, 85, 85, 224])
    fraud_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,-1), (-1,-1), BOX_ALERT_BG),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(fraud_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Recommended Internal Control & Governance Remediation Actions:</b>", h2_style))
    story.append(Paragraph("1. <b>Automated SoD & Dual Approval Limits:</b> Implement hard system locks preventing cost center managers from approving invoices within 10% of their authorization threshold without secondary VP sign-off.", bullet_style))
    story.append(Paragraph("2. <b>ERP Master Data Matching:</b> Establish automated nightly cross-join checks between the Employee bank account / residential address database and Vendor master records.", bullet_style))
    story.append(Paragraph("3. <b>Strict 3-Way Matching:</b> Mandate 3-way matching (PO, Receiving Report, Invoice) for all service and consulting invoices exceeding $2,500.", bullet_style))
    story.append(Paragraph("4. <b>GL Posting Window Locks:</b> Restrict manual General Ledger posting privileges to weekdays between 07:00 and 19:00, requiring explicit dual-key CFO approval for off-hours adjustments.", bullet_style))
    story.append(Paragraph("5. <b>Zero-Receipt T&E Rejection:</b> Enforce automatic rejection for any expense claim lacking an attached itemized digital receipt, regardless of dollar threshold.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 8: DAX SOLUTIONS & MODEL VERIFICATION KEY
    # =========================================================================
    story.append(Paragraph("Chapter 8: DAX Solutions & Model Verification Key", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5, spaceBefore=0))
    
    story.append(Paragraph(
        "Use this complete solution dictionary and verification matrix to validate your Power BI calculations against the mathematical ground truth:",
        body_style
    ))
    story.append(Spacer(1, 2))

    sol_key_data = [
        [Paragraph("<b>Metric / Measure Name</b>", table_header), Paragraph("<b>Expected Value / Ground Truth</b>", table_header), Paragraph("<b>Verification Visual & Filter Context</b>", table_header)],
        [Paragraph("GL Total Debits", table_cell_bold), Paragraph("<b>$77,628,218.12</b>", table_cell), Paragraph("Card visual: <code>SUM(Fact_GL_Journal_Entries[Debit])</code>", table_cell)],
        [Paragraph("GL Total Credits", table_cell_bold), Paragraph("<b>$77,628,218.12</b>", table_cell), Paragraph("Card visual: <code>SUM(Fact_GL_Journal_Entries[Credit])</code>", table_cell)],
        [Paragraph("GL Net Discrepancy", table_cell_bold), Paragraph("<b>$0.00 (Balanced)</b>", table_cell), Paragraph("Card visual: <code>[Total Debits] - [Total Credits]</code>", table_cell)],
        [Paragraph("Total Net Sales Revenue", table_cell_bold), Paragraph("<b>$32,066,469.23</b>", table_cell), Paragraph("Card visual: <code>SUM(Fact_Sales_Invoices_AR[Net_Sales_Amount])</code>", table_cell)],
        [Paragraph("Total Cost of Goods Sold", table_cell_bold), Paragraph("<b>$16,605,945.19</b>", table_cell), Paragraph("Card visual: <code>SUM(Fact_Sales_Invoices_AR[Cost_of_Sales])</code>", table_cell)],
        [Paragraph("Gross Profit ($ and %)", table_cell_bold), Paragraph("<b>$15,460,524.04 (48.2%)</b>", table_cell), Paragraph("Card visual: <code>[Net Sales Revenue] - [Total COGS]</code>", table_cell)],
        [Paragraph("Total AP Invoiced Spend", table_cell_bold), Paragraph("<b>$8,476,029.18</b> (1,734 invs)", table_cell), Paragraph("Matrix visual: <code>SUM(Fact_Vendor_Invoices_AP[Invoice_Amount])</code>", table_cell)],
        [Paragraph("CloudSphere Split Invoices", table_cell_bold), Paragraph("<b>$236,412.88</b> (48 invs)", table_cell), Paragraph("Filter AP on <code>Vendor_ID = 'VND-1042'</code>", table_cell)],
        [Paragraph("Apex Global Shell Vendor", table_cell_bold), Paragraph("<b>$266,129.04</b> (13 invs)", table_cell), Paragraph("Filter AP on <code>Vendor_ID = 'VND-1038'</code>", table_cell)],
        [Paragraph("Summit Logistics Excess Duplicates", table_cell_bold), Paragraph("<b>$94,200.50</b> (4 pairs)", table_cell), Paragraph("Filter AP on <code>Vendor_ID = 'VND-1015'</code> duplicate amounts", table_cell)],
        [Paragraph("Off-Hours Manual JEs", table_cell_bold), Paragraph("<b>$533,000.00</b> (8 journals)", table_cell), Paragraph("Filter GL on <code>Is_Manual = 1</code> & <code>Is_Weekend = 1</code>", table_cell)],
        [Paragraph("Julian Thorne Fake T&E", table_cell_bold), Paragraph("<b>$30,410.19</b> (208 claims)", table_cell), Paragraph("Filter TE on <code>Employee_ID = 'EMP-129'</code>", table_cell)],
        [Paragraph("Rachel Zane Excess Discounts", table_cell_bold), Paragraph("<b>$252,144.90</b> (55 invs > 20%)", table_cell), Paragraph("Filter AR on <code>Sales_Rep_ID = 'EMP-133'</code> & disc > 20%", table_cell)],
        [Paragraph("Total Discovered Fraud Exposure", table_cell_bold), Paragraph("<b>$1,412,297.51</b>", table_cell), Paragraph("Sum of all 6 forensic exposure measures", table_cell)]
    ]

    sol_table = Table(sol_key_data, colWidths=[150, 140, 214])
    sol_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(sol_table)
    story.append(Spacer(1, 6))

    concl_box = (
        "<b>Congratulations on Completing the Masterclass, Tatenda!</b><br/>"
        "By completing this workbook and building the complete Power BI Forensic Audit Model, you have mastered the transition "
        "from traditional audit procedures to modern, automated forensic data analytics. You now possess the skills to model complex "
        "financial schemas, write advanced forensic DAX expressions, and build interactive intelligence dashboards that safeguard enterprise assets."
    )
    story.append(make_callout(concl_box, "tip", "PROFESSIONAL ATTAINMENT"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
