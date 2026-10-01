"""
Database Manager and Schema Engine for Soulfyas Quality Restaurant ERP
Supports both PostgreSQL (Neon Cloud) and SQLite (Local / Dev) with unified API,
automatic migration, inventory stock deduction on sale, audit logging, multi-currency exchange rates,
dish modifiers, purchase orders, cashier shifts, and staff attendance.
"""

import os
import bcrypt
import pandas as pd
from datetime import date, datetime
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    try:
        import streamlit as st
        DATABASE_URL = st.secrets.get('DATABASE_URL')
    except Exception:
        DATABASE_URL = None

if not DATABASE_URL or DATABASE_URL.strip() == '':
    DATABASE_URL = 'sqlite:///restaurant.db'
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
IS_SQLITE = 'sqlite' in DATABASE_URL.lower()

def get_engine():
    return engine

def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_pw(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def run(sql: str, params: dict = None):
    with engine.begin() as conn:
        return conn.execute(text(sql), params or {})

def read(sql: str, params: dict = None) -> pd.DataFrame:
    with engine.begin() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})

def execute_insert(sql: str, params: dict = None) -> int:
    """Executes an INSERT statement and returns the newly generated primary key id."""
    with engine.begin() as conn:
        result = conn.execute(text(sql), params or {})
        try:
            inserted_id = result.scalar_one()
            return int(inserted_id)
        except Exception:
            if IS_SQLITE:
                last_id = conn.execute(text("SELECT last_insert_rowid()")).scalar_one()
                return int(last_id)
            return 0

def init_db():
    """Initializes all database tables with schema compatibility for SQLite and PostgreSQL"""
    pk_type = "INTEGER PRIMARY KEY AUTOINCREMENT" if IS_SQLITE else "BIGSERIAL PRIMARY KEY"
    timestamp_type = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP" if IS_SQLITE else "TIMESTAMPTZ DEFAULT now()"
    
    statements = [
        # Companies
        f"""
        CREATE TABLE IF NOT EXISTS companies (
            id {pk_type},
            name TEXT NOT NULL,
            trading_name TEXT,
            legal_name TEXT,
            address TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            website TEXT DEFAULT '',
            country TEXT DEFAULT 'Zimbabwe',
            timezone TEXT DEFAULT 'Africa/Harare',
            zimra_tin TEXT DEFAULT '',
            vat_number TEXT DEFAULT '',
            nssa_number TEXT DEFAULT '',
            currency TEXT DEFAULT 'USD',
            created_at {timestamp_type}
        );
        """,
        # Branches
        f"""
        CREATE TABLE IF NOT EXISTS branches (
            id {pk_type},
            company_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            address TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            is_main BOOLEAN DEFAULT TRUE,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Organisation Units
        f"""
        CREATE TABLE IF NOT EXISTS organisation_units (
            id {pk_type},
            company_id BIGINT NOT NULL,
            parent_id BIGINT,
            name TEXT NOT NULL,
            unit_type TEXT NOT NULL,
            description TEXT DEFAULT '',
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Positions
        f"""
        CREATE TABLE IF NOT EXISTS positions (
            id {pk_type},
            company_id BIGINT NOT NULL,
            unit_id BIGINT,
            title TEXT NOT NULL,
            reports_to_position_id BIGINT,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Employees
        f"""
        CREATE TABLE IF NOT EXISTS employees (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            unit_id BIGINT,
            employee_no TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            national_id TEXT DEFAULT '',
            nssa_number TEXT DEFAULT '',
            job_title TEXT DEFAULT '',
            salary NUMERIC(18,2) DEFAULT 0.0,
            allowances NUMERIC(18,2) DEFAULT 0.0,
            hire_date DATE,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Users & Authentication
        f"""
        CREATE TABLE IF NOT EXISTS users (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            active BOOLEAN DEFAULT TRUE,
            created_at {timestamp_type}
        );
        """,
        # Chart of Accounts
        f"""
        CREATE TABLE IF NOT EXISTS accounts (
            id {pk_type},
            company_id BIGINT NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            ifrs_category TEXT DEFAULT 'Operating',
            balance NUMERIC(18,2) DEFAULT 0.0,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Tax Codes
        f"""
        CREATE TABLE IF NOT EXISTS tax_codes (
            id {pk_type},
            company_id BIGINT NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            authority TEXT NOT NULL,
            rate NUMERIC(9,4) NOT NULL DEFAULT 0,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Multi-Currency Exchange Rates
        f"""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id {pk_type},
            company_id BIGINT NOT NULL,
            base_currency TEXT NOT NULL DEFAULT 'USD',
            target_currency TEXT NOT NULL,
            rate NUMERIC(18,6) NOT NULL,
            effective_date DATE NOT NULL,
            is_current BOOLEAN DEFAULT TRUE
        );
        """,
        # Restaurant Tables
        f"""
        CREATE TABLE IF NOT EXISTS tables (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            table_number TEXT NOT NULL,
            section TEXT NOT NULL DEFAULT 'Main Dining',
            capacity INTEGER DEFAULT 4,
            status TEXT DEFAULT 'Available'
        );
        """,
        # Menu Items
        f"""
        CREATE TABLE IF NOT EXISTS menu_items (
            id {pk_type},
            company_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT DEFAULT '',
            price NUMERIC(18,2) NOT NULL DEFAULT 0.0,
            cost NUMERIC(18,2) DEFAULT 0.0,
            is_vegetarian BOOLEAN DEFAULT FALSE,
            is_spicy BOOLEAN DEFAULT FALSE,
            prep_time_mins INTEGER DEFAULT 15,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Dish Modifiers & Add-ons
        f"""
        CREATE TABLE IF NOT EXISTS dish_modifiers (
            id {pk_type},
            company_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            additional_price NUMERIC(18,2) DEFAULT 0.0,
            cost NUMERIC(18,2) DEFAULT 0.0,
            inventory_item_id BIGINT,
            inventory_deduct_qty NUMERIC(18,4) DEFAULT 0.0,
            active BOOLEAN DEFAULT TRUE
        );
        """,
        # Customers & Suppliers
        f"""
        CREATE TABLE IF NOT EXISTS customers (
            id {pk_type},
            company_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            loyalty_points INTEGER DEFAULT 0,
            notes TEXT DEFAULT ''
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS suppliers (
            id {pk_type},
            company_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            contact_person TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            tax_id TEXT DEFAULT '',
            category TEXT DEFAULT 'General'
        );
        """,
        # Inventory
        f"""
        CREATE TABLE IF NOT EXISTS inventory (
            id {pk_type},
            company_id BIGINT NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL DEFAULT 'kg',
            quantity NUMERIC(18,4) DEFAULT 0.0,
            reorder_level NUMERIC(18,4) DEFAULT 0.0,
            unit_cost NUMERIC(18,2) DEFAULT 0.0,
            supplier_id BIGINT
        );
        """,
        # Recipes
        f"""
        CREATE TABLE IF NOT EXISTS recipes (
            id {pk_type},
            company_id BIGINT NOT NULL,
            menu_item_id BIGINT NOT NULL,
            yield_quantity NUMERIC(18,2) DEFAULT 1.0,
            instructions TEXT DEFAULT '',
            active BOOLEAN DEFAULT TRUE
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS recipe_lines (
            id {pk_type},
            recipe_id BIGINT NOT NULL,
            inventory_item_id BIGINT NOT NULL,
            quantity NUMERIC(18,4) NOT NULL,
            unit TEXT NOT NULL
        );
        """,
        # Sales & Orders
        f"""
        CREATE TABLE IF NOT EXISTS sales (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            invoice_no TEXT UNIQUE NOT NULL,
            sale_date DATE NOT NULL,
            customer_id BIGINT,
            table_id BIGINT,
            order_type TEXT DEFAULT 'Dine-In',
            payment_method TEXT DEFAULT 'Cash',
            subtotal NUMERIC(18,2) DEFAULT 0.0,
            discount NUMERIC(18,2) DEFAULT 0.0,
            tax NUMERIC(18,2) DEFAULT 0.0,
            tip NUMERIC(18,2) DEFAULT 0.0,
            total NUMERIC(18,2) DEFAULT 0.0,
            status TEXT DEFAULT 'Paid',
            kitchen_status TEXT DEFAULT 'Completed',
            created_by BIGINT,
            created_at {timestamp_type}
        );
        """,
        # Sale Lines
        f"""
        CREATE TABLE IF NOT EXISTS sale_lines (
            id {pk_type},
            sale_id BIGINT NOT NULL,
            item_id BIGINT NOT NULL,
            quantity NUMERIC(18,4) NOT NULL,
            unit_price NUMERIC(18,2) NOT NULL,
            line_total NUMERIC(18,2) NOT NULL,
            notes TEXT DEFAULT ''
        );
        """,
        # Kitchen Orders
        f"""
        CREATE TABLE IF NOT EXISTS kitchen_orders (
            id {pk_type},
            sale_id BIGINT NOT NULL,
            item_name TEXT NOT NULL,
            table_number TEXT DEFAULT 'Takeaway',
            quantity NUMERIC(18,2) NOT NULL,
            notes TEXT DEFAULT '',
            status TEXT DEFAULT 'Pending',
            created_at {timestamp_type}
        );
        """,
        # Cashier Shifts & Z-Reports
        f"""
        CREATE TABLE IF NOT EXISTS cashier_shifts (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            user_id BIGINT NOT NULL,
            shift_start {timestamp_type},
            shift_end {timestamp_type},
            opening_float NUMERIC(18,2) DEFAULT 0.0,
            cash_sales NUMERIC(18,2) DEFAULT 0.0,
            card_sales NUMERIC(18,2) DEFAULT 0.0,
            ecocash_sales NUMERIC(18,2) DEFAULT 0.0,
            bank_sales NUMERIC(18,2) DEFAULT 0.0,
            actual_cash_counted NUMERIC(18,2) DEFAULT 0.0,
            variance NUMERIC(18,2) DEFAULT 0.0,
            status TEXT DEFAULT 'open',
            notes TEXT DEFAULT ''
        );
        """,
        # Purchase Orders
        f"""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id {pk_type},
            company_id BIGINT NOT NULL,
            po_number TEXT UNIQUE NOT NULL,
            supplier_id BIGINT NOT NULL,
            order_date DATE NOT NULL,
            expected_delivery_date DATE,
            subtotal NUMERIC(18,2) DEFAULT 0.0,
            tax NUMERIC(18,2) DEFAULT 0.0,
            total NUMERIC(18,2) DEFAULT 0.0,
            status TEXT DEFAULT 'Draft',
            created_by BIGINT,
            created_at {timestamp_type}
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS purchase_order_lines (
            id {pk_type},
            po_id BIGINT NOT NULL,
            inventory_item_id BIGINT NOT NULL,
            quantity NUMERIC(18,4) NOT NULL,
            unit_cost NUMERIC(18,2) NOT NULL,
            line_total NUMERIC(18,2) NOT NULL
        );
        """,
        # Staff Attendance
        f"""
        CREATE TABLE IF NOT EXISTS staff_attendance (
            id {pk_type},
            company_id BIGINT NOT NULL,
            employee_id BIGINT NOT NULL,
            work_date DATE NOT NULL,
            clock_in TIME,
            clock_out TIME,
            hours_worked NUMERIC(6,2) DEFAULT 8.0,
            status TEXT DEFAULT 'Present'
        );
        """,
        # Stock Movements
        f"""
        CREATE TABLE IF NOT EXISTS stock_movements (
            id {pk_type},
            company_id BIGINT NOT NULL,
            inventory_item_id BIGINT NOT NULL,
            movement_type TEXT NOT NULL,
            quantity NUMERIC(18,4) NOT NULL,
            unit_cost NUMERIC(18,2) DEFAULT 0.0,
            reference TEXT DEFAULT '',
            reason TEXT DEFAULT '',
            created_by BIGINT,
            movement_date {timestamp_type}
        );
        """,
        # Expenses
        f"""
        CREATE TABLE IF NOT EXISTS expenses (
            id {pk_type},
            company_id BIGINT NOT NULL,
            branch_id BIGINT,
            expense_date DATE NOT NULL,
            category TEXT NOT NULL,
            description TEXT DEFAULT '',
            amount NUMERIC(18,2) NOT NULL,
            supplier TEXT DEFAULT '',
            supplier_id BIGINT,
            account_id BIGINT,
            payment_method TEXT DEFAULT 'Cash',
            tax_deductible BOOLEAN DEFAULT TRUE,
            receipt_no TEXT DEFAULT '',
            created_by BIGINT
        );
        """,
        # Journals & Lines
        f"""
        CREATE TABLE IF NOT EXISTS journals (
            id {pk_type},
            company_id BIGINT NOT NULL,
            entry_date DATE NOT NULL,
            reference TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'posted',
            created_by BIGINT,
            approved_by BIGINT,
            created_at {timestamp_type}
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS journal_lines (
            id {pk_type},
            journal_id BIGINT NOT NULL,
            account_id BIGINT NOT NULL,
            debit NUMERIC(18,2) DEFAULT 0.0,
            credit NUMERIC(18,2) DEFAULT 0.0
        );
        """,
        # Payroll
        f"""
        CREATE TABLE IF NOT EXISTS payroll_runs (
            id {pk_type},
            company_id BIGINT NOT NULL,
            period_month TEXT NOT NULL,
            period_year INTEGER NOT NULL,
            total_gross NUMERIC(18,2) DEFAULT 0.0,
            total_paye NUMERIC(18,2) DEFAULT 0.0,
            total_nssa NUMERIC(18,2) DEFAULT 0.0,
            total_net NUMERIC(18,2) DEFAULT 0.0,
            status TEXT DEFAULT 'Finalized',
            processed_by BIGINT,
            created_at {timestamp_type}
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS payroll_lines (
            id {pk_type},
            payroll_run_id BIGINT NOT NULL,
            employee_id BIGINT NOT NULL,
            basic_salary NUMERIC(18,2) DEFAULT 0.0,
            allowances NUMERIC(18,2) DEFAULT 0.0,
            gross_earnings NUMERIC(18,2) DEFAULT 0.0,
            nssa_employee NUMERIC(18,2) DEFAULT 0.0,
            nssa_employer NUMERIC(18,2) DEFAULT 0.0,
            nssa_apwcs NUMERIC(18,2) DEFAULT 0.0,
            paye_tax NUMERIC(18,2) DEFAULT 0.0,
            aids_levy NUMERIC(18,2) DEFAULT 0.0,
            other_deductions NUMERIC(18,2) DEFAULT 0.0,
            net_pay NUMERIC(18,2) DEFAULT 0.0
        );
        """,
        # Tax Returns
        f"""
        CREATE TABLE IF NOT EXISTS tax_returns (
            id {pk_type},
            company_id BIGINT NOT NULL,
            tax_type TEXT NOT NULL,
            period_name TEXT NOT NULL,
            gross_taxable NUMERIC(18,2) DEFAULT 0.0,
            tax_liability NUMERIC(18,2) DEFAULT 0.0,
            amount_paid NUMERIC(18,2) DEFAULT 0.0,
            status TEXT DEFAULT 'Submitted',
            due_date DATE,
            filed_at {timestamp_type}
        );
        """,
        # Audit Log
        f"""
        CREATE TABLE IF NOT EXISTS audit_log (
            id {pk_type},
            company_id BIGINT,
            user_id BIGINT,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            entity_id BIGINT,
            detail TEXT DEFAULT '',
            created_at {timestamp_type}
        );
        """
    ]
    
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
            
    seed_default_data()

def seed_default_data():
    """Seeds rich starter data for Soulfyas Quality Restaurant if database is empty"""
    with engine.begin() as conn:
        comp_count = conn.execute(text("SELECT COUNT(*) FROM companies")).scalar_one()
        if comp_count > 0:
            # Seed modifiers and exchange rates if not present
            try:
                mod_count = conn.execute(text("SELECT COUNT(*) FROM dish_modifiers")).scalar_one()
                if mod_count == 0:
                    seed_modifiers(conn, 1)
                rate_count = conn.execute(text("SELECT COUNT(*) FROM exchange_rates")).scalar_one()
                if rate_count == 0:
                    seed_rates(conn, 1)
            except Exception:
                pass
            return
            
        # 1. Company
        conn.execute(text("""
            INSERT INTO companies(name, trading_name, legal_name, address, phone, email, website, country, timezone, zimra_tin, vat_number, nssa_number, currency)
            VALUES('Soulfyas Quality Restaurant', 'Soulfyas Quality Restaurant', 'Soulfyas Investments (Pvt) Ltd',
                   '123 Samora Machel Avenue, Harare, Zimbabwe', '+263 242 700000', 'info@soulfyas.co.zw', 'https://soulfyas.co.zw',
                   'Zimbabwe', 'Africa/Harare', '200145892', '10045678', 'NSSA-789012', 'USD')
        """))
        if IS_SQLITE:
            cid = conn.execute(text("SELECT last_insert_rowid()")).scalar_one()
        else:
            cid = conn.execute(text("SELECT id FROM companies ORDER BY id DESC LIMIT 1")).scalar_one()
            
        # 2. Branches
        conn.execute(text("""
            INSERT INTO branches(company_id, name, code, address, phone, is_main, active)
            VALUES(:c, 'Harare Central Branch', 'HRE-01', '123 Samora Machel Ave, Harare', '+263 242 700000', 1, 1),
                  (:c, 'Bulawayo City Branch', 'BYO-01', '45 Jason Moyo St, Bulawayo', '+263 292 600000', 0, 1)
        """), {'c': cid})
        
        # 3. Directorates
        dirs = [
            ('Finance', 'Directorate', 'Financial management and statutory reporting'),
            ('Operations', 'Directorate', 'Restaurant operations, kitchen, and bar'),
            ('Commercial', 'Directorate', 'Sales, marketing, reservations, customer experience'),
            ('People', 'Directorate', 'Human resources, talent, and statutory payroll'),
            ('Technology', 'Directorate', 'POS systems, infrastructure, and IT support'),
            ('Governance & Risk', 'Directorate', 'Compliance, ZIMRA tax audit, and internal controls')
        ]
        for name, utype, desc in dirs:
            conn.execute(text("""
                INSERT INTO organisation_units(company_id, name, unit_type, description, active)
                VALUES(:c, :n, :t, :d, 1)
            """), {'c': cid, 'n': name, 't': utype, 'd': desc})
            
        # 4. Users
        pw_admin = hash_pw('ChangeMe123!')
        pw_user = hash_pw('Soulfyas2026!')
        
        users_data = [
            ('admin', 'System Administrator', pw_admin, 'admin'),
            ('manager', 'General Manager', pw_user, 'manager'),
            ('cashier', 'Head Cashier', pw_user, 'cashier'),
            ('chef', 'Executive Head Chef', pw_user, 'chef'),
            ('accountant', 'Financial Accountant', pw_user, 'accountant')
        ]
        for uname, fname, pwhash, role in users_data:
            conn.execute(text("""
                INSERT INTO users(company_id, username, full_name, password_hash, role, active)
                VALUES(:c, :u, :f, :p, :r, 1)
            """), {'c': cid, 'u': uname, 'f': fname, 'p': pwhash, 'r': role})
            
        # 5. Employees
        employees_data = [
            ('EMP-001', 'Tatenda Makuvaza', '63-123456-X-42', 'NSSA-9001', 'General Manager', 2500.0, 300.0, '2023-01-15'),
            ('EMP-002', 'Tendai Moyo', '63-234567-Y-18', 'NSSA-9002', 'Head Chef', 1400.0, 150.0, '2023-03-01'),
            ('EMP-003', 'Chipo Ndlovu', '08-345678-Z-29', 'NSSA-9003', 'Financial Accountant', 1600.0, 200.0, '2023-04-10'),
            ('EMP-004', 'Farai Mutasa', '63-456789-A-33', 'NSSA-9004', 'POS Cashier / Barista', 650.0, 50.0, '2023-06-01'),
            ('EMP-005', 'Tinashe Ncube', '29-567890-B-44', 'NSSA-9005', 'Senior Waiter / Server', 550.0, 50.0, '2023-08-15'),
            ('EMP-006', 'Rudo Sibanda', '08-678901-C-55', 'NSSA-9006', 'Sous Chef / Kitchen', 850.0, 80.0, '2024-01-10')
        ]
        for eno, fname, nid, nssa_no, jtitle, sal, allow, hdate in employees_data:
            conn.execute(text("""
                INSERT INTO employees(company_id, employee_no, full_name, national_id, nssa_number, job_title, salary, allowances, hire_date, active)
                VALUES(:c, :eno, :fn, :nid, :nssa, :jt, :sal, :al, :hd, 1)
            """), {'c': cid, 'eno': eno, 'fn': fname, 'nid': nid, 'nssa': nssa_no, 'jt': jtitle, 'sal': sal, 'al': allow, 'hd': hdate})
            
        # 6. Chart of Accounts
        accounts_data = [
            ('1000', 'Cash on Hand (POS Drawer)', 'asset', 'Operating'),
            ('1010', 'Petty Cash', 'asset', 'Operating'),
            ('1100', 'Stanbic Bank Operating USD', 'asset', 'Financing'),
            ('1110', 'Ecocash Merchant Wallet', 'asset', 'Operating'),
            ('1200', 'Raw Food & Beverage Inventory', 'asset', 'Operating'),
            ('1300', 'Trade Receivables & Customer Balances', 'asset', 'Operating'),
            ('1500', 'Kitchen & Restaurant Equipment', 'asset', 'Investing'),
            ('1550', 'Accumulated Depreciation - Equipment', 'asset', 'Investing'),
            ('2000', 'Trade Payables (Suppliers)', 'liability', 'Operating'),
            ('2100', 'ZIMRA VAT Output Payable', 'liability', 'Operating'),
            ('2110', 'ZIMRA VAT Input Receivable', 'asset', 'Operating'),
            ('2200', 'PAYE & AIDS Levy Payable', 'liability', 'Operating'),
            ('2210', 'NSSA POBS & APWCS Payable', 'liability', 'Operating'),
            ('2300', 'Accrued Operating Expenses', 'liability', 'Operating'),
            ('3000', 'Share Capital', 'equity', 'Financing'),
            ('3100', 'Retained Earnings', 'equity', 'Financing'),
            ('4000', 'Restaurant Food Sales', 'revenue', 'Operating'),
            ('4100', 'Bar & Beverage Sales', 'revenue', 'Operating'),
            ('4200', 'Catering & Event Revenue', 'revenue', 'Operating'),
            ('5000', 'Cost of Food & Ingredients (COGS)', 'expense', 'Operating'),
            ('5100', 'Cost of Beverages Sold', 'expense', 'Operating'),
            ('6000', 'Salaries, Wages & Benefits', 'expense', 'Operating'),
            ('6050', 'Employer NSSA & Statutory Levy', 'expense', 'Operating'),
            ('6100', 'Restaurant Rent & Rates', 'expense', 'Operating'),
            ('6200', 'Electricity, Gas & Water Utilities', 'expense', 'Operating'),
            ('6300', 'Kitchen Cleaning & Consumables', 'expense', 'Operating'),
            ('6400', 'POS & Software Subscriptions', 'expense', 'Operating'),
            ('6500', 'Repairs & Maintenance', 'expense', 'Operating'),
            ('6600', 'IMTT Bank Transfer Taxes', 'expense', 'Financing'),
            ('6700', 'Depreciation Expense', 'expense', 'Operating')
        ]
        for code, aname, atype, ifrs_cat in accounts_data:
            conn.execute(text("""
                INSERT INTO accounts(company_id, code, name, account_type, ifrs_category, balance, active)
                VALUES(:c, :co, :n, :t, :i, 0.0, 1)
            """), {'c': cid, 'co': code, 'n': aname, 't': atype, 'i': ifrs_cat})
            
        # 7. Tax Codes
        tax_codes = [
            ('VAT-15', 'ZIMRA Value Added Tax 15%', 'ZIMRA', 0.15),
            ('PAYE-STD', 'Statutory PAYE Brackets', 'ZIMRA', 0.25),
            ('NSSA-POBS', 'NSSA Pension Scheme 4.5%', 'NSSA', 0.045),
            ('NSSA-APWCS', 'Workers Compensation Scheme 1.4%', 'NSSA', 0.014),
            ('IMTT-2', 'Intermediated Money Transfer Tax 2%', 'ZIMRA', 0.02),
            ('WHT-5', 'Withholding Tax on Contracts 5%', 'ZIMRA', 0.05)
        ]
        for tcode, tname, tautho, trate in tax_codes:
            conn.execute(text("""
                INSERT INTO tax_codes(company_id, code, name, authority, rate, active)
                VALUES(:c, :tc, :tn, :ta, :tr, 1)
            """), {'c': cid, 'tc': tcode, 'tn': tname, 'ta': tautho, 'tr': trate})
            
        # 8. Tables
        tables_data = [
            ('T1', 'Main Dining', 4), ('T2', 'Main Dining', 4), ('T3', 'Main Dining', 6),
            ('T4', 'Main Dining', 2), ('T5', 'Main Dining', 8), ('P1', 'Garden / Patio', 4),
            ('P2', 'Garden / Patio', 4), ('P3', 'Garden / Patio', 6), ('VIP-1', 'VIP Lounge', 10),
            ('BAR-1', 'Bar Counter', 2), ('BAR-2', 'Bar Counter', 2)
        ]
        for tnum, sec, cap in tables_data:
            conn.execute(text("""
                INSERT INTO tables(company_id, table_number, section, capacity, status)
                VALUES(:c, :tn, :s, :cp, 'Available')
            """), {'c': cid, 'tn': tnum, 's': sec, 'cp': cap})
            
        # 9. Suppliers
        suppliers_data = [
            ('Irvines Zimbabwe', 'Kudzi B', '+263 242 612345', 'sales@irvines.co.zw', '10019922', 'Poultry & Meat'),
            ('Koala Butchery & Meats', 'John D', '+263 242 754321', 'orders@koala.co.zw', '10023456', 'Fresh Beef & Pork'),
            ('National Foods Zimbabwe', 'Grace M', '+263 242 753880', 'sales@natfoods.co.zw', '10034567', 'Grains, Mealies & Flour'),
            ('Delta Beverages', 'Tendai K', '+263 242 621100', 'orders@delta.co.zw', '10045678', 'Beverages & Soft Drinks'),
            ('Fresh Produce Wholesale Mbare', 'Sekuru Joe', '+263 772 345678', 'mbarefresh@gmail.com', '', 'Fresh Vegetables & Herbs')
        ]
        for sname, cper, sphone, semail, stax, scat in suppliers_data:
            conn.execute(text("""
                INSERT INTO suppliers(company_id, name, contact_person, phone, email, tax_id, category)
                VALUES(:c, :n, :cp, :p, :e, :t, :cat)
            """), {'c': cid, 'n': sname, 'cp': cper, 'p': sphone, 'e': semail, 't': stax, 'cat': scat})
            
        # 10. Customers
        customers_data = [
            ('Dr. Farai Shumba', '+263 773 111222', 'fshumba@gmail.com', 120, 'Prefers Patio T1'),
            ('Mrs. Tariro Chikwanha', '+263 772 998877', 'tariro.c@lawchambers.co.zw', 85, 'VIP regular'),
            ('Econet Corporate Account', '+263 242 486120', 'events@econet.co.zw', 450, 'Corporate client - invoiced monthly')
        ]
        for cname, cphone, cemail, cpts, cnotes in customers_data:
            conn.execute(text("""
                INSERT INTO customers(company_id, name, phone, email, loyalty_points, notes)
                VALUES(:c, :n, :p, :e, :pts, :nt)
            """), {'c': cid, 'n': cname, 'p': cphone, 'e': cemail, 'pts': cpts, 'nt': cnotes})
            
        # 11. Inventory
        inv_data = [
            ('Whole Chicken (Fresh)', 'Poultry', 'kg', 120.0, 25.0, 3.80, 1),
            ('Beef Rump & Chuck Steak', 'Meat', 'kg', 85.0, 20.0, 6.50, 2),
            ('Oxtail Cut', 'Meat', 'kg', 45.0, 15.0, 8.20, 2),
            ('Super Roller Meal (Sadza)', 'Grains', 'kg', 250.0, 50.0, 0.75, 3),
            ('Cooking Oil (Pure Vegetable)', 'Oils', 'litres', 90.0, 20.0, 1.90, 3),
            ('Fresh Tomatoes', 'Vegetables', 'kg', 60.0, 15.0, 1.20, 5),
            ('Onions', 'Vegetables', 'kg', 50.0, 15.0, 0.90, 5),
            ('Potatoes (Irish)', 'Vegetables', 'kg', 140.0, 30.0, 0.85, 5),
            ('Peri-Peri Spices & Marinade', 'Spices', 'kg', 25.0, 5.0, 4.50, 3),
            ('Zambezi Lager Cans (330ml)', 'Beverages', 'cans', 180.0, 48.0, 1.10, 4),
            ('Mazoe Orange Crush (2L)', 'Beverages', 'bottles', 40.0, 12.0, 3.20, 4),
            ('Burger Buns (Fresh Gourmet)', 'Bakery', 'packs', 75.0, 20.0, 1.20, 3),
            ('Cheddar Cheese Slices', 'Dairy', 'kg', 20.0, 5.0, 5.50, 3)
        ]
        for iname, icat, iunit, iqty, ireorder, icost, isup in inv_data:
            conn.execute(text("""
                INSERT INTO inventory(company_id, item_name, category, unit, quantity, reorder_level, unit_cost, supplier_id)
                VALUES(:c, :n, :cat, :u, :q, :r, :co, :s)
            """), {'c': cid, 'n': iname, 'cat': icat, 'u': iunit, 'q': iqty, 'r': ireorder, 'co': icost, 's': isup})
            
        # 12. Menu Items
        menu_data = [
            ('Full Flame-Grilled Peri-Peri Chicken', 'Mains', 'Signature tender flame-grilled chicken basted with authentic peri-peri sauce', 18.00, 5.50, 0, 1, 25),
            ('Half Peri-Peri Chicken & Chips', 'Mains', 'Half flame-grilled chicken served with golden crispy potato chips', 11.00, 3.20, 0, 1, 20),
            ('Sadza with Beef Stew & Covo Greens', 'Traditional', 'Authentic Zimbabwean Sadza served with slow-cooked beef stew and braised covo greens', 8.50, 2.60, 0, 0, 15),
            ('Soulfyas Special Braised Oxtail', 'Traditional', 'Rich, melt-in-mouth braised oxtail in savory gravy with sadza or rice', 16.00, 5.10, 0, 0, 25),
            ('Soulfyas Gourmet Beef Burger', 'Burgers', 'Charbroiled pure beef patty with melted cheddar, crisp lettuce, tomato and signature sauce', 10.00, 3.10, 0, 0, 15),
            ('Crispy Golden Potato Chips (Large)', 'Sides', 'Hand-cut crispy seasoned potato chips', 3.50, 0.80, 1, 0, 10),
            ('Traditional Sadza Portion', 'Sides', 'Freshly prepared Zimbabwean cornmeal staple', 2.00, 0.35, 1, 0, 10),
            ('Zambezi Lager (Cold Can 330ml)', 'Beverages', 'Zimbabwean iconic lager, ice cold', 2.50, 1.10, 1, 0, 2),
            ('Mazoe Orange Glass', 'Beverages', 'Chilled refreshing classic Mazoe Orange Crush', 2.00, 0.40, 1, 0, 2),
            ('Mineral Water (500ml)', 'Beverages', 'Still natural mineral water', 1.00, 0.30, 1, 0, 2)
        ]
        for mname, mcat, mdesc, mprice, mcost, is_veg, is_spicy, ptime in menu_data:
            conn.execute(text("""
                INSERT INTO menu_items(company_id, name, category, description, price, cost, is_vegetarian, is_spicy, prep_time_mins, active)
                VALUES(:c, :n, :cat, :d, :p, :co, :v, :s, :pt, 1)
            """), {'c': cid, 'n': mname, 'cat': mcat, 'd': mdesc, 'p': mprice, 'co': mcost, 'v': is_veg, 's': is_spicy, 'pt': ptime})
            
        # 13. Recipes
        recipes = [
            (1, [(1, 1.2, 'kg'), (9, 0.08, 'kg'), (5, 0.05, 'litres')]),
            (2, [(1, 0.6, 'kg'), (8, 0.3, 'kg'), (9, 0.04, 'kg'), (5, 0.1, 'litres')]),
            (3, [(2, 0.35, 'kg'), (4, 0.25, 'kg'), (6, 0.1, 'kg'), (7, 0.05, 'kg')]),
            (4, [(3, 0.5, 'kg'), (4, 0.25, 'kg'), (6, 0.1, 'kg'), (7, 0.05, 'kg')]),
            (5, [(12, 1.0, 'packs'), (2, 0.25, 'kg'), (13, 0.05, 'kg'), (8, 0.2, 'kg')]),
            (6, [(8, 0.4, 'kg'), (5, 0.08, 'litres')]),
            (7, [(4, 0.3, 'kg')]),
            (8, [(10, 1.0, 'cans')]),
            (9, [(11, 0.1, 'bottles')])
        ]
        for m_id, lines in recipes:
            conn.execute(text("""
                INSERT INTO recipes(company_id, menu_item_id, yield_quantity, instructions, active)
                VALUES(:c, :mi, 1.0, 'Standard restaurant formulation', 1)
            """), {'c': cid, 'mi': m_id})
            if IS_SQLITE:
                rec_id = conn.execute(text("SELECT last_insert_rowid()")).scalar_one()
            else:
                rec_id = conn.execute(text("SELECT id FROM recipes ORDER BY id DESC LIMIT 1")).scalar_one()
                
            for inv_id, qty_used, u in lines:
                conn.execute(text("""
                    INSERT INTO recipe_lines(recipe_id, inventory_item_id, quantity, unit)
                    VALUES(:r, :inv, :q, :u)
                """), {'r': rec_id, 'inv': inv_id, 'q': qty_used, 'u': u})
                
        # 14. Seed Modifiers & Rates
        seed_modifiers(conn, cid)
        seed_rates(conn, cid)
        
        # 15. Initial Open Cashier Shift
        conn.execute(text("""
            INSERT INTO cashier_shifts(company_id, branch_id, user_id, shift_start, opening_float, cash_sales, card_sales, ecocash_sales, bank_sales, status)
            VALUES(:c, 1, 3, :start_time, 100.0, 45.0, 27.0, 0.0, 0.0, 'open')
        """), {'c': cid, 'start_time': datetime.now()})
        
        # 16. Audit Log Initial Entry
        conn.execute(text("""
            INSERT INTO audit_log(company_id, user_id, action, entity, entity_id, detail)
            VALUES(:c, 1, 'SYSTEM_INIT', 'System', 1, 'Initialized Soulfyas Quality Restaurant ERP normalized database with multi-currency & modifiers.')
        """), {'c': cid})

def seed_modifiers(conn, cid):
    """Seeds dish modifiers for customizations, basting, and add-on sides"""
    modifiers = [
        # Side Choices
        ('Traditional Sadza Portion', 'Side Choice', 0.00, 0.35, 4, 0.3),
        ('Crispy Potato Chips', 'Side Choice', 1.00, 0.60, 8, 0.3),
        ('Savory Yellow Rice', 'Side Choice', 0.00, 0.40, None, 0.0),
        ('Fresh Garden Salad', 'Side Choice', 0.50, 0.45, 6, 0.15),
        # Basting / Heat Levels
        ('Mild Lemon & Herb Basting', 'Basting & Heat', 0.00, 0.10, None, 0.0),
        ('Medium Peri-Peri Sauce', 'Basting & Heat', 0.00, 0.15, 9, 0.03),
        ('Extra Hot Flame Peri-Peri', 'Basting & Heat', 0.00, 0.20, 9, 0.05),
        ('Smokey BBQ Glaze', 'Basting & Heat', 0.00, 0.15, None, 0.0),
        # Add-on Toppings
        ('Melted Cheddar Cheese Slice', 'Add-on Topping', 1.50, 0.40, 13, 0.05),
        ('Fried Free-Range Egg', 'Add-on Topping', 1.00, 0.30, None, 0.0),
        ('Creamy Garlic Mushroom Sauce', 'Add-on Topping', 2.50, 0.70, None, 0.0),
        ('Grilled Beef Bacon Rashers', 'Add-on Topping', 2.00, 0.80, 2, 0.1)
    ]
    for name, grp, add_p, cost, inv_id, inv_qty in modifiers:
        conn.execute(text("""
            INSERT INTO dish_modifiers(company_id, name, group_name, additional_price, cost, inventory_item_id, inventory_deduct_qty, active)
            VALUES(:c, :n, :g, :p, :co, :iid, :iq, 1)
        """), {'c': cid, 'n': name, 'g': grp, 'p': add_p, 'co': cost, 'iid': inv_id, 'iq': inv_qty})

def seed_rates(conn, cid):
    """Seeds official foreign exchange and RBZ ZiG rates"""
    today_d = str(date.today())
    rates = [
        ('USD', 'ZiG', 28.50),
        ('USD', 'ZAR', 18.20),
        ('USD', 'EUR', 0.92),
        ('USD', 'GBP', 0.78)
    ]
    for base, tgt, r in rates:
        conn.execute(text("""
            INSERT INTO exchange_rates(company_id, base_currency, target_currency, rate, effective_date, is_current)
            VALUES(:c, :b, :t, :r, :d, 1)
        """), {'c': cid, 'b': base, 't': tgt, 'r': r, 'd': today_d})

def get_current_rate(company_id: int, target_currency: str = 'ZiG') -> float:
    """Retrieves current active exchange rate for a target currency against USD"""
    res = read("""
        SELECT rate FROM exchange_rates
        WHERE company_id = :c AND target_currency = :t AND is_current = 1
        ORDER BY id DESC LIMIT 1
    """, {'c': company_id, 't': target_currency})
    if len(res):
        return float(res.iloc[0]['rate'])
    return 28.50 if target_currency == 'ZiG' else 1.0

def deduct_inventory_for_sale(company_id: int, sale_id: int, user_id: int = 1):
    """
    Automatically tracks and deducts recipe ingredients from stock balances when a POS sale occurs.
    """
    try:
        sale_lines = read("""
            SELECT sl.item_id, sl.quantity, mi.name AS item_name
            FROM sale_lines sl
            JOIN menu_items mi ON mi.id = sl.item_id
            WHERE sl.sale_id = :sid
        """, {'sid': sale_id})
        
        sale_info = read("SELECT invoice_no FROM sales WHERE id = :sid", {'sid': sale_id})
        inv_no = sale_info.iloc[0]['invoice_no'] if len(sale_info) else f"Sale #{sale_id}"
        
        for _, sline in sale_lines.iterrows():
            item_id = int(sline['item_id'])
            order_qty = float(sline['quantity'])
            
            # Find recipe for this menu item
            rec = read("SELECT id, yield_quantity FROM recipes WHERE menu_item_id = :mi AND company_id = :c AND active = 1 LIMIT 1", {'mi': item_id, 'c': company_id})
            if len(rec):
                rec_id = int(rec.iloc[0]['id'])
                yield_qty = float(rec.iloc[0]['yield_quantity']) or 1.0
                rlines = read("SELECT inventory_item_id, quantity, unit FROM recipe_lines WHERE recipe_id = :rid", {'rid': rec_id})
                
                for _, rline in rlines.iterrows():
                    inv_id = int(rline['inventory_item_id'])
                    qty_per_portion = float(rline['quantity'])
                    total_to_deduct = (qty_per_portion / yield_qty) * order_qty
                    
                    # Deduct from inventory
                    run("""
                        UPDATE inventory
                        SET quantity = MAX(0.0, quantity - :deduct_qty)
                        WHERE id = :inv_id AND company_id = :c
                    """, {'deduct_qty': total_to_deduct, 'inv_id': inv_id, 'c': company_id})
                    
                    # Log stock movement
                    run("""
                        INSERT INTO stock_movements(company_id, inventory_item_id, movement_type, quantity, reference, reason, created_by)
                        VALUES(:c, :inv_id, 'Sale Consumption', :qty, :ref, :reason, :u)
                    """, {
                        'c': company_id,
                        'inv_id': inv_id,
                        'qty': -total_to_deduct,
                        'ref': inv_no,
                        'reason': f"Deducted for {order_qty:g}x {sline['item_name']}",
                        'u': user_id
                    })
    except Exception as e:
        print(f"Stock deduction warning: {e}")

def log_audit(company_id: int, user_id: int, action: str, entity: str, entity_id: int, detail: str):
    """Records an immutable audit trail event"""
    try:
        run("""
            INSERT INTO audit_log(company_id, user_id, action, entity, entity_id, detail)
            VALUES(:c, :u, :a, :e, :eid, :d)
        """, {
            'c': company_id,
            'u': user_id,
            'a': action,
            'e': entity,
            'eid': entity_id,
            'd': detail
        })
    except Exception as e:
        print(f"Audit log error: {e}")
