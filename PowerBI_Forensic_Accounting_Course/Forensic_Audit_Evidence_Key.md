# Official Forensic Audit Investigation Dossier & Evidence Key
### Apex Horizon Global Corp — Audited Periods: FY2024 - FY2025
**Lead Forensic Investigator:** Tatenda Makuvaza  
**Case Classification:** Multi-Vector Occupational Fraud, Conflict of Interest & Financial Misstatement  
**Total Identified Financial Exposure:** **$1,412,297.51 USD**  

---

## 1. Executive Summary of Forensic Findings

During the comprehensive forensic examination of Apex Horizon Global Corp's Enterprise Resource Planning (ERP) database covering fiscal years 2024 and 2025 (25,830 total transactional records), our forensic data analytics model uncovered **six major fraudulent schemes and compliance breakdowns**, resulting in an aggregate financial exposure of **$1,412,297.51**.

```
+----------------------------------------------------------------------------------------------------+
|                                SUMMARY OF FORENSIC FRAUD SCHEMES                                   |
+---+------------------------------------+--------------------------+-------------+------------------+
| # | Scheme Description                 | Primary Subject(s)       | Volume      | Dollar Exposure  |
+---+------------------------------------+--------------------------+-------------+------------------+
| 1 | Split Invoicing Structuring        | Marcus Brody (EMP-103)   | 48 Invoices | $236,412.88      |
| 2 | Ghost Shell Vendor / Conflict      | David Vance (EMP-118)    | 13 Invoices | $266,129.04      |
| 3 | Duplicate Invoice Overpayments     | Summit Logistics (V1015) | 4 Pairs     | $94,200.50       |
| 4 | Off-Hours Manual Journal Plugs     | Elena Rostova (EMP-105)  | 8 JEs (16L) | $533,000.00      |
| 5 | Fictitious Weekend T&E Velocity    | Julian Thorne (EMP-129)  | 208 Claims  | $30,410.19       |
| 6 | Quarter-End Quota Discount Gaming  | Rachel Zane (EMP-133)    | 55 Invoices | $252,144.90      |
+---+------------------------------------+--------------------------+-------------+------------------+
|   | TOTAL QUANTIFIED FINANCIAL LOSS    | Multiple Internal Actors |             | $1,412,297.51    |
+---+------------------------------------+--------------------------+-------------+------------------+
```

---

## 2. Detailed Forensic Case Dossiers

### Case 1: Split Invoicing Structuring (Threshold Circumvention)
- **Subject:** Marcus Brody (VP of Commercial Sales, `EMP-103`)
- **Vendor:** CloudSphere Solutions LLC (`VND-1042`)
- **Cost Center:** Commercial Sales (`CC-300`)
- **Approval Authorization Limit:** $5,000.00
- **Modus Operandi:** To circumvent corporate procurement policy requiring Chief Financial Officer (`EMP-102`) dual authorization for expenditures ≥ $5,000, Marcus Brody approved 48 distinct invoices from CloudSphere Solutions structured precisely between **$4,853.11** and **$4,992.47**. Invoices were issued in rapid clusters (2 invoices per day within 48 hours of each other).
- **Total Invoiced Spend:** **$236,412.88** across 48 invoices.
- **Compliance Violation:** Zero Purchase Orders were issued (`Is_PO_Matched = 'No'`). Internal control circumvention of signature authority thresholds.

---

### Case 2: Conflict of Interest & Ghost Shell Vendor
- **Subject:** David Vance (Senior Procurement Officer, `EMP-118`)
- **Vendor Entity:** Apex Global Consulting Ltd (`VND-1038`)
- **Cost Center:** Supply Chain & Logistics (`CC-500`)
- **Modus Operandi:** In February 2024, David Vance created a shell vendor entity named *Apex Global Consulting Ltd* in the ERP master directory. A cross-join query between `Dim_Employees` and `Dim_Vendors` reveals:
  - **Bank Account Match:** Vendor bank account `ACCT-US-908812` is identical to David Vance's personal direct deposit payroll account.
  - **Physical Address Match:** Vendor registered address `742 Evergreen Terrace, Springfield, OR 97477` is Vance's personal residential address.
  - **Payment Terms:** Structured as "Immediate" disbursement. Invoices were approved by Vance with no Purchase Orders (`PO_Number = 'NONE-EMERGENCY'`).
- **Total Siphoned Amount:** **$266,129.04** across 13 disbursements.

---

### Case 3: Duplicate Invoice Payments & Near-Duplicate Exploit
- **Vendor Entity:** Summit Logistics Inc (`VND-1015`)
- **Cost Center:** Supply Chain & Logistics (`CC-500`)
- **Modus Operandi:** 4 separate freight delivery service events were billed and disbursed twice through subtle string manipulations and alternate payment instrument runs:
  1. `AP-INV-77102` ($18,450.00 on 2024-04-10) re-billed as `AP-INV-77102-DUP` ($18,450.00 on 2024-04-24).
  2. `AP-INV-81204` ($24,800.00 on 2024-08-15) re-billed as `AP-INV-81204A` ($24,800.00 on 2024-08-29).
  3. `AP-INV-92011` ($19,750.50 on 2025-03-10) re-billed with a trailing whitespace `AP-INV-92011 ` ($19,750.50 on 2025-03-24).
  4. `AP-INV-99401` ($31,200.00 on 2025-09-18) re-billed as `AP-INV-99401-1` ($31,200.00 on 2025-10-02).
- **Total Erroneous Duplicate Outflow:** **$94,200.50**.

---

### Case 4: Weekend & Off-Hours Manual Journal Plugs
- **Subject:** Elena Rostova (Senior General Ledger Accountant, `EMP-105`)
- **General Ledger Accounts Debited:** `9100` (Miscellaneous & Sundry Expense) and `6030` (Professional Consulting)
- **Offsetting Account Credited:** `1010` (Operating Cash Checking)
- **Modus Operandi:** 8 high-dollar manual journal adjustments were entered on Saturday evenings between **23:35 and 23:55** using vague narrative memos such as *"Quarterly unallocated expense reclassification"*, *"Intercompany variance write-off"*, and *"Late close suspense plug"*.
- **Control Breakdown:** All 8 entries bypassed secondary supervisory review (`Approved_By` field is completely blank).
- **Total Debited Amount:** **$533,000.00** ($396,000 to Account 9100, $137,000 to Account 6030).

---

### Case 5: Fictitious Weekend T&E Reimbursement Claims
- **Subject:** Julian Thorne (Senior Enterprise Sales Rep, `EMP-129`)
- **Cost Center:** Commercial Sales (`CC-300`)
- **Approving Manager:** Marcus Brody (`EMP-103`)
- **Modus Operandi:** Over the two-year audited period, Julian Thorne submitted **208 consecutive expense reimbursement claims** exclusively dated on Saturdays and Sundays.
  - **Receipt Audit:** 100% of claims (208 out of 208) lacked attached receipts (`Receipt_Attached = 'No'`).
  - **Threshold Structuring:** All claims were filed between **$142.50 and $149.95** (mean = $146.20), deliberately staying just below the corporate $150 receipt mandatory audit policy.
  - **Merchants:** Fabricated entities (*"Luxury VIP Lounge Club"*, *"Platinum Sky Lounge"*, *"Apex Gastronomy Club"*).
- **Total Fictitious Reimbursements:** **$30,410.19**.

---

### Case 6: Quarter-End Quota Gaming & Unauthorized Discounts
- **Subject:** Rachel Zane (Key Account Executive, `EMP-133`)
- **Corporate Discount Policy Limit:** Maximum 15% without CFO written approval.
- **Modus Operandi:** While the overall sales team averaged a **3.1%** discount rate, Rachel Zane averaged **7.4%** across all accounts, with severe spikes occurring in the final 10 days of Q1 (March), Q2 (June), Q3 (September), and Q4 (December).
- **Findings:** Zane applied unauthorized discounts between **30% and 42%** on 55 large enterprise invoices to artificially inflate sales volume and trigger personal quarterly bonus payouts.
- **Total Revenue Leakage:** **$252,144.90** in excess discounts on high-discount sales.

---

## 3. Ground Truth Mathematical Verification Matrix

| Power BI Measure / Metric | Mathematical Ground Truth | Power BI Source & Context |
|---|---|---|
| **GL Total Debits** | `$77,628,218.12` | `SUM(Fact_GL_Journal_Entries[Debit])` |
| **GL Total Credits** | `$77,628,218.12` | `SUM(Fact_GL_Journal_Entries[Credit])` |
| **GL Net Discrepancy** | `$0.00` | Double-entry trial balance 100% balanced |
| **Gross Commercial Revenue** | `$33,074,481.93` | `SUM(Fact_Sales_Invoices_AR[Gross_Sales_Amount])` |
| **Total Commercial Discounts** | `$1,008,012.70` | `SUM(Fact_Sales_Invoices_AR[Discount_Amount])` |
| **Net Sales Revenue** | `$32,066,469.23` | `SUM(Fact_Sales_Invoices_AR[Net_Sales_Amount])` |
| **Cost of Goods Sold (COGS)** | `$16,605,945.19` | `SUM(Fact_Sales_Invoices_AR[Cost_of_Sales])` |
| **Gross Profit ($ and %)** | `$15,460,524.04 (48.2%)` | `[Net Sales Revenue] - [Total COGS]` |
| **Total AP Invoiced Spend** | `$8,476,029.18` (1,734 invs) | `SUM(Fact_Vendor_Invoices_AP[Invoice_Amount])` |
| **Total AP Cash Disbursed** | `$7,975,413.92` | `SUM(Fact_Vendor_Invoices_AP[Paid_Amount])` |
| **CloudSphere Split Spend** | `$236,412.88` (48 invs) | Filter on `Vendor_ID = 'VND-1042'` |
| **Apex Global Shell Spend** | `$266,129.04` (13 invs) | Filter on `Vendor_ID = 'VND-1038'` |
| **Summit Logistics Duplicates** | `$94,200.50` (4 pairs) | Duplicate amounts on `VND-1015` |
| **Weekend Manual JEs Total** | `$533,000.00` (8 JEs) | `Is_Manual = 1` & `Is_Weekend = 1` |
| **Julian Thorne Fake T&E** | `$30,410.19` (208 claims) | Filter on `Employee_ID = 'EMP-129'` |
| **Rachel Zane Excess Discounts** | `$252,144.90` (55 invs) | Filter on `Sales_Rep_ID = 'EMP-133'` & `Disc > 20%` |
| **Total Quantified Fraud Exposure**| **`$1,412,297.51`** | Aggregate forensic audit loss |

---

## 4. Internal Control Recommendations & Remediation Plan

1. **Segregation of Duties (SoD) & Approval Bands:** Configure hard ERP workflow blocks preventing managers from approving invoices within 10% of their authorization limit without secondary VP approval.
2. **Master Entity Cross-Matching:** Implement automated nightly cross-validation jobs comparing employee bank routing/accounts and addresses against vendor master records.
3. **Mandatory 3-Way Matching:** Eliminate all non-PO emergency payments for consulting/advisory retainers. Mandate purchase requisition and PO generation before invoice receipt.
4. **GL Posting Temporal Locks:** Restrict manual journal postings to standard business hours (07:00 - 19:00 Mon-Fri). Require dual-key CFO electronic sign-off for off-hours adjustments.
5. **Zero-Receipt Policy:** Eliminate the $150 receipt waiver for discretionary dining and entertainment claims. Require itemized digital receipts for 100% of claims.
