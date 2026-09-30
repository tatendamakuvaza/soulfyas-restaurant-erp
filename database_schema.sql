-- Soulfyas Quality Restaurant ERP - normalized PostgreSQL/Neon foundation
-- Run through a migration tool in production; do not edit posted transactions in place.

CREATE TABLE companies (
  id BIGSERIAL PRIMARY KEY, legal_name VARCHAR(200) NOT NULL, trading_name VARCHAR(200) NOT NULL,
  tax_id VARCHAR(80), vat_number VARCHAR(80), nssa_number VARCHAR(80), functional_currency CHAR(3) NOT NULL DEFAULT 'USD',
  address TEXT, phone VARCHAR(50), email VARCHAR(200), created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE branches (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), name VARCHAR(150) NOT NULL,
  address TEXT, active BOOLEAN NOT NULL DEFAULT true
);
CREATE TABLE departments (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), name VARCHAR(150) NOT NULL, active BOOLEAN NOT NULL DEFAULT true,
  UNIQUE(company_id,name)
);
CREATE TABLE roles (id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), name VARCHAR(80) NOT NULL, is_top_management BOOLEAN NOT NULL DEFAULT false);
CREATE TABLE employees (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), branch_id BIGINT REFERENCES branches(id), department_id BIGINT REFERENCES departments(id),
  employee_no VARCHAR(50), full_name VARCHAR(200) NOT NULL, national_id VARCHAR(80), nssa_number VARCHAR(80), job_title VARCHAR(150),
  employment_date DATE, termination_date DATE, salary NUMERIC(18,2), active BOOLEAN NOT NULL DEFAULT true
);
CREATE TABLE app_users (
  id BIGSERIAL PRIMARY KEY, employee_id BIGINT REFERENCES employees(id), username VARCHAR(100) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, role_id BIGINT REFERENCES roles(id), active BOOLEAN NOT NULL DEFAULT true, last_login TIMESTAMPTZ
);
CREATE TABLE accounts (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), code VARCHAR(30) NOT NULL, name VARCHAR(200) NOT NULL,
  account_type VARCHAR(30) NOT NULL CHECK(account_type IN ('asset','liability','equity','revenue','expense')), ifrs_category VARCHAR(30),
  parent_id BIGINT REFERENCES accounts(id), active BOOLEAN NOT NULL DEFAULT true, UNIQUE(company_id,code)
);
CREATE TABLE tax_codes (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), code VARCHAR(50) NOT NULL, name VARCHAR(150) NOT NULL,
  authority VARCHAR(50) NOT NULL, rate NUMERIC(9,4) NOT NULL DEFAULT 0, effective_from DATE NOT NULL, effective_to DATE, active BOOLEAN DEFAULT true
);
CREATE TABLE journal_batches (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), branch_id BIGINT REFERENCES branches(id), batch_no VARCHAR(60) UNIQUE NOT NULL,
  entry_date DATE NOT NULL, source VARCHAR(40) NOT NULL, description TEXT, status VARCHAR(20) NOT NULL DEFAULT 'draft',
  created_by BIGINT REFERENCES app_users(id), approved_by BIGINT REFERENCES app_users(id), posted_at TIMESTAMPTZ
);
CREATE TABLE journal_lines (
  id BIGSERIAL PRIMARY KEY, batch_id BIGINT NOT NULL REFERENCES journal_batches(id), account_id BIGINT NOT NULL REFERENCES accounts(id),
  department_id BIGINT REFERENCES departments(id), tax_code_id BIGINT REFERENCES tax_codes(id), description TEXT,
  debit NUMERIC(18,2) NOT NULL DEFAULT 0 CHECK(debit >= 0), credit NUMERIC(18,2) NOT NULL DEFAULT 0 CHECK(credit >= 0),
  CHECK(NOT(debit > 0 AND credit > 0)), CHECK(debit > 0 OR credit > 0)
);
CREATE TABLE customers (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), name VARCHAR(200) NOT NULL, phone VARCHAR(50), email VARCHAR(200));
CREATE TABLE suppliers (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), name VARCHAR(200) NOT NULL, phone VARCHAR(50), email VARCHAR(200), tax_id VARCHAR(80));
CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), sku VARCHAR(80), name VARCHAR(200) NOT NULL, category VARCHAR(100),
  item_type VARCHAR(30) NOT NULL DEFAULT 'menu_item', selling_price NUMERIC(18,2) NOT NULL DEFAULT 0, standard_cost NUMERIC(18,2) NOT NULL DEFAULT 0,
  active BOOLEAN NOT NULL DEFAULT true
);
CREATE TABLE recipes (id BIGSERIAL PRIMARY KEY, product_id BIGINT NOT NULL REFERENCES products(id), version INTEGER NOT NULL DEFAULT 1, active BOOLEAN DEFAULT true);
CREATE TABLE recipe_lines (id BIGSERIAL PRIMARY KEY, recipe_id BIGINT NOT NULL REFERENCES recipes(id), ingredient_product_id BIGINT NOT NULL REFERENCES products(id), quantity NUMERIC(18,4) NOT NULL);
CREATE TABLE warehouses (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), branch_id BIGINT REFERENCES branches(id), name VARCHAR(150) NOT NULL);
CREATE TABLE stock_balances (id BIGSERIAL PRIMARY KEY, warehouse_id BIGINT NOT NULL REFERENCES warehouses(id), product_id BIGINT NOT NULL REFERENCES products(id), quantity NUMERIC(18,4) NOT NULL DEFAULT 0, reorder_level NUMERIC(18,4) DEFAULT 0, UNIQUE(warehouse_id,product_id));
CREATE TABLE stock_movements (id BIGSERIAL PRIMARY KEY, warehouse_id BIGINT NOT NULL REFERENCES warehouses(id), product_id BIGINT NOT NULL REFERENCES products(id), movement_type VARCHAR(30) NOT NULL, quantity NUMERIC(18,4) NOT NULL, unit_cost NUMERIC(18,4) DEFAULT 0, source VARCHAR(60), movement_date TIMESTAMPTZ DEFAULT now(), created_by BIGINT REFERENCES app_users(id));
CREATE TABLE sales (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), branch_id BIGINT REFERENCES branches(id), invoice_no VARCHAR(80) UNIQUE NOT NULL, customer_id BIGINT REFERENCES customers(id), sale_date TIMESTAMPTZ NOT NULL DEFAULT now(), subtotal NUMERIC(18,2), tax NUMERIC(18,2), total NUMERIC(18,2), payment_method VARCHAR(40), status VARCHAR(30), created_by BIGINT REFERENCES app_users(id));
CREATE TABLE sale_lines (id BIGSERIAL PRIMARY KEY, sale_id BIGINT NOT NULL REFERENCES sales(id), product_id BIGINT NOT NULL REFERENCES products(id), quantity NUMERIC(18,4) NOT NULL, unit_price NUMERIC(18,2) NOT NULL, tax_code_id BIGINT REFERENCES tax_codes(id), line_total NUMERIC(18,2) NOT NULL);
CREATE TABLE expenses (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), branch_id BIGINT REFERENCES branches(id), expense_date DATE NOT NULL, supplier_id BIGINT REFERENCES suppliers(id), account_id BIGINT REFERENCES accounts(id), description TEXT, amount NUMERIC(18,2) NOT NULL, tax_code_id BIGINT REFERENCES tax_codes(id), created_by BIGINT REFERENCES app_users(id));
CREATE TABLE payroll_runs (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), period_start DATE NOT NULL, period_end DATE NOT NULL, status VARCHAR(20) DEFAULT 'draft', approved_by BIGINT REFERENCES app_users(id));
CREATE TABLE payroll_lines (id BIGSERIAL PRIMARY KEY, payroll_run_id BIGINT NOT NULL REFERENCES payroll_runs(id), employee_id BIGINT NOT NULL REFERENCES employees(id), gross_pay NUMERIC(18,2), paye NUMERIC(18,2), nssa_employee NUMERIC(18,2), nssa_employer NUMERIC(18,2), other_deductions NUMERIC(18,2), net_pay NUMERIC(18,2));
CREATE TABLE tax_returns (id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), tax_code_id BIGINT NOT NULL REFERENCES tax_codes(id), period_start DATE NOT NULL, period_end DATE NOT NULL, liability NUMERIC(18,2), paid NUMERIC(18,2), filing_status VARCHAR(30) DEFAULT 'draft', due_date DATE);
CREATE TABLE audit_log (id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), user_id BIGINT REFERENCES app_users(id), action VARCHAR(50) NOT NULL, table_name VARCHAR(100), record_id BIGINT, before_json JSONB, after_json JSONB, created_at TIMESTAMPTZ DEFAULT now());
CREATE INDEX idx_journal_lines_account ON journal_lines(account_id);
CREATE INDEX idx_journal_batches_date ON journal_batches(entry_date);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_stock_product ON stock_balances(product_id);
CREATE INDEX idx_audit_record ON audit_log(table_name,record_id);
