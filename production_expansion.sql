-- Soulfyas ERP production expansion migration for Neon PostgreSQL
-- Run only after backing up the database. Uses IF NOT EXISTS and preserves data.

ALTER TABLE companies ADD COLUMN IF NOT EXISTS legal_name TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS trading_name TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS email TEXT DEFAULT '';
ALTER TABLE companies ADD COLUMN IF NOT EXISTS website TEXT DEFAULT '';
ALTER TABLE companies ADD COLUMN IF NOT EXISTS country TEXT DEFAULT 'Zimbabwe';
ALTER TABLE companies ADD COLUMN IF NOT EXISTS timezone TEXT DEFAULT 'Africa/Harare';
ALTER TABLE companies ADD COLUMN IF NOT EXISTS financial_year_end DATE;

CREATE TABLE IF NOT EXISTS organisation_units (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), parent_id BIGINT REFERENCES organisation_units(id),
 name TEXT NOT NULL, unit_type TEXT NOT NULL, description TEXT DEFAULT '', active BOOLEAN DEFAULT TRUE,
 UNIQUE(company_id,parent_id,name)
);
CREATE TABLE IF NOT EXISTS positions (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), unit_id BIGINT REFERENCES organisation_units(id),
 title TEXT NOT NULL, reports_to_position_id BIGINT REFERENCES positions(id), active BOOLEAN DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS department_activities (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), unit_id BIGINT NOT NULL REFERENCES organisation_units(id),
 activity_code TEXT NOT NULL, name TEXT NOT NULL, description TEXT DEFAULT '', process_owner TEXT, active BOOLEAN DEFAULT TRUE,
 UNIQUE(company_id,activity_code)
);
CREATE TABLE IF NOT EXISTS company_contacts (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), contact_type TEXT NOT NULL,
 name TEXT, email TEXT, phone TEXT, department TEXT, is_primary BOOLEAN DEFAULT FALSE, active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS accounting_periods (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), period_start DATE NOT NULL, period_end DATE NOT NULL,
 status TEXT NOT NULL DEFAULT 'open', closed_by BIGINT REFERENCES users(id), closed_at TIMESTAMPTZ,
 UNIQUE(company_id,period_start,period_end)
);
CREATE TABLE IF NOT EXISTS journal_batches (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), period_id BIGINT REFERENCES accounting_periods(id),
 batch_no TEXT UNIQUE NOT NULL, entry_date DATE NOT NULL, source TEXT NOT NULL, description TEXT DEFAULT '', status TEXT DEFAULT 'draft',
 created_by BIGINT REFERENCES users(id), approved_by BIGINT REFERENCES users(id), posted_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS journal_batch_lines (
 id BIGSERIAL PRIMARY KEY, batch_id BIGINT NOT NULL REFERENCES journal_batches(id), account_code TEXT NOT NULL,
 account_name TEXT NOT NULL, department TEXT, description TEXT DEFAULT '', debit NUMERIC(18,2) DEFAULT 0, credit NUMERIC(18,2) DEFAULT 0,
 CHECK((debit=0 AND credit>0) OR (credit=0 AND debit>0))
);
CREATE TABLE IF NOT EXISTS statement_definitions (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), statement_type TEXT NOT NULL,
 line_code TEXT NOT NULL, label TEXT NOT NULL, category TEXT, display_order INTEGER DEFAULT 0, active BOOLEAN DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS statement_line_mappings (
 id BIGSERIAL PRIMARY KEY, statement_definition_id BIGINT NOT NULL REFERENCES statement_definitions(id), account_code TEXT NOT NULL,
 sign_multiplier NUMERIC(8,2) DEFAULT 1
);
CREATE TABLE IF NOT EXISTS comparative_periods (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), current_start DATE NOT NULL, current_end DATE NOT NULL,
 comparative_start DATE NOT NULL, comparative_end DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS accounting_policies (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), policy_name TEXT NOT NULL,
 policy_text TEXT NOT NULL, effective_from DATE NOT NULL, effective_to DATE, approved_by BIGINT REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS management_performance_measures (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), name TEXT NOT NULL,
 definition TEXT NOT NULL, calculation TEXT NOT NULL, period_start DATE NOT NULL, period_end DATE NOT NULL,
 amount NUMERIC(18,2), ifrs_reconciliation TEXT, approved_by BIGINT REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS financial_statement_runs (
 id BIGSERIAL PRIMARY KEY, company_id BIGINT NOT NULL REFERENCES companies(id), period_start DATE NOT NULL, period_end DATE NOT NULL,
 status TEXT DEFAULT 'draft', generated_by BIGINT REFERENCES users(id), generated_at TIMESTAMPTZ DEFAULT now(), trial_balance_debits NUMERIC(18,2), trial_balance_credits NUMERIC(18,2), balanced BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS financial_statement_notes (
 id BIGSERIAL PRIMARY KEY, run_id BIGINT NOT NULL REFERENCES financial_statement_runs(id), note_number TEXT NOT NULL,
 title TEXT NOT NULL, content TEXT NOT NULL
);

-- Seed the organisation chart for the first company.
DO $$
DECLARE c BIGINT; finance BIGINT; operations BIGINT; commercial BIGINT; people BIGINT; technology BIGINT; governance BIGINT;
BEGIN
 SELECT id INTO c FROM companies ORDER BY id LIMIT 1;
 IF c IS NULL THEN RETURN; END IF;
 INSERT INTO organisation_units(company_id,name,unit_type,description) VALUES
 (c,'Finance','Directorate','Financial management and reporting'),(c,'Operations','Directorate','Restaurant and service delivery'),(c,'Commercial','Directorate','Sales, marketing and customers'),(c,'People','Directorate','Human resources and payroll'),(c,'Technology','Directorate','IT, applications and data'),(c,'Governance & Risk','Directorate','Legal, risk, compliance and audit') ON CONFLICT DO NOTHING;
 SELECT id INTO finance FROM organisation_units WHERE company_id=c AND name='Finance';
 SELECT id INTO operations FROM organisation_units WHERE company_id=c AND name='Operations';
 SELECT id INTO commercial FROM organisation_units WHERE company_id=c AND name='Commercial';
 SELECT id INTO people FROM organisation_units WHERE company_id=c AND name='People';
 SELECT id INTO technology FROM organisation_units WHERE company_id=c AND name='Technology';
 SELECT id INTO governance FROM organisation_units WHERE company_id=c AND name='Governance & Risk';
 INSERT INTO organisation_units(company_id,parent_id,name,unit_type) VALUES
 (c,finance,'General Ledger','Department'),(c,finance,'Accounts Payable','Department'),(c,finance,'Accounts Receivable','Department'),(c,finance,'Treasury','Department'),(c,finance,'Budgeting & Planning','Department'),(c,finance,'Tax','Department'),(c,finance,'Fixed Assets','Department'),(c,finance,'Management Reporting','Department'),
 (c,operations,'Procurement','Department'),(c,operations,'Inventory','Department'),(c,operations,'Warehousing','Department'),(c,operations,'Logistics','Department'),(c,operations,'Service Delivery','Department'),(c,operations,'Quality','Department'),(c,operations,'Maintenance','Department'),
 (c,commercial,'Sales','Department'),(c,commercial,'Marketing','Department'),(c,commercial,'CRM','Department'),(c,commercial,'Customer Service','Department'),
 (c,people,'Recruitment','Department'),(c,people,'Payroll','Department'),(c,people,'Learning & Development','Department'),(c,people,'Performance Management','Department'),
 (c,technology,'IT Infrastructure','Department'),(c,technology,'Applications','Department'),(c,technology,'Cybersecurity','Department'),(c,technology,'Data & Analytics','Department'),
 (c,governance,'Legal','Department'),(c,governance,'Compliance','Department'),(c,governance,'Internal Audit','Department'),(c,governance,'Risk Management','Department') ON CONFLICT DO NOTHING;
END $$;

CREATE INDEX IF NOT EXISTS idx_org_company ON organisation_units(company_id);
CREATE INDEX IF NOT EXISTS idx_activity_unit ON department_activities(unit_id);
CREATE INDEX IF NOT EXISTS idx_journal_period ON journal_batches(period_id);
CREATE INDEX IF NOT EXISTS idx_statement_run ON financial_statement_runs(company_id,period_end);
