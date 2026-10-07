import pandas as pd
import numpy as np

data_dir = '/home/user/soulfyas-restaurant-erp/PowerBI_Forensic_Accounting_Course/data'
ap = pd.read_csv(data_dir + '/Fact_Vendor_Invoices_AP.csv')
ar = pd.read_csv(data_dir + '/Fact_Sales_Invoices_AR.csv')
gl = pd.read_csv(data_dir + '/Fact_GL_Journal_Entries.csv')
te = pd.read_csv(data_dir + '/Fact_Employee_Expenses_TE.csv')
emp = pd.read_csv(data_dir + '/Dim_Employees.csv')
vnd = pd.read_csv(data_dir + '/Dim_Vendors.csv')
coa = pd.read_csv(data_dir + '/Dim_Chart_of_Accounts.csv')

print('=== FINANCIAL SUMMARY ===')
tot_rev = ar['Net_Sales_Amount'].sum()
tot_cogs = ar['Cost_of_Sales'].sum()
gross_profit = tot_rev - tot_cogs
print(f'Total Net Revenue: ${tot_rev:,.2f}')
print(f'Total COGS:        ${tot_cogs:,.2f}')
print(f'Gross Profit:      ${gross_profit:,.2f} ({gross_profit/tot_rev*100:.1f}%)')
print(f'Total AP Invoices: {len(ap):,} | Total AP Spend: ${ap["Invoice_Amount"].sum():,.2f}')

print('\n=== CASE 1: SPLIT INVOICES (VND-1042 CloudSphere Solutions) ===')
c1 = ap[ap['Vendor_ID'] == 'VND-1042']
print(f'Count of Invoices: {len(c1)}')
print(f'Total Amount: ${c1["Invoice_Amount"].sum():,.2f}')
print(f'Min Amount: ${c1["Invoice_Amount"].min():,.2f} | Max Amount: ${c1["Invoice_Amount"].max():,.2f}')
print(f'Approved By: {c1["Approved_By"].unique()}')

print('\n=== CASE 2: SHELL VENDOR (VND-1038 Apex Global Consulting) ===')
c2 = ap[ap['Vendor_ID'] == 'VND-1038']
print(f'Count of Invoices: {len(c2)}')
print(f'Total Amount: ${c2["Invoice_Amount"].sum():,.2f}')
print(f'Approved By: {c2["Approved_By"].unique()}')
vnd_38 = vnd[vnd['Vendor_ID'] == 'VND-1038'].iloc[0]
emp_match = emp[emp['Bank_Account_Number'] == vnd_38['Bank_Account_Number']]
print(f'Vendor Bank Acct: {vnd_38["Bank_Account_Number"]} | Matched Employee: {emp_match["Full_Name"].values[0]} ({emp_match["Employee_ID"].values[0]})')
print(f'Address Match: Vendor "{vnd_38["Address"]}" == Employee "{emp_match["Residential_Address"].values[0]}"')

print('\n=== CASE 3: DUPLICATE INVOICES (VND-1015 Summit Logistics) ===')
c3_dups = ap[ap['Vendor_ID'] == 'VND-1015']
print(f'Summit Logistics Invoices: {len(c3_dups)}')
dup_pairs = [('AP-INV-77102', 'AP-INV-77102-DUP', 18450.00), ('AP-INV-81204', 'AP-INV-81204A', 24800.00), ('AP-INV-92011', 'AP-INV-92011 ', 19750.50), ('AP-INV-99401', 'AP-INV-99401-1', 31200.00)]
tot_dup = sum(p[2] for p in dup_pairs)
print(f'Duplicate Pairs Total Excess Paid: ${tot_dup:,.2f}')

print('\n=== CASE 4: OFF-HOURS MANUAL JOURNAL ENTRIES ===')
manual_jes = gl[gl['Is_Manual'] == 1]
off_hours = gl[gl['Document_Reference'] == 'MAN-ADJ-OVERRIDE']
print(f'Off-Hours Suspicious Entries: {len(off_hours)} lines ({len(off_hours["Journal_ID"].unique())} unique journals)')
print(f'Total Debited: ${off_hours[off_hours["Debit"] > 0]["Debit"].sum():,.2f}')
print(f'Accounts Debited: {off_hours[off_hours["Debit"] > 0]["Account_Number"].unique()}')
print(f'Posted By: {off_hours["Posted_By"].unique()} | Approvals: {off_hours["Approved_By"].unique()}')

print('\n=== CASE 5: FICTITIOUS T&E EXPENSES (EMP-129 Julian Thorne) ===')
c5 = te[te['Employee_ID'] == 'EMP-129']
print(f'Count of Claims: {len(c5)}')
print(f'Total Claimed: ${c5["Claim_Amount"].sum():,.2f}')
print(f'Missing Receipts: {(c5["Receipt_Attached"] == "No").sum()} out of {len(c5)}')
print(f'Avg Claim: ${c5["Claim_Amount"].mean():,.2f}')

print('\n=== CASE 6: EXCESSIVE DISCOUNTS (EMP-133 Rachel Zane) ===')
c6_rz = ar[ar['Sales_Rep_ID'] == 'EMP-133']
c6_others = ar[ar['Sales_Rep_ID'] != 'EMP-133']
print(f'Rachel Zane Avg Discount: {c6_rz["Discount_Percentage"].mean()*100:.1f}% | Total Discount $: ${c6_rz["Discount_Amount"].sum():,.2f}')
print(f'Other Reps Avg Discount:  {c6_others["Discount_Percentage"].mean()*100:.1f}%')
q_end_rz = c6_rz[c6_rz['Discount_Percentage'] > 0.20]
print(f'Rachel Zane High Discounts (>20%): {len(q_end_rz)} invoices, Total High Discount Value: ${q_end_rz["Discount_Amount"].sum():,.2f}')

# First-digit distribution (Benford's Law)
print('\n=== CASE 7: BENFORD\'S LAW FIRST-DIGIT DISTRIBUTION ===')
gl_expenses = gl[(gl['Account_Number'] >= 5000) & (gl['Debit'] > 0)]
first_digits_all = gl_expenses['Debit'].astype(str).str.extract(r'([1-9])')[0].astype(int)
print('All Expenses First-Digit Dist:')
print((first_digits_all.value_counts(normalize=True).sort_index() * 100).round(1).to_dict())

gl_9100 = gl[(gl['Account_Number'] == 9100) & (gl['Debit'] > 0)]
first_digits_9100 = gl_9100['Debit'].astype(str).str.extract(r'([1-9])')[0].astype(int)
print('Account 9100 First-Digit Dist (Anomalous):')
print((first_digits_9100.value_counts(normalize=True).sort_index() * 100).round(1).to_dict())
