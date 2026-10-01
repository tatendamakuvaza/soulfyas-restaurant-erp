# Soulfyas Quality Restaurant ERP

An enterprise-grade, multi-module Restaurant ERP built with Streamlit, SQLAlchemy, ReportLab, and pandas. Designed for hospitality operations with point of sale (POS), live kitchen display system (KDS), floor and table management, recipes and automated stock depletion (Bill of Materials), inventory control, IFRS 18 financial statements, Zimbabwe statutory tax & payroll (ZIMRA & NSSA), double-entry general ledger, and branded PDF generation.

---

## 🍽️ Key Modules & Capabilities

### 1. Executive Dashboard & Real-Time KPIs
- Live revenue, daily order volume, average check size, daily expenses, and net profit.
- Low-stock critical alerts banner with instant reorder triggers.
- Active table occupancy tracking.
- Interactive sales trend charts and top 5 best-selling menu items.

### 2. Point of Sale (POS) & Fast Checkout
- Interactive menu grid with category filtering and real-time dish search.
- Dietary tags (🌱 Vegetarian, 🌶️ Spicy) and prep time indicators.
- Multi-order types: **Dine-In** (with table selection), **Takeaway**, and **Delivery**.
- Customer loyalty lookup & assignment.
- Automated 15% ZIMRA VAT calculation, discounts, and tips/gratuities.
- Multi-payment support: Cash, Card (Visa/Swipe), Ecocash/Mobile Money, Bank Transfer, Credit.
- **Automated Recipe Depletion**: Every POS sale automatically deducts raw ingredients from inventory.
- Real-time generation and instant download of branded **POS Tax Receipts (PDF)**.

### 3. Kitchen Display System (KDS) & Floor Management
- Live Kitchen Order Ticket (KOT) board for chefs and kitchen staff.
- Order progression workflow: **⏳ Pending -> 🍳 In Preparation -> 🛎️ Ready for Service -> ✅ Served**.
- Visual interactive floor plan organized by dining sections: Main Dining, Garden/Patio, VIP Lounge, Bar Counter.
- Real-time table occupancy status toggling (Available, Occupied, Reserved, Cleaning).

### 4. Recipes, Food Costing & Bill of Materials (BOM)
- Formulate dishes with exact ingredient consumption quantities (e.g. whole chicken, spices, cooking oil, potatoes).
- Automatic calculation of food cost per dish and gross profit margin percentage.
- Real-time inventory synchronization on sale.

### 5. Inventory, Stock Movements & Food Wastage
- Stock balances, units of measure, unit costs, and total inventory valuation.
- Quick restock delivery receiving tool.
- Immutable stock movements audit trail.
- Kitchen food loss and spillage tracker with reason codes.
- Exportable **Inventory Valuation Report (PDF & CSV)**.

### 6. IFRS 18 Financial Statements & General Ledger
- Compliant with **IFRS 18 Presentation and Disclosure in Financial Statements** (effective 2027).
- Structured into **Operating, Investing, and Financing** categories.
- **Statement of Profit or Loss**: Operating Revenue, COGS, Gross Profit, Operating Expenses, Operating Profit subtotal, Financing/IMTT, and Net Period Surplus.
- **Statement of Financial Position (Balance Sheet)**.
- **Direct Method Statement of Cash Flows**.
- **Management Performance Measures (MPMs)**: Food Cost %, Gross Margin %, Operating EBITDA Margin.
- **Double-Entry Journal Adjustments** with real-time balanced Debit == Credit validation.
- Complete IFRS Chart of Accounts.
- Single-click **Official Financial Statements Report (PDF & CSV)**.

### 7. Zimbabwe Tax Hub & Statutory Payroll (ZIMRA & NSSA)
- **ZIMRA VAT 7 Return Summary**: Standard 15% VAT on output sales vs input allowable purchases.
- **Statutory PAYE Engine**: Official USD progressive monthly tax brackets + 3% AIDS Levy.
- **NSSA POBS Pension Scheme**: 4.5% Employee + 4.5% Employer (capped at insurable ceiling).
- **NSSA APWCS**: 1.4% Employer Workers Compensation Scheme.
- **IMTT 2% Calculation**: Intermediated Money Transfer Tax on electronic transfers.
- **Confidential Employee Payslip Generator (PDF)** with full earnings and statutory deductions breakdown.
- Tax return filing and payment logging.

### 8. People, Organisation Structure & CRM
- 6 Executive Directorates (Finance, Operations, Commercial, People, Technology, Governance & Risk) and 31 departmental units.
- Employee profiles, job titles, national IDs, NSSA numbers, and salary scales.
- Customer CRM with repeat visit tracking, lifetime spend, and loyalty points.

### 9. Administration, Security & Audit Trail
- Granular Role-Based Access Control (Admin, Manager, Cashier, Chef, Accountant, Waiter).
- Tamper-evident system audit log tracking sales, stock movements, journal postings, and settings changes.
- Multi-branch configuration and functional currency switcher (USD, ZiG, ZAR, GBP, EUR).

---

## 🚀 Getting Started

### Local Development (Zero-Config SQLite)
```bash
# Clone the repository
git clone https://github.com/tatendamakuvaza/soulfyas-restaurant-erp.git
cd soulfyas-restaurant-erp

# Install dependencies
pip install -r requirements.txt

# Launch the ERP application
streamlit run app.py
```

### Initial Credentials
- **Administrator**: `admin` / `ChangeMe123!`
- **General Manager**: `manager` / `Soulfyas2026!`
- **Head Cashier**: `cashier` / `Soulfyas2026!`
- **Head Chef**: `chef` / `Soulfyas2026!`
- **Accountant**: `accountant` / `Soulfyas2026!`

---

## ☁️ Production Deployment (Streamlit Cloud & Neon PostgreSQL)

1. Push your repository to GitHub.
2. Link the repository to **Streamlit Community Cloud**.
3. In Streamlit Cloud **Settings > Secrets**, configure:
   ```toml
   DATABASE_URL = "postgresql+psycopg://username:password@ep-sample-pooler.neon.tech/soulfyas_db?sslmode=require"
   ```
4. The database layer automatically detects PostgreSQL, initializes all normalized tables, and applies schema compatibility.

---

## 📄 License
Proprietary & Confidential - Soulfyas Quality Restaurant Investments (Pvt) Ltd.
