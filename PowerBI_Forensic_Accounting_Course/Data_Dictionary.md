# Enterprise Data Dictionary — Apex Horizon Global Corp
### Forensic Accounting & Power BI Training Dataset
**Author:** Forensic Data Analytics Curriculum Team  
**Participant:** Tatenda Makuvaza  
**Target Tables:** 11 Relational CSV Files (Located in `/data/`)  

---

## 1. Dimension Tables

### 1.1 `Dim_Date.csv` (731 Rows)
Master continuous calendar table covering FY2024 and FY2025.
- `Date_Key` *(Integer)*: Primary Key in `YYYYMMDD` format (e.g. `20240101`).
- `Date` *(Date)*: Continuous calendar date (`2024-01-01` to `2025-12-31`).
- `Year` *(Integer)*: Calendar year (`2024`, `2025`).
- `Quarter` *(Text)*: Calendar quarter (`Q1`, `Q2`, `Q3`, `Q4`).
- `Month_Num` *(Integer)*: Calendar month integer (`1` to `12`).
- `Month_Name` *(Text)*: Full month name (`January` to `December`). Sort by `Month_Num`.
- `Month_Year` *(Text)*: Short month and year (`Jan 2024` to `Dec 2025`).
- `Day_Of_Month` *(Integer)*: Day of the month (`1` to `31`).
- `Day_Of_Week` *(Integer)*: ISO day of week (`1 = Monday`, `7 = Sunday`).
- `Day_Name` *(Text)*: Full day name (`Monday` to `Sunday`).
- `Is_Weekend` *(Integer)*: Binary weekend indicator (`1 = Saturday/Sunday`, `0 = Weekday`).
- `Fiscal_Year` *(Text)*: Fiscal year string (`FY2024`, `FY2025`).
- `Fiscal_Quarter` *(Text)*: Fiscal quarter string (`FQ1`, `FQ2`, `FQ3`, `FQ4`).
- `Fiscal_Period` *(Text)*: Fiscal period string (`FP01` to `FP12`).

---

### 1.2 `Dim_Chart_of_Accounts.csv` (32 Rows)
Master general ledger chart of accounts structure.
- `Account_Number` *(Text)*: Primary Key (e.g., `1010`, `2010`, `4010`, `9100`).
- `Account_Name` *(Text)*: Formal ledger account title.
- `Account_Class` *(Text)*: Top-level classification (`Asset`, `Liability`, `Equity`, `Revenue`, `Expense`).
- `Account_Subclass` *(Text)*: Sub-level category (`Current Assets`, `Operating Expenses`, `Cost of Sales`, etc.).
- `Financial_Statement` *(Text)*: Reporting target (`Balance Sheet`, `Income Statement`).
- `Normal_Balance` *(Text)*: Natural balance sign (`Debit`, `Credit`).
- `Is_Sensitive_Account` *(Integer)*: Forensic audit flag (`1 = High Risk`, `0 = Standard`).

---

### 1.3 `Dim_Cost_Centers.csv` (7 Rows)
Operating departments and organizational hierarchy.
- `Cost_Center_ID` *(Text)*: Primary Key (`CC-100` to `CC-700`).
- `Cost_Center_Name` *(Text)*: Department name (e.g., `Executive Management`, `Finance & Accounting`, `Sales & Commercial Operations`, `IT, Cloud & Cybersecurity`, `Supply Chain & Logistics`).
- `Division` *(Text)*: Broad corporate division (`Corporate`, `Operations`, `Commercial`).
- `Department_Head` *(Text)*: Executive director in charge.
- `Budget_FY24` *(Fixed Decimal)*: Approved annual OPEX budget for FY2024.
- `Budget_FY25` *(Fixed Decimal)*: Approved annual OPEX budget for FY2025.

---

### 1.4 `Dim_Employees.csv` (40 Rows)
Staff directory, organizational hierarchy, and banking details.
- `Employee_ID` *(Text)*: Primary Key (`EMP-101` to `EMP-140`).
- `Full_Name` *(Text)*: Employee full name.
- `Email` *(Text)*: Corporate email address.
- `Cost_Center_ID` *(Text)*: Foreign Key to `Dim_Cost_Centers`.
- `Department` *(Text)*: Operating department.
- `Job_Title` *(Text)*: Position / role title.
- `Manager_ID` *(Text)*: Foreign Key to `Dim_Employees` (Manager reporting line).
- `Hire_Date` *(Date)*: Employee start date.
- `Residential_Address` *(Text)*: Registered home address.
- `Bank_Account_Number` *(Text)*: Direct deposit payroll bank account number. *(Forensic audit link to vendor master!)*
- `Approval_Limit_USD` *(Fixed Decimal)*: Maximum single transaction signing authority.
- `Status` *(Text)*: Employment status (`Active`, `Terminated`).

---

### 1.5 `Dim_Vendors.csv` (50 Rows)
Approved supplier master records and banking details.
- `Vendor_ID` *(Text)*: Primary Key (`VND-1001` to `VND-1050`).
- `Vendor_Name` *(Text)*: Commercial vendor legal title.
- `Tax_ID` *(Text)*: Corporate Employer Identification Number (EIN).
- `Address` *(Text)*: Physical vendor billing address.
- `City` *(Text)*: Vendor city.
- `Country` *(Text)*: Country code.
- `Bank_Account_Number` *(Text)*: Direct disbursement bank account number.
- `Bank_Routing_Number` *(Text)*: Automated Clearing House (ACH) 9-digit routing transit number.
- `Payment_Terms` *(Text)*: Standard commercial terms (`Net 15`, `Net 30`, `Net 60`, `Immediate`).
- `Creation_Date` *(Date)*: Date supplier master was created in ERP.
- `Created_By` *(Text)*: Foreign Key to `Dim_Employees` (User ID who set up vendor).
- `Vendor_Risk_Rating` *(Text)*: Procurement risk category (`Low`, `Medium`, `High`, `Critical`).
- `Is_Approved_Vendor` *(Text)*: Vendor validation state (`Yes`, `No`).

---

### 1.6 `Dim_Customers.csv` (50 Rows)
Commercial enterprise customer records.
- `Customer_ID` *(Text)*: Primary Key (`CUST-2001` to `CUST-2050`).
- `Customer_Name` *(Text)*: Enterprise client legal name.
- `Region` *(Text)*: Geographic sales theater (`North America`, `Europe`, `Asia Pacific`, `Latin America`).
- `Country` *(Text)*: Customer country.
- `Industry` *(Text)*: Sector (`Technology`, `Healthcare`, `Manufacturing`, `Retail`, `Financial Services`, `Energy`).
- `Credit_Limit` *(Fixed Decimal)*: Authorized credit limit in USD.
- `Customer_Since` *(Date)*: Onboarding contract date.
- `Payment_Terms` *(Text)*: Invoicing credit terms (`Net 30`, `Net 45`, `Net 60`).
- `Risk_Category` *(Text)*: Credit rating (`Preferred`, `Standard`, `High Risk`).

---

## 2. Fact Tables

### 2.1 `Fact_GL_Journal_Entries.csv` (18,579 Rows)
Comprehensive General Ledger double-entry transactional journal lines.
- `Journal_ID` *(Text)*: Batch journal header identifier (`JE-YYYY-XXXXX`).
- `Line_ID` *(Integer)*: Individual line item number within the journal batch (`1`, `2`, `3`...).
- `Posting_Date` *(Date)*: Accounting posting date. Foreign Key to `Dim_Date`.
- `Posting_Timestamp` *(Text)*: Complete ISO date and time (`YYYY-MM-DD HH:MM:SS`).
- `Period_Key` *(Integer)*: Accounting period key (`YYYYMM`).
- `Account_Number` *(Text)*: Foreign Key to `Dim_Chart_of_Accounts`.
- `Cost_Center_ID` *(Text)*: Foreign Key to `Dim_Cost_Centers`.
- `Debit` *(Fixed Decimal)*: Debit transaction amount in USD ($).
- `Credit` *(Fixed Decimal)*: Credit transaction amount in USD ($).
- `Transaction_Type` *(Text)*: Category (`Standard Subledger Post`, `Automated Recurring`, `Standard Payment Clearing`, `Manual Adjustment`).
- `Description` *(Text)*: Journal memo narrative.
- `Posted_By` *(Text)*: User ID or system module that created the entry.
- `Approved_By` *(Text)*: User ID who authorized posting (Blank for unapproved adjustments).
- `Is_Manual` *(Integer)*: Flag for manual journal adjustments (`1 = Manual Entry`, `0 = Automated Subledger`).
- `Document_Reference` *(Text)*: Source transaction document identifier.

---

### 2.2 `Fact_Vendor_Invoices_AP.csv` (1,734 Rows)
Accounts Payable supplier invoices and disbursement details.
- `Invoice_ID` *(Text)*: Primary Key (`AP-INV-XXXXX`).
- `Vendor_ID` *(Text)*: Foreign Key to `Dim_Vendors`.
- `PO_Number` *(Text)*: Associated Purchase Order reference number.
- `Invoice_Date` *(Date)*: Date invoice was received. Foreign Key to `Dim_Date`.
- `Due_Date` *(Date)*: Payment due date based on payment terms.
- `Payment_Date` *(Date / Text)*: Actual disbursement date (Blank if open/unpaid).
- `Cost_Center_ID` *(Text)*: Foreign Key to `Dim_Cost_Centers`.
- `Invoice_Amount` *(Fixed Decimal)*: Total invoiced gross amount in USD.
- `Paid_Amount` *(Fixed Decimal)*: Actual settlement amount disbursed.
- `Discount_Taken` *(Fixed Decimal)*: Early settlement cash discount applied.
- `Payment_Status` *(Text)*: Settlement status (`Paid`, `Open`, `Overdue`, `Disputed`).
- `Approved_By` *(Text)*: Foreign Key to `Dim_Employees` (Approving manager).
- `Payment_Method` *(Text)*: Payment instrument (`EFT`, `ACH Wire`, `Corporate Card`, `Check`).
- `Is_PO_Matched` *(Text)*: Compliance 3-way match validation flag (`Yes`, `No`).
- `Notes` *(Text)*: Invoicing memo and line item descriptions.

---

### 2.3 `Fact_Sales_Invoices_AR.csv` (2,881 Rows)
Accounts Receivable commercial customer billing.
- `Sales_Invoice_ID` *(Text)*: Primary Key (`AR-INV-XXXXX`).
- `Customer_ID` *(Text)*: Foreign Key to `Dim_Customers`.
- `Sales_Rep_ID` *(Text)*: Foreign Key to `Dim_Employees` (Sales Representative).
- `Invoice_Date` *(Date)*: Billing recognition date. Foreign Key to `Dim_Date`.
- `Due_Date` *(Date)*: Payment due date.
- `Payment_Date` *(Date / Text)*: Customer payment receipt date.
- `Gross_Sales_Amount` *(Fixed Decimal)*: List price gross revenue.
- `Discount_Amount` *(Fixed Decimal)*: Price concession or contractual discount.
- `Discount_Percentage` *(Fixed Decimal)*: Discount rate applied (`0.00` to `0.42`).
- `Net_Sales_Amount` *(Fixed Decimal)*: Net recognized revenue (`Gross - Discount`).
- `Cost_of_Sales` *(Fixed Decimal)*: Standard direct product / service cost.
- `Payment_Status` *(Text)*: Collection status (`Paid`, `Outstanding`, `Overdue`, `Bad Debt Written Off`).
- `Region` *(Text)*: Sales geographic region.

---

### 2.4 `Fact_Employee_Expenses_TE.csv` (1,833 Rows)
Employee Travel & Entertainment (T&E) reimbursement claims.
- `Expense_ID` *(Text)*: Primary Key (`EXP-XXXXX`).
- `Employee_ID` *(Text)*: Foreign Key to `Dim_Employees`.
- `Cost_Center_ID` *(Text)*: Foreign Key to `Dim_Cost_Centers`.
- `Expense_Date` *(Date)*: Date expenditure incurred. Foreign Key to `Dim_Date`.
- `Submission_Date` *(Date)*: Date claim was filed in Concur / ERP.
- `Category` *(Text)*: Expense classification (`Airfare`, `Lodging`, `Meals & Entertainment`, `Ground Transport`, `Tech Hardware`, `Office Misc`).
- `Merchant_Name` *(Text)*: Commercial vendor / restaurant / airline name.
- `City` *(Text)*: Expenditure location.
- `Claim_Amount` *(Fixed Decimal)*: Total claimed reimbursement amount.
- `Approved_Amount` *(Fixed Decimal)*: Manager-approved settlement amount.
- `Receipt_Attached` *(Text)*: Itemized receipt audit verification (`Yes`, `No`).
- `Approved_By` *(Text)*: Foreign Key to `Dim_Employees` (Approving supervisor).
- `Approval_Status` *(Text)*: Workflow state (`Approved`, `Rejected`, `Flagged Under Review`).
- `Payment_Date` *(Date)*: Payroll expense reimbursement date.

---

### 2.5 `Fact_Bank_Statements.csv` (72 Rows)
Monthly treasury bank account statement transactions for cash reconciliation.
- `Bank_Trans_ID` *(Text)*: Primary Key (`BNK-XXXXX`).
- `Statement_Date` *(Date)*: Monthly statement close date. Foreign Key to `Dim_Date`.
- `Transaction_Type` *(Text)*: Banking event (`ACH Customer Receipts Deposit`, `ACH Vendor Wire Outflows`, `Bank Service Fee`).
- `Reference_Number` *(Text)*: Banking reference code (`DEP-YYYYMM`, `WIR-YYYYMM`, `FEE-YYYYMM`).
- `Amount` *(Fixed Decimal)*: Net cash movement in USD (+ for inflows, - for outflows).
- `GL_Reference_Account` *(Integer / Text)*: Target general ledger offset account (`1010` Cash, `9100` Fee).
- `Is_Reconciled` *(Integer)*: Statement reconciliation flag (`1 = Matched`, `0 = Unreconciled`).
- `Reconciliation_Notes` *(Text)*: Treasury clearing commentary.
