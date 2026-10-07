# Power BI Forensic Accounting — Complete DAX Formula Library
### Ready-to-Use Data Analysis Expressions (DAX)
**Author:** Forensic Data Analytics Curriculum Team  
**Participant:** Tatenda Makuvaza  
**Target Table in Power BI:** `_Forensic_Measures` (Recommended dedicated measure table)  

---

## 1. General Ledger & Double-Entry Integrity Measures

```dax
// Measure 1: Total General Ledger Debits
Total Debits = 
SUM(Fact_GL_Journal_Entries[Debit])

// Measure 2: Total General Ledger Credits
Total Credits = 
SUM(Fact_GL_Journal_Entries[Credit])

// Measure 3: GL Balance Discrepancy Check (Should equal $0.00)
GL Net Discrepancy Check = 
[Total Debits] - [Total Credits]

// Measure 4: Dynamic GL Health KPI Card
GL Balance Status = 
IF(
    ROUND([GL Net Discrepancy Check], 2) = 0,
    "✅ BALANCED TO THE CENT",
    "🚨 IMBALANCE: " & FORMAT([GL Net Discrepancy Check], "$#,##0.00")
)

// Measure 5: Trial Balance Net Activity by Normal Balance Type
GL Net Activity = 
SUMX(
    Dim_Chart_of_Accounts,
    IF(
        Dim_Chart_of_Accounts[Normal_Balance] = "Debit",
        [Total Debits] - [Total Credits],
        [Total Credits] - [Total Debits]
    )
)
```

---

## 2. Core Financial Statements & Profitability DAX

```dax
// Measure 6: Gross Commercial Revenue
Gross Commercial Revenue = 
SUM(Fact_Sales_Invoices_AR[Gross_Sales_Amount])

// Measure 7: Total Sales Discounts
Total Sales Discounts = 
SUM(Fact_Sales_Invoices_AR[Discount_Amount])

// Measure 8: Net Recognized Sales Revenue
Net Sales Revenue = 
SUM(Fact_Sales_Invoices_AR[Net_Sales_Amount])

// Measure 9: Total Cost of Goods Sold (COGS)
Total Cost of Goods Sold = 
SUM(Fact_Sales_Invoices_AR[Cost_of_Sales])

// Measure 10: Gross Profit
Gross Profit = 
[Net Sales Revenue] - [Total Cost of Goods Sold]

// Measure 11: Gross Profit Margin Percentage
Gross Margin % = 
DIVIDE([Gross Profit], [Net Sales Revenue], 0)

// Measure 12: Total Operating Expenses (OPEX)
Total Operating Expenses = 
CALCULATE(
    [Total Debits] - [Total Credits],
    Dim_Chart_of_Accounts[Account_Subclass] = "Operating Expenses"
)

// Measure 13: EBITDA Operating Income
EBITDA Operating Income = 
[Gross Profit] - [Total Operating Expenses]

// Measure 14: Net Revenue Year-over-Year (YoY) Growth %
Net Revenue Prior Year = 
CALCULATE(
    [Net Sales Revenue],
    SAMEPERIODLASTYEAR(Dim_Date[Date])
)

Net Revenue YoY % = 
DIVIDE(
    [Net Sales Revenue] - [Net Revenue Prior Year],
    [Net Revenue Prior Year],
    0
)
```

---

## 3. Accounts Payable (AP) & Procurement Forensic DAX

```dax
// Measure 15: Total AP Invoiced Spend
Total AP Invoiced Spend = 
SUM(Fact_Vendor_Invoices_AP[Invoice_Amount])

// Measure 16: Total AP Cash Disbursed
Total AP Cash Disbursed = 
SUM(Fact_Vendor_Invoices_AP[Paid_Amount])

// Measure 17: Count of Split Invoices Under $5,000 Approval Limit ($4,850 - $4,999)
Count Split Invoices (<$5k Limit) = 
CALCULATE(
    COUNTROWS(Fact_Vendor_Invoices_AP),
    Fact_Vendor_Invoices_AP[Invoice_Amount] >= 4850,
    Fact_Vendor_Invoices_AP[Invoice_Amount] < 5000
)

// Measure 18: Total Dollar Value of Split Invoices (<$5k)
Split Invoices Total Spend = 
CALCULATE(
    SUM(Fact_Vendor_Invoices_AP[Invoice_Amount]),
    Fact_Vendor_Invoices_AP[Invoice_Amount] >= 4850,
    Fact_Vendor_Invoices_AP[Invoice_Amount] < 5000
)

// Measure 19: Non-PO Emergency Invoices Spend
Non-PO Invoiced Spend = 
CALCULATE(
    SUM(Fact_Vendor_Invoices_AP[Invoice_Amount]),
    Fact_Vendor_Invoices_AP[Is_PO_Matched] = "No"
)

// Measure 20: Non-PO Spend Percentage
Non-PO Spend % = 
DIVIDE([Non-PO Invoiced Spend], [Total AP Invoiced Spend], 0)

// Measure 21: Potential Duplicate Invoices Spend
Duplicate Invoiced Spend = 
SUMX(
    SUMMARIZE(
        Fact_Vendor_Invoices_AP,
        Fact_Vendor_Invoices_AP[Vendor_ID],
        Fact_Vendor_Invoices_AP[Invoice_Amount],
        "InvoiceCount", COUNT(Fact_Vendor_Invoices_AP[Invoice_ID]),
        "SumAmount", SUM(Fact_Vendor_Invoices_AP[Invoice_Amount])
    ),
    IF([InvoiceCount] > 1, [SumAmount] - ([SumAmount] / [InvoiceCount]), 0)
)
```

---

## 4. General Ledger Anomaly & Fraud Detection DAX

```dax
// Measure 22: Weekend Manual Journal Adjustments Total Value
Weekend Manual JEs Total = 
CALCULATE(
    SUM(Fact_GL_Journal_Entries[Debit]),
    Fact_GL_Journal_Entries[Is_Manual] = 1,
    Dim_Date[Is_Weekend] = 1
)

// Measure 23: Count of Weekend Manual Journal Entries
Weekend Manual JEs Count = 
CALCULATE(
    DISTINCTCOUNT(Fact_GL_Journal_Entries[Journal_ID]),
    Fact_GL_Journal_Entries[Is_Manual] = 1,
    Dim_Date[Is_Weekend] = 1
)

// Measure 24: Unapproved Suspicious Manual Journal Adjustments
Unapproved Suspicious Adjustments = 
CALCULATE(
    SUM(Fact_GL_Journal_Entries[Debit]),
    Fact_GL_Journal_Entries[Is_Manual] = 1,
    ISBLANK(Fact_GL_Journal_Entries[Approved_By]) || Fact_GL_Journal_Entries[Approved_By] = ""
)

// Measure 25: Sensitive Account 9100 Miscellaneous Debit Spend
Account 9100 Total Debits = 
CALCULATE(
    SUM(Fact_GL_Journal_Entries[Debit]),
    Fact_GL_Journal_Entries[Account_Number] = "9100"
)
```

---

## 5. Travel & Entertainment (T&E) Expense Audit DAX

```dax
// Measure 26: Total Claimed T&E Expenses
Total Claimed Expenses = 
SUM(Fact_Employee_Expenses_TE[Claim_Amount])

// Measure 27: Total Missing Receipt Claims Dollar Amount
Missing Receipt Claims Amount = 
CALCULATE(
    SUM(Fact_Employee_Expenses_TE[Claim_Amount]),
    Fact_Employee_Expenses_TE[Receipt_Attached] = "No"
)

// Measure 28: Missing Receipt Percentage
Missing Receipt % = 
DIVIDE([Missing Receipt Claims Amount], [Total Claimed Expenses], 0)

// Measure 29: Weekend Expense Claims Spend
Weekend Expense Spend = 
CALCULATE(
    SUM(Fact_Employee_Expenses_TE[Claim_Amount]),
    Dim_Date[Is_Weekend] = 1
)
```

---

## 6. Commercial Margin Leakage & Discount Fraud DAX

```dax
// Measure 30: Average Discount Percentage Applied
Average Discount % = 
AVERAGE(Fact_Sales_Invoices_AR[Discount_Percentage])

// Measure 31: Count of Invoices with Discounts Over Policy Limit (>15%)
High Discount Invoices Count = 
CALCULATE(
    COUNTROWS(Fact_Sales_Invoices_AR),
    Fact_Sales_Invoices_AR[Discount_Percentage] > 0.15
)

// Measure 32: Total Financial Loss from Unauthorized Discounts (>15%)
Unauthorized High Discounts Amount = 
CALCULATE(
    SUM(Fact_Sales_Invoices_AR[Discount_Amount]),
    Fact_Sales_Invoices_AR[Discount_Percentage] > 0.15
)
```

---

## 7. Grand Forensic Exposure Summary DAX

```dax
// Measure 33: Total Quantified Forensic Anomaly & Fraud Loss
Total Quantified Fraud Exposure = 
[Split Invoices Total Spend] + 
CALCULATE(SUM(Fact_Vendor_Invoices_AP[Invoice_Amount]), Fact_Vendor_Invoices_AP[Vendor_ID] = "VND-1038") + 
[Duplicate Invoiced Spend] + 
[Weekend Manual JEs Total] + 
CALCULATE(SUM(Fact_Employee_Expenses_TE[Claim_Amount]), Fact_Employee_Expenses_TE[Employee_ID] = "EMP-129") + 
[Unauthorized High Discounts Amount]
```
