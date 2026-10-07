import os
import random
import datetime
import numpy as np
import pandas as pd

# Set fixed seed for reproducibility
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "/home/user/soulfyas-restaurant-erp/PowerBI_Forensic_Accounting_Course/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting Forensic Accounting Dataset Generation...")

# ==========================================
# 1. Dim_Date (2024-01-01 to 2025-12-31)
# ==========================================
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2025, 12, 31)
num_days = (end_date - start_date).days + 1

date_rows = []
for i in range(num_days):
    d = start_date + datetime.timedelta(days=i)
    date_key = int(d.strftime("%Y%m%d"))
    year = d.year
    quarter = f"Q{(d.month - 1) // 3 + 1}"
    month_num = d.month
    month_name = d.strftime("%B")
    month_year = d.strftime("%b %Y")
    day_of_month = d.day
    day_of_week = d.isoweekday() # 1=Mon, 7=Sun
    day_name = d.strftime("%A")
    is_weekend = 1 if day_of_week in [6, 7] else 0
    fiscal_year = f"FY{year}"
    fiscal_quarter = f"FQ{(d.month - 1) // 3 + 1}"
    fiscal_period = f"FP{d.month:02d}"
    
    date_rows.append({
        "Date_Key": date_key,
        "Date": d.strftime("%Y-%m-%d"),
        "Year": year,
        "Quarter": quarter,
        "Month_Num": month_num,
        "Month_Name": month_name,
        "Month_Year": month_year,
        "Day_Of_Month": day_of_month,
        "Day_Of_Week": day_of_week,
        "Day_Name": day_name,
        "Is_Weekend": is_weekend,
        "Fiscal_Year": fiscal_year,
        "Fiscal_Quarter": fiscal_quarter,
        "Fiscal_Period": fiscal_period
    })

df_date = pd.DataFrame(date_rows)
df_date.to_csv(os.path.join(OUTPUT_DIR, "Dim_Date.csv"), index=False)
print(f"Dim_Date created: {len(df_date)} rows")

# ==========================================
# 2. Dim_Chart_of_Accounts
# ==========================================
coa_data = [
    # Assets
    (1010, "Operating Cash - Checking", "Asset", "Current Assets", "Balance Sheet", "Debit", 1),
    (1020, "Payroll Cash - Escrow", "Asset", "Current Assets", "Balance Sheet", "Debit", 0),
    (1030, "Petty Cash Fund", "Asset", "Current Assets", "Balance Sheet", "Debit", 1),
    (1200, "Accounts Receivable - Trade", "Asset", "Current Assets", "Balance Sheet", "Debit", 0),
    (1250, "Allowance for Doubtful Accounts", "Asset", "Current Assets", "Balance Sheet", "Credit", 1),
    (1300, "Inventory - Finished Goods", "Asset", "Current Assets", "Balance Sheet", "Debit", 0),
    (1350, "Prepaid Expenses & Insurance", "Asset", "Current Assets", "Balance Sheet", "Debit", 0),
    (1500, "Property, Plant & Equipment", "Asset", "Non-Current Assets", "Balance Sheet", "Debit", 0),
    (1550, "Accumulated Depreciation", "Asset", "Non-Current Assets", "Balance Sheet", "Credit", 0),
    # Liabilities
    (2010, "Accounts Payable - Trade", "Liability", "Current Liabilities", "Balance Sheet", "Credit", 0),
    (2020, "Accrued Payroll & Benefits", "Liability", "Current Liabilities", "Balance Sheet", "Credit", 0),
    (2030, "Accrued Sales & Corporate Tax", "Liability", "Current Liabilities", "Balance Sheet", "Credit", 0),
    (2100, "Short-Term Revolving Credit", "Liability", "Current Liabilities", "Balance Sheet", "Credit", 0),
    (2500, "Long-Term Senior Notes", "Liability", "Long-Term Liabilities", "Balance Sheet", "Credit", 0),
    # Equity
    (3010, "Common Stock & Paid-In Capital", "Equity", "Shareholders Equity", "Balance Sheet", "Credit", 0),
    (3020, "Retained Earnings", "Equity", "Shareholders Equity", "Balance Sheet", "Credit", 0),
    # Revenue
    (4010, "Commercial Product Sales", "Revenue", "Operating Revenue", "Income Statement", "Credit", 0),
    (4020, "Enterprise Software & Support", "Revenue", "Operating Revenue", "Income Statement", "Credit", 0),
    (4030, "Professional Services Revenue", "Revenue", "Operating Revenue", "Income Statement", "Credit", 0),
    (4090, "Sales Discounts & Allowances", "Revenue", "Operating Revenue", "Income Statement", "Debit", 1),
    # COGS & Expenses
    (5010, "Cost of Goods Sold - Materials", "Expense", "Cost of Sales", "Income Statement", "Debit", 0),
    (5020, "Direct Labor Cost", "Expense", "Cost of Sales", "Income Statement", "Debit", 0),
    (6010, "Salaries & Wages - Operating", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (6020, "Employee Benefits & Health", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (6030, "Professional & Legal Consulting", "Expense", "Operating Expenses", "Income Statement", "Debit", 1),
    (6040, "Travel & Entertainment (T&E)", "Expense", "Operating Expenses", "Income Statement", "Debit", 1),
    (6050, "Marketing & Advertising Campaigns", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (6060, "IT Cloud & Infrastructure", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (6070, "Office Facilities & Utilities", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (7010, "Depreciation & Amortization", "Expense", "Operating Expenses", "Income Statement", "Debit", 0),
    (8010, "Interest Expense - Debt", "Expense", "Non-Operating Expenses", "Income Statement", "Debit", 0),
    (9100, "Miscellaneous & Sundry Expense", "Expense", "Non-Operating Expenses", "Income Statement", "Debit", 1),
]

df_coa = pd.DataFrame(coa_data, columns=[
    "Account_Number", "Account_Name", "Account_Class", "Account_Subclass", 
    "Financial_Statement", "Normal_Balance", "Is_Sensitive_Account"
])
df_coa.to_csv(os.path.join(OUTPUT_DIR, "Dim_Chart_of_Accounts.csv"), index=False)
print(f"Dim_Chart_of_Accounts created: {len(df_coa)} rows")

# ==========================================
# 3. Dim_Cost_Centers
# ==========================================
cc_data = [
    ("CC-100", "Executive Management", "Corporate", "Victoria Sterling", 1200000, 1350000),
    ("CC-200", "Finance & Accounting", "Corporate", "Alexander Hayes", 950000, 1020000),
    ("CC-300", "Sales & Commercial Operations", "Commercial", "Marcus Brody", 3400000, 3800000),
    ("CC-400", "IT, Cloud & Cybersecurity", "Operations", "Devon Vance", 2800000, 3100000),
    ("CC-500", "Supply Chain & Logistics", "Operations", "Siddharth Nair", 4200000, 4600000),
    ("CC-600", "Human Resources & Talent", "Corporate", "Claire Bennett", 750000, 820000),
    ("CC-700", "Legal & Regulatory Compliance", "Corporate", "Tariq Al-Mansoor", 650000, 710000),
]

df_cc = pd.DataFrame(cc_data, columns=[
    "Cost_Center_ID", "Cost_Center_Name", "Division", "Department_Head", "Budget_FY24", "Budget_FY25"
])
df_cc.to_csv(os.path.join(OUTPUT_DIR, "Dim_Cost_Centers.csv"), index=False)
print(f"Dim_Cost_Centers created: {len(df_cc)} rows")

# ==========================================
# 4. Dim_Employees
# ==========================================
first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "Lucas", "Isabella", 
               "Benjamin", "Mia", "Oliver", "Evelyn", "Elijah", "Harper", "Alexander", "Camila", "Henry", "Gianna"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", 
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

departments = [
    ("CC-100", "Executive Management"),
    ("CC-200", "Finance & Accounting"),
    ("CC-300", "Sales & Commercial Operations"),
    ("CC-400", "IT, Cloud & Cybersecurity"),
    ("CC-500", "Supply Chain & Logistics"),
    ("CC-600", "Human Resources & Talent"),
    ("CC-700", "Legal & Regulatory Compliance")
]

emp_rows = [
    # C-Level & Executives
    {"Employee_ID": "EMP-101", "Full_Name": "Victoria Sterling", "Email": "v.sterling@enterprise.io", "Cost_Center_ID": "CC-100", "Department": "Executive Management", "Job_Title": "Chief Executive Officer", "Manager_ID": "", "Hire_Date": "2019-01-15", "Residential_Address": "1442 Bel Air Rd, Los Angeles, CA", "Bank_Account_Number": "ACCT-US-102938", "Approval_Limit_USD": 500000, "Status": "Active"},
    {"Employee_ID": "EMP-102", "Full_Name": "Alexander Hayes", "Email": "a.hayes@enterprise.io", "Cost_Center_ID": "CC-200", "Department": "Finance & Accounting", "Job_Title": "Chief Financial Officer", "Manager_ID": "EMP-101", "Hire_Date": "2019-03-01", "Residential_Address": "88 Ocean Blvd, Santa Monica, CA", "Bank_Account_Number": "ACCT-US-223411", "Approval_Limit_USD": 250000, "Status": "Active"},
    {"Employee_ID": "EMP-103", "Full_Name": "Marcus Brody", "Email": "m.brody@enterprise.io", "Cost_Center_ID": "CC-300", "Department": "Sales & Commercial Operations", "Job_Title": "VP of Commercial Sales", "Manager_ID": "EMP-101", "Hire_Date": "2020-05-12", "Residential_Address": "512 Pinecrest Way, Pasadena, CA", "Bank_Account_Number": "ACCT-US-334912", "Approval_Limit_USD": 5000, "Status": "Active"},
    {"Employee_ID": "EMP-104", "Full_Name": "Devon Vance", "Email": "d.vance@enterprise.io", "Cost_Center_ID": "CC-400", "Department": "IT, Cloud & Cybersecurity", "Job_Title": "Chief Technology Officer", "Manager_ID": "EMP-101", "Hire_Date": "2020-02-18", "Residential_Address": "104 Silicon Heights, Irvine, CA", "Bank_Account_Number": "ACCT-US-449102", "Approval_Limit_USD": 50000, "Status": "Active"},
    {"Employee_ID": "EMP-105", "Full_Name": "Elena Rostova", "Email": "e.rostova@enterprise.io", "Cost_Center_ID": "CC-200", "Department": "Finance & Accounting", "Job_Title": "Senior General Ledger Accountant", "Manager_ID": "EMP-102", "Hire_Date": "2021-06-10", "Residential_Address": "319 Elmwood St, Glendale, CA", "Bank_Account_Number": "ACCT-US-551029", "Approval_Limit_USD": 10000, "Status": "Active"},
    
    # Forensic Case 2 Key Actor: David Vance (Procurement Officer) - Shares Bank Acct & Address with Apex Global Consulting!
    {"Employee_ID": "EMP-118", "Full_Name": "David Vance", "Email": "d.vance.proc@enterprise.io", "Cost_Center_ID": "CC-500", "Department": "Supply Chain & Logistics", "Job_Title": "Senior Procurement Officer", "Manager_ID": "EMP-101", "Hire_Date": "2022-01-10", "Residential_Address": "742 Evergreen Terrace, Springfield, OR 97477", "Bank_Account_Number": "ACCT-US-908812", "Approval_Limit_USD": 25000, "Status": "Active"},
    
    # Forensic Case 5 Key Actor: Julian Thorne (Sales Executive submitting fake T&E)
    {"Employee_ID": "EMP-129", "Full_Name": "Julian Thorne", "Email": "j.thorne@enterprise.io", "Cost_Center_ID": "CC-300", "Department": "Sales & Commercial Operations", "Job_Title": "Senior Enterprise Sales Rep", "Manager_ID": "EMP-103", "Hire_Date": "2022-08-01", "Residential_Address": "404 Sunset Blvd, West Hollywood, CA", "Bank_Account_Number": "ACCT-US-778811", "Approval_Limit_USD": 2500, "Status": "Active"},
    
    # Forensic Case 6 Key Actor: Rachel Zane (Sales Rep applying excessive unauthorized discounts)
    {"Employee_ID": "EMP-133", "Full_Name": "Rachel Zane", "Email": "r.zane@enterprise.io", "Cost_Center_ID": "CC-300", "Department": "Sales & Commercial Operations", "Job_Title": "Key Account Executive", "Manager_ID": "EMP-103", "Hire_Date": "2021-11-15", "Residential_Address": "812 Beverly Glen, Century City, CA", "Bank_Account_Number": "ACCT-US-661199", "Approval_Limit_USD": 2500, "Status": "Active"}
]

existing_ids = [e["Employee_ID"] for e in emp_rows]
for num in range(106, 141):
    emp_id = f"EMP-{num}"
    if emp_id in existing_ids:
        continue
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    email = f"{fn.lower()[0]}.{ln.lower()}{num}@enterprise.io"
    cc_id, dept = random.choice(departments)
    titles = {
        "Executive Management": "Executive Director",
        "Finance & Accounting": random.choice(["Financial Analyst", "Accounts Payable Specialist", "Staff Accountant", "Internal Auditor"]),
        "Sales & Commercial Operations": random.choice(["Sales Manager", "Account Executive", "Business Development Rep"]),
        "IT, Cloud & Cybersecurity": random.choice(["Systems Administrator", "DevOps Engineer", "Cloud Architect"]),
        "Supply Chain & Logistics": random.choice(["Logistics Coordinator", "Procurement Specialist", "Inventory Supervisor"]),
        "Human Resources & Talent": random.choice(["HR Business Partner", "Talent Acquisition Lead", "Payroll Specialist"]),
        "Legal & Regulatory Compliance": random.choice(["Compliance Officer", "Corporate Counsel", "Legal Analyst"])
    }
    title = titles[dept]
    hire_yr = random.choice([2020, 2021, 2022, 2023])
    hire_mo = random.randint(1, 12)
    hire_d = random.randint(1, 28)
    h_date = f"{hire_yr}-{hire_mo:02d}-{hire_d:02d}"
    addr = f"{random.randint(100, 999)} {random.choice(['Oak', 'Maple', 'Cedar', 'Willow', 'Main'])} St, Suite {random.randint(10, 80)}, Los Angeles, CA"
    bank_acc = f"ACCT-US-{random.randint(100000, 899999)}"
    limit = random.choice([2500, 5000, 10000, 15000])
    
    emp_rows.append({
        "Employee_ID": emp_id,
        "Full_Name": name,
        "Email": email,
        "Cost_Center_ID": cc_id,
        "Department": dept,
        "Job_Title": title,
        "Manager_ID": random.choice(["EMP-101", "EMP-102", "EMP-103", "EMP-104"]),
        "Hire_Date": h_date,
        "Residential_Address": addr,
        "Bank_Account_Number": bank_acc,
        "Approval_Limit_USD": limit,
        "Status": "Active"
    })

emp_rows.sort(key=lambda x: int(x["Employee_ID"].split("-")[1]))
df_employees = pd.DataFrame(emp_rows)
df_employees.to_csv(os.path.join(OUTPUT_DIR, "Dim_Employees.csv"), index=False)
print(f"Dim_Employees created: {len(df_employees)} rows")

# ==========================================
# 5. Dim_Vendors
# ==========================================
vendor_base = [
    # Legitimate Vendors
    ("VND-1001", "Global Logistics Freight Co", "94-1182741", "1200 Harbor Dr, Long Beach, CA", "Long Beach", "USA", "ACCT-US-881920", "021000021", "Net 30", "2020-01-15", "EMP-102", "Low", "Yes"),
    ("VND-1002", "Amazon Web Services (AWS)", "91-1928374", "410 Terry Ave N, Seattle, WA", "Seattle", "USA", "ACCT-US-554433", "121000358", "Net 15", "2020-02-01", "EMP-104", "Low", "Yes"),
    ("VND-1003", "Microsoft Azure Cloud", "91-9988776", "One Microsoft Way, Redmond, WA", "Redmond", "USA", "ACCT-US-665544", "121000358", "Net 30", "2020-03-10", "EMP-104", "Low", "Yes"),
    ("VND-1004", "Ernst & Young LLP Audit", "13-5544332", "One Manhattan West, New York, NY", "New York", "USA", "ACCT-US-112233", "021000089", "Net 30", "2020-04-20", "EMP-102", "Low", "Yes"),
    ("VND-1005", "Dell Enterprise Hardware", "74-2233445", "One Dell Way, Round Rock, TX", "Round Rock", "USA", "ACCT-US-998811", "111000614", "Net 30", "2020-06-15", "EMP-104", "Low", "Yes"),
    ("VND-1006", "Staples Business Advantage", "04-2891029", "500 Staples Dr, Framingham, MA", "Framingham", "USA", "ACCT-US-334455", "011000138", "Net 30", "2020-07-01", "EMP-105", "Low", "Yes"),
    ("VND-1007", "Cisco Systems Network", "77-0129384", "170 West Tasman Dr, San Jose, CA", "San Jose", "USA", "ACCT-US-778899", "121000248", "Net 30", "2020-08-14", "EMP-104", "Low", "Yes"),
    ("VND-1008", "KPMG Tax & Advisory", "13-1122998", "345 Park Ave, New York, NY", "New York", "USA", "ACCT-US-223344", "021000089", "Net 30", "2020-09-05", "EMP-102", "Low", "Yes"),
    ("VND-1009", "FedEx Corporate Shipping", "71-0427007", "3610 Hacks Cross Rd, Memphis, TN", "Memphis", "USA", "ACCT-US-445566", "084000026", "Net 15", "2020-10-10", "EMP-105", "Low", "Yes"),
    ("VND-1010", "Salesforce CRM Systems", "94-3320693", "415 Mission St, San Francisco, CA", "San Francisco", "USA", "ACCT-US-556677", "121000358", "Net 30", "2020-11-20", "EMP-103", "Low", "Yes"),
    ("VND-1011", "Iron Mountain Records", "04-2588496", "85 Research Rd, Boston, MA", "Boston", "USA", "ACCT-US-667788", "011000138", "Net 30", "2021-01-12", "EMP-105", "Low", "Yes"),
    ("VND-1012", "Oracle Database Solutions", "94-2805720", "2300 Oracle Way, Austin, TX", "Austin", "USA", "ACCT-US-778800", "111000614", "Net 30", "2021-02-18", "EMP-104", "Low", "Yes"),
    ("VND-1013", "Industrial Power & Utilities", "95-1029384", "400 S Hope St, Los Angeles, CA", "Los Angeles", "USA", "ACCT-US-889911", "122000496", "Net 15", "2021-03-25", "EMP-105", "Low", "Yes"),
    ("VND-1014", "Verizon Business Telecom", "13-3174059", "1095 Ave of the Americas, New York, NY", "New York", "USA", "ACCT-US-990022", "021000089", "Net 30", "2021-04-14", "EMP-104", "Low", "Yes"),
    
    # Forensic Case 3 Target: Summit Logistics Inc (Duplicate invoices & overpayments)
    ("VND-1015", "Summit Logistics Inc", "95-8827361", "8820 Aviation Blvd, Inglewood, CA", "Inglewood", "USA", "ACCT-US-102948", "122000496", "Net 30", "2021-05-19", "EMP-118", "Medium", "Yes"),
    
    # Forensic Case 1 Target: CloudSphere Solutions (Split invoice structuring below $5k limit)
    ("VND-1042", "CloudSphere Solutions LLC", "82-9918273", "2044 Tech Center Pkwy, Irvine, CA", "Irvine", "USA", "ACCT-US-440099", "121000248", "Net 15", "2023-01-10", "EMP-104", "High", "Yes"),
    
    # Forensic Case 2 Target: Shell Vendor Apex Global Consulting Ltd
    # Created by EMP-118 (David Vance), shares SAME Bank Account and Residential Address!
    ("VND-1038", "Apex Global Consulting Ltd", "99-9999999", "742 Evergreen Terrace, Springfield, OR 97477", "Springfield", "USA", "ACCT-US-908812", "123000999", "Immediate", "2024-02-10", "EMP-118", "Critical", "No"),
]

vendor_names_pool = [
    "Pinnacle Facilities Management", "Beacon Media Group", "Vanguard Security Services", "Pacific Coast Packaging", 
    "Aegis Cyber Defense", "Titan Industrial Supplies", "Crestview Office Furniture", "Omni Health Solutions",
    "Nexus Cloud Architecture", "BlueSky Aviation Freight", "Redwood Legal Advisory", "Frontier Telecom Partners",
    "Metro Clean Janitorial", "Highland Real Estate Group", "Silverline Staffing Agency", "Atlas Courier Express",
    "Spectrum Data Analytics", "Trident Safety Equipment", "Zenith Marketing Partners", "Horizon Printing Works",
    "Integra Fleet Management", "Optima Executive Search", "TrueNorth Compliance Services", "Vortex Software Labs",
    "Benchmark Financial Consultants", "Keystone Environmental", "Precision Machine Works", "Alpha Waste Solutions",
    "Sterling Catering Services", "Quantum Digital Media", "AeroSpace Cargo Systems", "Prime Hospitality Partners",
    "Paramount Risk Management", "Dynamic Engineering Corp"
]

existing_vnd_ids = [v[0] for v in vendor_base]
v_counter = 1016
for vname in vendor_names_pool:
    while f"VND-{v_counter}" in existing_vnd_ids:
        v_counter += 1
    vid = f"VND-{v_counter}"
    v_counter += 1
    ein = f"{random.randint(10,99)}-{random.randint(1000000,9999999)}"
    city = random.choice(["Los Angeles", "San Francisco", "Seattle", "Chicago", "Dallas", "New York", "Boston", "Denver"])
    addr = f"{random.randint(100, 9900)} {random.choice(['Wilshire Blvd', 'Market St', 'Grand Ave', 'Commerce Way', 'Broadway'])}, {city}"
    b_acc = f"ACCT-US-{random.randint(100000, 899999)}"
    rout = f"0{random.randint(10000000, 99999999)}"
    terms = random.choice(["Net 30", "Net 30", "Net 15", "Net 60"])
    c_date = f"202{random.randint(1,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    c_by = random.choice(["EMP-102", "EMP-105", "EMP-118"])
    risk = random.choice(["Low", "Low", "Low", "Medium", "High"])
    vendor_base.append((vid, vname, ein, addr, city, "USA", b_acc, rout, terms, c_date, c_by, risk, "Yes"))
    if len(vendor_base) >= 50:
        break

df_vendors = pd.DataFrame(vendor_base, columns=[
    "Vendor_ID", "Vendor_Name", "Tax_ID", "Address", "City", "Country", 
    "Bank_Account_Number", "Bank_Routing_Number", "Payment_Terms", "Creation_Date", 
    "Created_By", "Vendor_Risk_Rating", "Is_Approved_Vendor"
])
df_vendors.sort_values(by="Vendor_ID", inplace=True)
df_vendors.to_csv(os.path.join(OUTPUT_DIR, "Dim_Vendors.csv"), index=False)
print(f"Dim_Vendors created: {len(df_vendors)} rows")

# ==========================================
# 6. Dim_Customers
# ==========================================
cust_names = [
    ("CUST-2001", "Acme Industrial Technologies", "North America", "USA", "Manufacturing", 500000, "2019-03-15", "Net 30", "Preferred"),
    ("CUST-2002", "Globex Global Logistics", "North America", "USA", "Logistics", 750000, "2019-06-20", "Net 30", "Preferred"),
    ("CUST-2003", "Initech Software Corporation", "North America", "USA", "Technology", 400000, "2020-01-10", "Net 30", "Standard"),
    ("CUST-2004", "Umbrella Health Systems", "Europe", "UK", "Healthcare", 1000000, "2020-04-18", "Net 60", "Preferred"),
    ("CUST-2005", "Stark Energy & Robotics", "North America", "USA", "Energy", 1500000, "2020-08-22", "Net 30", "Preferred"),
    ("CUST-2006", "Wayne Financial Holdings", "North America", "USA", "Financial Services", 2000000, "2020-11-05", "Net 30", "Preferred"),
    ("CUST-2007", "Cyberdyne Automated Systems", "Asia Pacific", "Japan", "Technology", 600000, "2021-02-14", "Net 60", "Standard"),
    ("CUST-2008", "Massive Dynamic Biotech", "Europe", "Germany", "Healthcare", 850000, "2021-05-30", "Net 45", "Preferred"),
    ("CUST-2009", "Soylent Consumer Products", "North America", "USA", "Retail", 300000, "2021-09-12", "Net 30", "High Risk"),
    ("CUST-2010", "Hooli Cloud Computing", "North America", "USA", "Technology", 1200000, "2021-12-01", "Net 30", "Preferred"),
]

regions = [("North America", "USA"), ("North America", "Canada"), ("Europe", "UK"), ("Europe", "Germany"), 
           ("Europe", "France"), ("Asia Pacific", "Japan"), ("Asia Pacific", "Australia"), ("Latin America", "Brazil")]
industries = ["Technology", "Healthcare", "Manufacturing", "Retail", "Financial Services", "Energy", "Telecommunications"]
risk_cats = ["Standard", "Standard", "Standard", "Preferred", "High Risk"]

for c_idx in range(2011, 2051):
    cid = f"CUST-{c_idx}"
    cname = f"{random.choice(['Apex', 'Nova', 'Vanguard', 'Pinnacle', 'Summit', 'Sterling', 'Quantum', 'Aura', 'Nexus', 'Echo', 'Horizon', 'Velocity'])} {random.choice(['Enterprises', 'Group', 'Solutions', 'Holdings', 'Industries', 'Dynamics', 'Corp', 'Partners'])}"
    reg, ctry = random.choice(regions)
    ind = random.choice(industries)
    clim = random.choice([150000, 250000, 500000, 750000, 1000000])
    csince = f"202{random.randint(0,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    pterm = random.choice(["Net 30", "Net 30", "Net 45", "Net 60"])
    rcat = random.choice(risk_cats)
    cust_names.append((cid, cname, reg, ctry, ind, clim, csince, pterm, rcat))

df_customers = pd.DataFrame(cust_names, columns=[
    "Customer_ID", "Customer_Name", "Region", "Country", "Industry", 
    "Credit_Limit", "Customer_Since", "Payment_Terms", "Risk_Category"
])
df_customers.to_csv(os.path.join(OUTPUT_DIR, "Dim_Customers.csv"), index=False)
print(f"Dim_Customers created: {len(df_customers)} rows")

# ==========================================
# 7. Fact_Vendor_Invoices_AP
# ==========================================
ap_rows = []
inv_id_counter = 10001
po_id_counter = 50001

all_vendors = df_vendors["Vendor_ID"].tolist()
legit_vendors = [v for v in all_vendors if v not in ["VND-1038", "VND-1042", "VND-1015"]]

# Standard legitimate invoices
for day_idx in range(num_days):
    cur_date = start_date + datetime.timedelta(days=day_idx)
    num_invs = random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1])[0]
    for _ in range(num_invs):
        inv_id = f"AP-INV-{inv_id_counter}"
        inv_id_counter += 1
        po_num = f"PO-{po_id_counter}"
        po_id_counter += 1
        v_id = random.choice(legit_vendors)
        cc_id = random.choice(df_cc["Cost_Center_ID"].tolist())
        
        base_amt = float(np.random.exponential(scale=4500) + 150)
        amt = round(base_amt, 2)
        
        terms_days = random.choice([15, 30, 30, 45, 60])
        due_date = cur_date + datetime.timedelta(days=terms_days)
        
        days_to_pay = random.randint(10, terms_days + 15)
        pay_date = cur_date + datetime.timedelta(days=days_to_pay)
        
        if pay_date <= end_date:
            status = "Paid"
            discount = round(amt * 0.02, 2) if days_to_pay <= 10 and random.random() < 0.3 else 0.0
            paid_amt = round(amt - discount, 2)
            p_date_str = pay_date.strftime("%Y-%m-%d")
        else:
            if cur_date + datetime.timedelta(days=terms_days) < end_date:
                status = "Overdue"
            else:
                status = "Open"
            paid_amt = 0.0
            discount = 0.0
            p_date_str = ""
            
        approver = random.choice(["EMP-102", "EMP-104", "EMP-105", "EMP-118"])
        method = random.choice(["EFT", "ACH Wire", "Corporate Card", "Check"])
        
        ap_rows.append({
            "Invoice_ID": inv_id,
            "Vendor_ID": v_id,
            "PO_Number": po_num,
            "Invoice_Date": cur_date.strftime("%Y-%m-%d"),
            "Due_Date": due_date.strftime("%Y-%m-%d"),
            "Payment_Date": p_date_str,
            "Cost_Center_ID": cc_id,
            "Invoice_Amount": amt,
            "Paid_Amount": paid_amt,
            "Discount_Taken": discount,
            "Payment_Status": status,
            "Approved_By": approver,
            "Payment_Method": method,
            "Is_PO_Matched": "Yes",
            "Notes": "Standard operational vendor invoice verified against goods received."
        })

# Case 1: Split Invoices
split_dates = [
    datetime.date(2024, 3, 12), datetime.date(2024, 3, 14), datetime.date(2024, 3, 15),
    datetime.date(2024, 6, 20), datetime.date(2024, 6, 21), datetime.date(2024, 6, 23),
    datetime.date(2024, 9, 15), datetime.date(2024, 9, 16), datetime.date(2024, 9, 18),
    datetime.date(2024, 11, 10), datetime.date(2024, 11, 12), datetime.date(2024, 11, 13),
    datetime.date(2025, 2, 14), datetime.date(2025, 2, 16), datetime.date(2025, 2, 17),
    datetime.date(2025, 5, 18), datetime.date(2025, 5, 20), datetime.date(2025, 5, 21),
    datetime.date(2025, 8, 10), datetime.date(2025, 8, 12), datetime.date(2025, 8, 14),
    datetime.date(2025, 11, 5), datetime.date(2025, 11, 6), datetime.date(2025, 11, 8)
]

for s_date in split_dates:
    for split_sub in range(2):
        inv_id = f"AP-INV-{inv_id_counter}"
        inv_id_counter += 1
        amt = round(random.uniform(4850.0, 4995.0), 2)
        due_d = s_date + datetime.timedelta(days=15)
        pay_d = s_date + datetime.timedelta(days=10)
        ap_rows.append({
            "Invoice_ID": inv_id,
            "Vendor_ID": "VND-1042",
            "PO_Number": f"PO-{po_id_counter}",
            "Invoice_Date": s_date.strftime("%Y-%m-%d"),
            "Due_Date": due_d.strftime("%Y-%m-%d"),
            "Payment_Date": pay_d.strftime("%Y-%m-%d"),
            "Cost_Center_ID": "CC-300",
            "Invoice_Amount": amt,
            "Paid_Amount": amt,
            "Discount_Taken": 0.0,
            "Payment_Status": "Paid",
            "Approved_By": "EMP-103",
            "Payment_Method": "ACH Wire",
            "Is_PO_Matched": "No",
            "Notes": "Expedited cloud analytics consulting modules - approved under departmental limit."
        })
        po_id_counter += 1

# Case 2: Shell Vendor (Apex Global Consulting VND-1038)
shell_dates = [
    datetime.date(2024, 3, 5), datetime.date(2024, 4, 12), datetime.date(2024, 5, 22),
    datetime.date(2024, 7, 8), datetime.date(2024, 8, 19), datetime.date(2024, 10, 14),
    datetime.date(2024, 12, 10), datetime.date(2025, 1, 15), datetime.date(2025, 3, 20),
    datetime.date(2025, 5, 11), datetime.date(2025, 7, 18), datetime.date(2025, 9, 25),
    datetime.date(2025, 11, 30)
]

for s_date in shell_dates:
    inv_id = f"AP-INV-{inv_id_counter}"
    inv_id_counter += 1
    amt = round(random.uniform(16500.0, 24800.0), 2)
    due_d = s_date + datetime.timedelta(days=1)
    pay_d = s_date + datetime.timedelta(days=2)
    ap_rows.append({
        "Invoice_ID": inv_id,
        "Vendor_ID": "VND-1038",
        "PO_Number": "NONE-EMERGENCY",
        "Invoice_Date": s_date.strftime("%Y-%m-%d"),
        "Due_Date": due_d.strftime("%Y-%m-%d"),
        "Payment_Date": pay_d.strftime("%Y-%m-%d"),
        "Cost_Center_ID": "CC-500",
        "Invoice_Amount": amt,
        "Paid_Amount": amt,
        "Discount_Taken": 0.0,
        "Payment_Status": "Paid",
        "Approved_By": "EMP-118",
        "Payment_Method": "ACH Wire",
        "Is_PO_Matched": "No",
        "Notes": "Executive supply chain optimization & strategic restructuring advisory retainer."
    })

# Case 3: Duplicate Payments & Near-Duplicates
dup_scenarios = [
    (datetime.date(2024, 4, 10), 18450.00, "AP-INV-77102", "AP-INV-77102-DUP"),
    (datetime.date(2024, 8, 15), 24800.00, "AP-INV-81204", "AP-INV-81204A"),
    (datetime.date(2025, 3, 10), 19750.50, "AP-INV-92011", "AP-INV-92011 "),
    (datetime.date(2025, 9, 18), 31200.00, "AP-INV-99401", "AP-INV-99401-1")
]

for orig_date, dup_amt, inv1, inv2 in dup_scenarios:
    ap_rows.append({
        "Invoice_ID": inv1,
        "Vendor_ID": "VND-1015",
        "PO_Number": f"PO-{po_id_counter}",
        "Invoice_Date": orig_date.strftime("%Y-%m-%d"),
        "Due_Date": (orig_date + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        "Payment_Date": (orig_date + datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
        "Cost_Center_ID": "CC-500",
        "Invoice_Amount": dup_amt,
        "Paid_Amount": dup_amt,
        "Discount_Taken": 0.0,
        "Payment_Status": "Paid",
        "Approved_By": "EMP-118",
        "Payment_Method": "ACH Wire",
        "Is_PO_Matched": "Yes",
        "Notes": "Heavy freight logistics delivery across Western distribution hubs."
    })
    po_id_counter += 1
    
    dup_date = orig_date + datetime.timedelta(days=14)
    ap_rows.append({
        "Invoice_ID": inv2,
        "Vendor_ID": "VND-1015",
        "PO_Number": f"PO-{po_id_counter}",
        "Invoice_Date": dup_date.strftime("%Y-%m-%d"),
        "Due_Date": (dup_date + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        "Payment_Date": (dup_date + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
        "Cost_Center_ID": "CC-500",
        "Invoice_Amount": dup_amt,
        "Paid_Amount": dup_amt,
        "Discount_Taken": 0.0,
        "Payment_Status": "Paid",
        "Approved_By": "EMP-118",
        "Payment_Method": "Check",
        "Is_PO_Matched": "No",
        "Notes": "Duplicate freight billing - processed on alternative payment cycle."
    })
    po_id_counter += 1

df_ap = pd.DataFrame(ap_rows)
df_ap.sort_values(by="Invoice_Date", inplace=True)
df_ap.to_csv(os.path.join(OUTPUT_DIR, "Fact_Vendor_Invoices_AP.csv"), index=False)
print(f"Fact_Vendor_Invoices_AP created: {len(df_ap)} rows")

# ==========================================
# 8. Fact_Sales_Invoices_AR
# ==========================================
ar_rows = []
ar_id_counter = 20001
sales_reps = ["EMP-103", "EMP-129", "EMP-133", "EMP-120", "EMP-125", "EMP-130"]

for day_idx in range(num_days):
    cur_date = start_date + datetime.timedelta(days=day_idx)
    num_sales = random.choices([2, 3, 4, 5, 6], weights=[0.1, 0.3, 0.3, 0.2, 0.1])[0]
    for _ in range(num_sales):
        sinv_id = f"AR-INV-{ar_id_counter}"
        ar_id_counter += 1
        cust_id = random.choice(df_customers["Customer_ID"].tolist())
        s_rep = random.choice(sales_reps)
        
        gross_amt = round(float(np.random.gamma(shape=3.0, scale=3500) + 1200), 2)
        disc_pct = round(random.choices([0.0, 0.03, 0.05, 0.08, 0.10], weights=[0.4, 0.25, 0.2, 0.1, 0.05])[0], 2)
        
        # Case 6: Excessive unauthorized discounts by Rachel Zane (EMP-133)
        if s_rep == "EMP-133" and cur_date.month in [3, 6, 9, 12] and cur_date.day >= 20:
            disc_pct = round(random.uniform(0.30, 0.42), 2)
            
        disc_amt = round(gross_amt * disc_pct, 2)
        net_amt = round(gross_amt - disc_amt, 2)
        cogs_amt = round(gross_amt * random.uniform(0.42, 0.58), 2)
        
        due_d = cur_date + datetime.timedelta(days=30)
        days_to_pay = random.randint(15, 65)
        pay_d = cur_date + datetime.timedelta(days=days_to_pay)
        
        if pay_d <= end_date:
            status = "Paid"
            p_date_str = pay_d.strftime("%Y-%m-%d")
        else:
            if due_d < end_date:
                status = random.choice(["Overdue", "Overdue", "Bad Debt Written Off"])
            else:
                status = "Outstanding"
            p_date_str = ""
            
        ar_rows.append({
            "Sales_Invoice_ID": sinv_id,
            "Customer_ID": cust_id,
            "Sales_Rep_ID": s_rep,
            "Invoice_Date": cur_date.strftime("%Y-%m-%d"),
            "Due_Date": due_d.strftime("%Y-%m-%d"),
            "Payment_Date": p_date_str,
            "Gross_Sales_Amount": gross_amt,
            "Discount_Amount": disc_amt,
            "Discount_Percentage": disc_pct,
            "Net_Sales_Amount": net_amt,
            "Cost_of_Sales": cogs_amt,
            "Payment_Status": status,
            "Region": df_customers.loc[df_customers["Customer_ID"] == cust_id, "Region"].values[0]
        })

df_ar = pd.DataFrame(ar_rows)
df_ar.sort_values(by="Invoice_Date", inplace=True)
df_ar.to_csv(os.path.join(OUTPUT_DIR, "Fact_Sales_Invoices_AR.csv"), index=False)
print(f"Fact_Sales_Invoices_AR created: {len(df_ar)} rows")

# ==========================================
# 9. Fact_Employee_Expenses_TE
# ==========================================
te_rows = []
exp_id_counter = 30001
merchants = {
    "Airfare": ["Delta Air Lines", "United Airlines", "American Airlines", "British Airways", "Lufthansa"],
    "Lodging": ["Marriott International", "Hilton Hotels", "Hyatt Regency", "Sheraton Grand", "Westin Suites"],
    "Meals & Entertainment": ["Ruth's Chris Steak House", "Capital Grille", "Morton's The Steakhouse", "Ocean Prime", "Local Bistro & Cafe", "Starbucks Coffee"],
    "Ground Transport": ["Uber Technologies", "Lyft Inc", "Hertz Car Rental", "Avis Rent A Car", "Yellow Cab Co"],
    "Tech Hardware": ["Apple Store", "Best Buy Enterprise", "CDW Direct", "B&H Photo Video"],
    "Office Misc": ["Office Depot", "Staples Direct", "FedEx Office", "Amazon Prime Business"]
}

emp_ids = df_employees["Employee_ID"].tolist()

for day_idx in range(num_days):
    cur_date = start_date + datetime.timedelta(days=day_idx)
    num_exps = random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1])[0]
    for _ in range(num_exps):
        exp_id = f"EXP-{exp_id_counter}"
        exp_id_counter += 1
        emp = random.choice(emp_ids)
        if emp == "EMP-129":
            continue
            
        cat = random.choice(list(merchants.keys()))
        merchant = random.choice(merchants[cat])
        city = random.choice(["Los Angeles", "New York", "Chicago", "San Francisco", "Dallas", "Seattle", "Atlanta", "London"])
        
        if cat == "Airfare":
            amt = round(random.uniform(350, 1400), 2)
        elif cat == "Lodging":
            amt = round(random.uniform(180, 850), 2)
        elif cat == "Meals & Entertainment":
            amt = round(random.uniform(25, 220), 2)
        elif cat == "Ground Transport":
            amt = round(random.uniform(18, 95), 2)
        elif cat == "Tech Hardware":
            amt = round(random.uniform(150, 1200), 2)
        else:
            amt = round(random.uniform(30, 250), 2)
            
        sub_date = cur_date + datetime.timedelta(days=random.randint(1, 10))
        receipt = "Yes" if random.random() > 0.05 else "No"
        status = "Approved"
        appr_amt = amt
        
        te_rows.append({
            "Expense_ID": exp_id,
            "Employee_ID": emp,
            "Cost_Center_ID": df_employees.loc[df_employees["Employee_ID"] == emp, "Cost_Center_ID"].values[0],
            "Expense_Date": cur_date.strftime("%Y-%m-%d"),
            "Submission_Date": sub_date.strftime("%Y-%m-%d"),
            "Category": cat,
            "Merchant_Name": merchant,
            "City": city,
            "Claim_Amount": amt,
            "Approved_Amount": appr_amt,
            "Receipt_Attached": receipt,
            "Approved_By": df_employees.loc[df_employees["Employee_ID"] == emp, "Manager_ID"].values[0] if df_employees.loc[df_employees["Employee_ID"] == emp, "Manager_ID"].values[0] != "" else "EMP-101",
            "Approval_Status": status,
            "Payment_Date": (sub_date + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        })

# Case 5: Fictitious T&E Claims by Julian Thorne (EMP-129)
for day_idx in range(num_days):
    cur_date = start_date + datetime.timedelta(days=day_idx)
    if cur_date.isoweekday() in [6, 7]:
        exp_id = f"EXP-{exp_id_counter}"
        exp_id_counter += 1
        amt = round(random.uniform(142.50, 149.95), 2)
        fake_merchant = random.choice(["Luxury VIP Lounge Club", "Executive Cigar & Wine Cellar", "Platinum Sky Lounge", "Private Dining Room Riviera", "Apex Gastronomy Club"])
        sub_d = cur_date + datetime.timedelta(days=1)
        te_rows.append({
            "Expense_ID": exp_id,
            "Employee_ID": "EMP-129",
            "Cost_Center_ID": "CC-300",
            "Expense_Date": cur_date.strftime("%Y-%m-%d"),
            "Submission_Date": sub_d.strftime("%Y-%m-%d"),
            "Category": "Meals & Entertainment",
            "Merchant_Name": fake_merchant,
            "City": "Los Angeles",
            "Claim_Amount": amt,
            "Approved_Amount": amt,
            "Receipt_Attached": "No",
            "Approved_By": "EMP-103",
            "Approval_Status": "Approved",
            "Payment_Date": (sub_d + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        })

df_te = pd.DataFrame(te_rows)
df_te.sort_values(by="Expense_Date", inplace=True)
df_te.to_csv(os.path.join(OUTPUT_DIR, "Fact_Employee_Expenses_TE.csv"), index=False)
print(f"Fact_Employee_Expenses_TE created: {len(df_te)} rows")

# ==========================================
# 10. Fact_GL_Journal_Entries (General Ledger)
# ==========================================
gl_rows = []
je_counter = 40001

def add_journal_entry(date_obj, posting_time_str, je_type, desc, posted_by, approved_by, is_manual, doc_ref, lines):
    global je_counter
    je_id = f"JE-{date_obj.year}-{je_counter:05d}"
    je_counter += 1
    period_key = int(date_obj.strftime("%Y%m"))
    timestamp = f"{date_obj.strftime('%Y-%m-%d')} {posting_time_str}"
    
    # Ensure perfect balancing to the cent
    tot_debit = round(sum(l["Debit"] for l in lines), 2)
    tot_credit = round(sum(l["Credit"] for l in lines), 2)
    diff = round(tot_debit - tot_credit, 2)
    
    if diff != 0:
        # adjust last credit or debit line
        if diff > 0:
            lines[-1]["Credit"] = round(lines[-1]["Credit"] + diff, 2)
        else:
            lines[-1]["Debit"] = round(lines[-1]["Debit"] - diff, 2)
            
    for line_idx, line in enumerate(lines, 1):
        gl_rows.append({
            "Journal_ID": je_id,
            "Line_ID": line_idx,
            "Posting_Date": date_obj.strftime("%Y-%m-%d"),
            "Posting_Timestamp": timestamp,
            "Period_Key": period_key,
            "Account_Number": line["Account_Number"],
            "Cost_Center_ID": line["Cost_Center_ID"],
            "Debit": round(line["Debit"], 2),
            "Credit": round(line["Credit"], 2),
            "Transaction_Type": je_type,
            "Description": desc,
            "Posted_By": posted_by,
            "Approved_By": approved_by,
            "Is_Manual": is_manual,
            "Document_Reference": doc_ref
        })

# 10.1 Recurring payroll entries
for y in [2024, 2025]:
    for m in range(1, 13):
        for p_day in [15, 28]:
            p_date = datetime.date(y, m, p_day)
            sal_amt = round(185000.00 + random.uniform(-5000, 5000), 2)
            ben_amt = round(sal_amt * 0.22, 2)
            tax_amt = round(sal_amt * 0.15, 2)
            net_pay = round(sal_amt + ben_amt - tax_amt, 2)
            
            lines = [
                {"Account_Number": 6010, "Cost_Center_ID": "CC-200", "Debit": sal_amt, "Credit": 0.0},
                {"Account_Number": 6020, "Cost_Center_ID": "CC-200", "Debit": ben_amt, "Credit": 0.0},
                {"Account_Number": 2030, "Cost_Center_ID": "CC-200", "Debit": 0.0, "Credit": tax_amt},
                {"Account_Number": 1020, "Cost_Center_ID": "CC-200", "Debit": 0.0, "Credit": net_pay}
            ]
            add_journal_entry(p_date, "09:00:00", "Automated Recurring", f"Semi-monthly payroll run - Period {y}-{m:02d}", "SYSTEM_PAYROLL", "EMP-102", 0, f"PAY-{y}{m:02d}-{p_day}", lines)

# 10.2 AP Invoices GL posting
for _, ap in df_ap.iterrows():
    inv_d = datetime.datetime.strptime(ap["Invoice_Date"], "%Y-%m-%d").date()
    amt = round(float(ap["Invoice_Amount"]), 2)
    
    if ap["Vendor_ID"] == "VND-1038":
        exp_acc = 6030
    elif ap["Vendor_ID"] == "VND-1042":
        exp_acc = 6060
    elif ap["Vendor_ID"] == "VND-1015":
        exp_acc = 5010
    else:
        exp_acc = random.choice([5010, 6030, 6050, 6060, 6070, 9100])
        
    lines = [
        {"Account_Number": exp_acc, "Cost_Center_ID": ap["Cost_Center_ID"], "Debit": amt, "Credit": 0.0},
        {"Account_Number": 2010, "Cost_Center_ID": ap["Cost_Center_ID"], "Debit": 0.0, "Credit": amt}
    ]
    add_journal_entry(inv_d, "10:30:00", "Standard Subledger Post", f"AP Invoice booking - {ap['Vendor_ID']}", "SYSTEM_AP", ap["Approved_By"], 0, ap["Invoice_ID"], lines)
    
    if ap["Payment_Status"] == "Paid" and ap["Payment_Date"] != "":
        pay_d = datetime.datetime.strptime(ap["Payment_Date"], "%Y-%m-%d").date()
        paid_amt = round(float(ap["Paid_Amount"]), 2)
        disc = round(float(ap["Discount_Taken"]), 2)
        pay_lines = [
            {"Account_Number": 2010, "Cost_Center_ID": ap["Cost_Center_ID"], "Debit": amt, "Credit": 0.0},
            {"Account_Number": 1010, "Cost_Center_ID": ap["Cost_Center_ID"], "Debit": 0.0, "Credit": paid_amt}
        ]
        if disc > 0:
            pay_lines.append({"Account_Number": 4090, "Cost_Center_ID": ap["Cost_Center_ID"], "Debit": 0.0, "Credit": disc})
        add_journal_entry(pay_d, "14:15:00", "Standard Payment Clearing", f"AP Payment settlement - {ap['Vendor_ID']}", "SYSTEM_AP", "EMP-102", 0, f"PAY-{ap['Invoice_ID']}", pay_lines)

# 10.3 AR Sales GL posting
for _, ar in df_ar.iterrows():
    inv_d = datetime.datetime.strptime(ar["Invoice_Date"], "%Y-%m-%d").date()
    net = round(float(ar["Net_Sales_Amount"]), 2)
    cogs = round(float(ar["Cost_of_Sales"]), 2)
    
    rev_lines = [
        {"Account_Number": 1200, "Cost_Center_ID": "CC-300", "Debit": net, "Credit": 0.0},
        {"Account_Number": 4010, "Cost_Center_ID": "CC-300", "Debit": 0.0, "Credit": net}
    ]
    add_journal_entry(inv_d, "11:00:00", "Standard Subledger Post", f"Sales revenue recognition - {ar['Customer_ID']}", "SYSTEM_AR", ar["Sales_Rep_ID"], 0, ar["Sales_Invoice_ID"], rev_lines)
    
    cogs_lines = [
        {"Account_Number": 5010, "Cost_Center_ID": "CC-500", "Debit": cogs, "Credit": 0.0},
        {"Account_Number": 1300, "Cost_Center_ID": "CC-500", "Debit": 0.0, "Credit": cogs}
    ]
    add_journal_entry(inv_d, "11:00:05", "Standard Subledger Post", f"Inventory relief COGS - {ar['Sales_Invoice_ID']}", "SYSTEM_AR", ar["Sales_Rep_ID"], 0, ar["Sales_Invoice_ID"], cogs_lines)

# Case 4: Weekend / Off-Hours Manual Journal Entries
fraud_manual_dates = [
    (datetime.date(2024, 2, 17), "23:48:12", 45000.00, 9100, "Quarterly unallocated expense reclassification adjustment"),
    (datetime.date(2024, 5, 25), "23:35:44", 62000.00, 9100, "Intercompany variance write-off"),
    (datetime.date(2024, 8, 17), "23:52:10", 54000.00, 6030, "Special advisory consulting services reclass"),
    (datetime.date(2024, 11, 23), "23:41:05", 78000.00, 9100, "Year-end clearing adjustment suspense"),
    (datetime.date(2025, 2, 22), "23:55:18", 49000.00, 9100, "Sundry expense allocation plug"),
    (datetime.date(2025, 5, 24), "23:39:29", 83000.00, 6030, "Strategic consulting clearing entry"),
    (datetime.date(2025, 8, 23), "23:47:50", 67000.00, 9100, "Management discretion clearing"),
    (datetime.date(2025, 11, 22), "23:50:11", 95000.00, 9100, "Late close suspense account adjustment")
]

for f_date, f_time, f_amt, deb_acc, f_desc in fraud_manual_dates:
    f_lines = [
        {"Account_Number": deb_acc, "Cost_Center_ID": "CC-200", "Debit": f_amt, "Credit": 0.0},
        {"Account_Number": 1010, "Cost_Center_ID": "CC-200", "Debit": 0.0, "Credit": f_amt}
    ]
    add_journal_entry(f_date, f_time, "Manual Adjustment", f_desc, "EMP-105", "", 1, "MAN-ADJ-OVERRIDE", f_lines)

# Standard monthly depreciation entries
for y in [2024, 2025]:
    for m in range(1, 13):
        eom = datetime.date(y, m, 28)
        dep_amt = 42500.00
        dep_lines = [
            {"Account_Number": 7010, "Cost_Center_ID": "CC-200", "Debit": dep_amt, "Credit": 0.0},
            {"Account_Number": 1550, "Cost_Center_ID": "CC-200", "Debit": 0.0, "Credit": dep_amt}
        ]
        add_journal_entry(eom, "17:00:00", "Manual Adjustment", f"Monthly depreciation recognition - {y}-{m:02d}", "EMP-105", "EMP-102", 1, f"ADJ-DEP-{y}{m:02d}", dep_lines)

df_gl = pd.DataFrame(gl_rows)
df_gl.sort_values(by=["Posting_Date", "Journal_ID", "Line_ID"], inplace=True)
df_gl.to_csv(os.path.join(OUTPUT_DIR, "Fact_GL_Journal_Entries.csv"), index=False)
print(f"Fact_GL_Journal_Entries created: {len(df_gl)} rows")

# ==========================================
# 11. Fact_Bank_Statements
# ==========================================
bank_rows = []
b_id_counter = 50001

for y in [2024, 2025]:
    for m in range(1, 13):
        st_date = datetime.date(y, m, 28)
        month_ar_paid = df_ar[(pd.to_datetime(df_ar["Payment_Date"]).dt.year == y) & (pd.to_datetime(df_ar["Payment_Date"]).dt.month == m)]
        tot_dep = round(month_ar_paid["Net_Sales_Amount"].sum(), 2)
        
        month_ap_paid = df_ap[(pd.to_datetime(df_ap["Payment_Date"]).dt.year == y) & (pd.to_datetime(df_ap["Payment_Date"]).dt.month == m)]
        tot_wire = round(month_ap_paid["Paid_Amount"].sum(), 2)
        
        bank_rows.append({
            "Bank_Trans_ID": f"BNK-{b_id_counter}",
            "Statement_Date": st_date.strftime("%Y-%m-%d"),
            "Transaction_Type": "ACH Customer Receipts Deposit",
            "Reference_Number": f"DEP-{y}{m:02d}",
            "Amount": tot_dep,
            "GL_Reference_Account": 1010,
            "Is_Reconciled": 1,
            "Reconciliation_Notes": "Matched with AR batch settlements."
        })
        b_id_counter += 1
        
        bank_rows.append({
            "Bank_Trans_ID": f"BNK-{b_id_counter}",
            "Statement_Date": st_date.strftime("%Y-%m-%d"),
            "Transaction_Type": "ACH Vendor Wire Outflows",
            "Reference_Number": f"WIR-{y}{m:02d}",
            "Amount": -tot_wire,
            "GL_Reference_Account": 1010,
            "Is_Reconciled": 1,
            "Reconciliation_Notes": "Matched with AP disbursements."
        })
        b_id_counter += 1
        
        bank_rows.append({
            "Bank_Trans_ID": f"BNK-{b_id_counter}",
            "Statement_Date": st_date.strftime("%Y-%m-%d"),
            "Transaction_Type": "Bank Service Fee",
            "Reference_Number": f"FEE-{y}{m:02d}",
            "Amount": -450.00,
            "GL_Reference_Account": 9100,
            "Is_Reconciled": 1,
            "Reconciliation_Notes": "Standard monthly treasury maintenance fee."
        })
        b_id_counter += 1

df_bank = pd.DataFrame(bank_rows)
df_bank.to_csv(os.path.join(OUTPUT_DIR, "Fact_Bank_Statements.csv"), index=False)
print(f"Fact_Bank_Statements created: {len(df_bank)} rows")
print("\nDataset generation finished with 100% precision.")
