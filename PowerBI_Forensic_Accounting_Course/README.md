# Power BI for Forensic Accounting & Audit Intelligence
### Masterclass Course Workbook & Hands-On Lab Dataset
**Personalized for:** Tatenda Makuvaza  
**Target Domain:** Forensic Accounting, Financial Auditing, Enterprise Fraud Analytics & Power BI Data Modeling  
**Dataset Time Horizon:** FY2024 – FY2025 (2 Full Calendar & Fiscal Years)  
**Total Dataset Records:** 25,830 Transactions & Dimension Entities  

---

## 🎯 Course Overview & Learning Objectives

Welcome, **Tatenda Makuvaza**! This course is custom-built to elevate your forensic accounting expertise into advanced business intelligence and automated audit analytics using **Microsoft Power BI**. 

In corporate auditing and forensic investigations, relying on traditional spreadsheet sampling is no longer sufficient. Enterprise fraudsters conceal illicit transactions through split purchases, off-hours postings, fictitious vendors, rubber-stamped expense claims, and unauthorized margin discounts. With Power BI, you will learn to build a high-performance **Relational Star Schema**, write advanced **Forensic DAX Measures**, design **Dynamic Audit Matrix Reports**, and construct an **Executive Forensic Intelligence Dashboard**.

---

## 📂 Folder & Deliverable Structure

```
PowerBI_Forensic_Accounting_Course/
│
├── Forensic_Accounting_PowerBI_Workbook_Tatenda_Makuvaza.pdf  <-- 📄 MASTER COURSE WORKBOOK (PDF)
├── README.md                                                   <-- 📖 This Course Guide
├── Data_Dictionary.md                                          <-- 📊 Comprehensive Table & Column Dictionary
├── DAX_Formulas_Guide.md                                       <-- ⚡ Ready-to-use DAX Formulas (Copy & Paste)
├── Forensic_Audit_Evidence_Key.md                              <-- 🔍 7 Fraud Cases Dossier & Solution Key
│
├── data/                                                       <-- 📁 Raw Relational CSV Datasets (11 Tables)
│   ├── Dim_Date.csv                                            (731 rows - Master Date Table)
│   ├── Dim_Chart_of_Accounts.csv                               (32 rows - Master Chart of Accounts)
│   ├── Dim_Cost_Centers.csv                                    (7 rows - Departmental Cost Centers & Budgets)
│   ├── Dim_Employees.csv                                       (40 rows - Employee Profiles, Limits & Addresses)
│   ├── Dim_Vendors.csv                                         (50 rows - Vendor Master & Bank Details)
│   ├── Dim_Customers.csv                                       (50 rows - Enterprise Customers & Terms)
│   ├── Fact_GL_Journal_Entries.csv                             (18,579 rows - General Ledger Double-Entry)
│   ├── Fact_Vendor_Invoices_AP.csv                             (1,734 rows - Accounts Payable Spend)
│   ├── Fact_Sales_Invoices_AR.csv                              (2,881 rows - Accounts Receivable Revenue)
│   ├── Fact_Employee_Expenses_TE.csv                           (1,833 rows - Travel & Entertainment Reimbursements)
│   └── Fact_Bank_Statements.csv                                (72 rows - Monthly Treasury Bank Statements)
│
├── generate_data.py                                            (Data Generation Engine)
├── generate_pdf_workbook.py                                    (PDF Publication Engine)
└── verify_stats.py                                             (Automated Ground Truth Verification)
```

---

## 🏗️ Relational Star Schema Architecture

In Power BI Desktop **Model View**, establish the following **1-to-Many (1:*)** relationships with **Single Direction Filtering** (Dimension filters Fact):

```
                   +---------------------------+
                   |         Dim_Date          |
                   +---------------------------+
                     /      |            |    \
           (1:*)    / (1:*) |      (1:*) |     \ (1:*)
                   /        |            |      \
+--------------------+ +----+---------------+ +-+------------------+ +--------------------+
| Fact_GL_Journal    | | Fact_Vendor_       | | Fact_Sales_        | | Fact_Employee_     |
| Entries (GL)       | | Invoices_AP (AP)   | | Invoices_AR (AR)   | | Expenses_TE (T&E)  |
+--------------------+ +--------------------+ +--------------------+ +--------------------+
      |       |            |                      |                      |
(1:*) | (1:*) |      (1:*) |                (1:*) |                (1:*) |
      |       |            |                      |                      |
+-----+---+ +-+----------+ +---+------------+ +---+------------+ +-------+------------+
| Dim_    | | Dim_Cost_  | | Dim_Vendors    | | Dim_Customers  | | Dim_Employees      |
| COA     | | Centers    | +----------------+ +----------------+ +--------------------+
+---------+ +------------+
```

### 🔗 Relationship Configuration Table:

| From Dimension (1) | To Fact Table (*) | Primary Key → Foreign Key | Filtering Direction |
|---|---|---|---|
| `Dim_Date` | `Fact_GL_Journal_Entries` | `Date` → `Posting_Date` | Single (`Dim_Date` filters Fact) |
| `Dim_Date` | `Fact_Vendor_Invoices_AP` | `Date` → `Invoice_Date` | Single (`Dim_Date` filters Fact) |
| `Dim_Date` | `Fact_Sales_Invoices_AR` | `Date` → `Invoice_Date` | Single (`Dim_Date` filters Fact) |
| `Dim_Date` | `Fact_Employee_Expenses_TE` | `Date` → `Expense_Date` | Single (`Dim_Date` filters Fact) |
| `Dim_Chart_of_Accounts` | `Fact_GL_Journal_Entries` | `Account_Number` → `Account_Number` | Single (`Dim_COA` filters Fact) |
| `Dim_Cost_Centers` | `Fact_GL_Journal_Entries` | `Cost_Center_ID` → `Cost_Center_ID` | Single (`Dim_Cost_Centers` filters Fact) |
| `Dim_Cost_Centers` | `Fact_Vendor_Invoices_AP` | `Cost_Center_ID` → `Cost_Center_ID` | Single (`Dim_Cost_Centers` filters Fact) |
| `Dim_Vendors` | `Fact_Vendor_Invoices_AP` | `Vendor_ID` → `Vendor_ID` | Single (`Dim_Vendors` filters Fact) |
| `Dim_Customers` | `Fact_Sales_Invoices_AR` | `Customer_ID` → `Customer_ID` | Single (`Dim_Customers` filters Fact) |
| `Dim_Employees` | `Fact_Employee_Expenses_TE` | `Employee_ID` → `Employee_ID` | Single (`Dim_Employees` filters Fact) |
| `Dim_Employees` | `Fact_Sales_Invoices_AR` | `Employee_ID` → `Sales_Rep_ID` | Single (`Dim_Employees` filters Fact) |

---

## ⚡ Quick-Start Step-by-Step Instructions

1. **Launch Power BI Desktop**.
2. Click **Get Data > Folder** (or **Text/CSV**) and select the `data/` folder.
3. In **Power Query Editor**:
   - Verify data types: Amounts = `Fixed Decimal Number ($)`, Dates = `Date`, IDs & Account Numbers = `Text`.
   - Apply **Transform > Format > Trim** to `Fact_Vendor_Invoices_AP[Invoice_ID]`.
   - Add Custom Column `Is_Off_Hours_Posting` in `Fact_GL_Journal_Entries`.
   - Click **Close & Apply**.
4. In **Model View**: Establish the 11 active relationships as shown above.
5. In **Data View**: Select `Dim_Date`, click **Table Tools > Mark as Date Table**, and select `Date`.
6. Click **Enter Data** to create a dedicated measures table: `_Forensic_Measures`.
7. Copy and paste measures from `DAX_Formulas_Guide.md`.
8. Complete the **25 Hands-On Tasks** described in the master PDF workbook.
9. Verify your final metrics against `Forensic_Audit_Evidence_Key.md`.

---

## 🚨 Embedded Forensic Investigation Highlights

| Case | Forensic Anomaly Scheme | Key Actor | Exposure ($) | Modus Operandi |
|---|---|---|---|---|
| **Case 1** | Split Invoicing Under Limit | Marcus Brody (EMP-103) | **$236,412.88** | 48 invoices from CloudSphere Solutions billed between $4,850 and $4,995 to bypass $5,000 threshold. |
| **Case 2** | Conflict of Interest / Shell Vendor | David Vance (EMP-118) | **$266,129.04** | Created shell vendor Apex Global Consulting sharing Vance's home address & bank account. |
| **Case 3** | Duplicate Payments & Whitespace | Summit Logistics (VND-1015) | **$94,200.50** | Duplicate invoices with trailing whitespace and suffix variations paid twice. |
| **Case 4** | Weekend Manual Journal Plugs | Elena Rostova (EMP-105) | **$533,000.00** | $533k debited to Acct 9100/6030 on Saturday nights (23:35-23:55) with blank manager approvals. |
| **Case 5** | Fictitious Weekend T&E Spikes | Julian Thorne (EMP-129) | **$30,410.19** | 208 weekend meal claims submitted at $142-$149.95 with 0 receipts attached. |
| **Case 6** | Quarter-End Quota Gaming | Rachel Zane (EMP-133) | **$252,144.90** | 30% to 42% unauthorized discounts applied at the end of Q1, Q2, Q3, and Q4. |
| **TOTAL** | **Enterprise Financial Loss Identified** | **Multiple Actors** | **$1,412,297.51** | Comprehensive internal control collapse requiring immediate executive remediation. |

---

## 🏆 Key Milestones for Tatenda Makuvaza
- [x] Ingest & Model Relational Star Schema in Power BI
- [x] Build Automated Double-Entry Balance Validator ($77,628,218.12 Debits = Credits)
- [x] Construct Trial Balance & Financial Income Statement (48.2% Gross Margin)
- [x] Uncover the 6 Occupational Fraud Schemes & Quantify $1.41M Financial Exposure
- [x] Implement Row-Level Security (RLS) for Segregation of Duties
- [x] Publish the Executive Forensic Intelligence Capstone Dashboard
