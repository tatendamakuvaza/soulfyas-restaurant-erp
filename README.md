# Soulfyas Quality Restaurant ERP

A Streamlit restaurant ERP starter with secure login, administrator-created employee accounts, point of sale, invoices, menu, expenses, inventory, customers/suppliers, financial statements and settings.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

First login: `admin` / `ChangeMe123!`. Change it immediately by creating a new admin account and disabling the default account in the database before production use.

## Deploy on Streamlit

1. Put `app.py`, `requirements.txt`, `soulfyas_logo.png` and this README in GitHub.
2. Create a Streamlit Community Cloud app using `app.py`.
3. Add `DATABASE_URL` in Secrets. For Neon, use its pooled PostgreSQL connection string.
4. Set a long random application secret and restrict database access.

## Database note

The starter includes `database_schema.sql`, a normalized PostgreSQL/Neon schema with companies, branches, departments, roles, employees, users, chart of accounts, tax codes, journal batches and lines, customers, suppliers, products, recipes, warehouses, stock, sales, expenses, payroll, tax returns and an audit log. It includes foreign keys, uniqueness rules, accounting debit/credit checks and indexes.

The Streamlit prototype uses SQLite by default for local development. It accepts `DATABASE_URL` for a hosted database. Before production with Neon/PostgreSQL, migrate the schema to PostgreSQL and test all writes, especially generated IDs and upsert syntax. Do not use SQLite for multi-user production traffic.

## Included modules

- Login and role-based access: admin, manager, employee
- Admin account creation
- Restaurant profile and tax rate
- Point of sale and invoice download
- Menu items
- Expenses
- Inventory and low-stock alerts
- Customers and suppliers
- IFRS 18-oriented statement of profit or loss, statement of financial position, cash-flow statement, changes in equity and disclosure checklist
- CSV and PDF export for invoices, expenses, inventory, tax obligations and all primary financial statements
- Zimbabwe tax profile for ZIMRA, VAT, PAYE, withholding tax, IMTT, fiscalisation and NSSA POBS/APWCS
- Central audit-friendly records and created-by fields

## Production checklist

- Replace the default password.
- Use PostgreSQL/Neon, not SQLite.
- Add database migrations (Alembic), backups and monitoring.
- Configure local currency, tax, chart of accounts, liabilities, equity and statutory reporting.
- Add MFA/SSO, password reset and account lockout.
- Add payment gateway reconciliation and bank feeds.
- Have an accountant validate statutory statements before relying on them.
