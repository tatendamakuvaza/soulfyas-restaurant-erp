import os, io, html, secrets
from datetime import date, datetime
import bcrypt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title='Soulfyas Quality Restaurant ERP', page_icon='🍽️', layout='wide')
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    try:
        DATABASE_URL = st.secrets['DATABASE_URL']
    except Exception:
        DATABASE_URL = None
if not DATABASE_URL:
    st.error('DATABASE_URL is not configured. Add it in Streamlit Cloud Secrets.'); st.stop()
if DATABASE_URL.startswith('postgresql://'): DATABASE_URL=DATABASE_URL.replace('postgresql://','postgresql+psycopg://',1)
engine=create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
LOGO='soulfyas_logo.png'

SCHEMA='''
CREATE TABLE IF NOT EXISTS companies(id BIGSERIAL PRIMARY KEY, name TEXT NOT NULL, address TEXT DEFAULT '', phone TEXT DEFAULT '', zimra_tin TEXT DEFAULT '', vat_number TEXT DEFAULT '', nssa_number TEXT DEFAULT '', currency TEXT DEFAULT 'USD', created_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS users(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), username TEXT UNIQUE NOT NULL, full_name TEXT NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'employee', active BOOLEAN DEFAULT TRUE, created_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS accounts(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), code TEXT NOT NULL, name TEXT NOT NULL, account_type TEXT NOT NULL, UNIQUE(company_id,code));
CREATE TABLE IF NOT EXISTS menu_items(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), name TEXT NOT NULL, category TEXT, price NUMERIC(18,2) NOT NULL DEFAULT 0, cost NUMERIC(18,2) DEFAULT 0, active BOOLEAN DEFAULT TRUE);
CREATE TABLE IF NOT EXISTS customers(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), name TEXT NOT NULL, phone TEXT, email TEXT);
CREATE TABLE IF NOT EXISTS suppliers(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), name TEXT NOT NULL, phone TEXT, email TEXT);
CREATE TABLE IF NOT EXISTS inventory(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), item_name TEXT NOT NULL, category TEXT, unit TEXT, quantity NUMERIC(18,4) DEFAULT 0, reorder_level NUMERIC(18,4) DEFAULT 0, unit_cost NUMERIC(18,2) DEFAULT 0);
CREATE TABLE IF NOT EXISTS sales(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), invoice_no TEXT UNIQUE NOT NULL, sale_date DATE NOT NULL, customer_id BIGINT REFERENCES customers(id), payment_method TEXT, subtotal NUMERIC(18,2), tax NUMERIC(18,2), total NUMERIC(18,2), status TEXT DEFAULT 'Paid', created_by BIGINT REFERENCES users(id));
CREATE TABLE IF NOT EXISTS sale_lines(id BIGSERIAL PRIMARY KEY, sale_id BIGINT REFERENCES sales(id), item_id BIGINT REFERENCES menu_items(id), quantity NUMERIC(18,4), unit_price NUMERIC(18,2), line_total NUMERIC(18,2));
CREATE TABLE IF NOT EXISTS expenses(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), expense_date DATE NOT NULL, category TEXT, description TEXT, amount NUMERIC(18,2) NOT NULL, supplier TEXT, payment_method TEXT, created_by BIGINT REFERENCES users(id));
CREATE TABLE IF NOT EXISTS journals(id BIGSERIAL PRIMARY KEY, company_id BIGINT REFERENCES companies(id), entry_date DATE NOT NULL, reference TEXT NOT NULL, description TEXT, status TEXT DEFAULT 'draft', created_by BIGINT REFERENCES users(id), approved_by BIGINT REFERENCES users(id), created_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS journal_lines(id BIGSERIAL PRIMARY KEY, journal_id BIGINT REFERENCES journals(id), account_id BIGINT REFERENCES accounts(id), debit NUMERIC(18,2) DEFAULT 0, credit NUMERIC(18,2) DEFAULT 0, CHECK((debit=0 AND credit>0) OR (credit=0 AND debit>0)));
CREATE TABLE IF NOT EXISTS audit_log(id BIGSERIAL PRIMARY KEY, company_id BIGINT, user_id BIGINT, action TEXT, entity TEXT, entity_id BIGINT, detail TEXT, created_at TIMESTAMPTZ DEFAULT now());
'''

def hash_pw(p): return bcrypt.hashpw(p.encode(),bcrypt.gensalt()).decode()
def verify_pw(p,h):
    try: return bcrypt.checkpw(p.encode(),h.encode())
    except Exception: return False
def run(sql,params=None):
    with engine.begin() as c: return c.execute(text(sql),params or {})
def read(sql,params=None):
    with engine.begin() as c: return pd.read_sql(text(sql),c,params=params or {})
def csv_button(df,name): st.download_button(f'Download {name} CSV',df.to_csv(index=False),f'{name.lower().replace(" ","_")}.csv','text/csv')
def pdf_button(df,name):
    b=io.BytesIO(); c=canvas.Canvas(b,pagesize=A4); y=800; c.setFont('Helvetica-Bold',14); c.drawString(35,y,name); y-=25; c.setFont('Helvetica',8)
    for _,r in df.iterrows():
        c.drawString(35,y,' | '.join(str(x)[:25] for x in r.tolist())); y-=13
        if y<40: c.showPage(); y=800
    c.save(); st.download_button(f'Download {name} PDF',b.getvalue(),f'{name.lower().replace(" ","_")}.pdf','application/pdf')

def setup():
    with engine.begin() as c:
        for s in SCHEMA.split(';'):
            if s.strip(): c.execute(text(s))
        # Upgrade the earlier Neon schema without deleting existing data.
        c.execute(text("ALTER TABLE companies ADD COLUMN IF NOT EXISTS name TEXT"))
        c.execute(text("UPDATE companies SET name=COALESCE(NULLIF(name,''), trading_name, legal_name, 'Soulfyas Quality Restaurant') WHERE name IS NULL OR name=''"))
        if c.execute(text('SELECT COUNT(*) FROM companies')).scalar()==0:
            cid=c.execute(text("INSERT INTO companies(name) VALUES('Soulfyas Quality Restaurant') RETURNING id")).scalar_one()
            accounts=[('1000','Cash','asset'),('1100','Bank','asset'),('1200','Inventory','asset'),('2000','Trade Payables','liability'),('3000','Equity','equity'),('4000','Restaurant Revenue','revenue'),('5000','Cost of Sales','expense'),('6000','Operating Expenses','expense'),('2100','VAT Payable','liability'),('2200','PAYE Payable','liability'),('2210','NSSA Payable','liability')]
            for code,name,typ in accounts: c.execute(text('INSERT INTO accounts(company_id,code,name,account_type) VALUES(:c,:o,:n,:t)'),{'c':cid,'o':code,'n':name,'t':typ})
            c.execute(text("INSERT INTO users(company_id,username,full_name,password_hash,role) VALUES(:c,'admin','System Administrator',:p,'admin')"),{'c':cid,'p':hash_pw('ChangeMe123!')})
        # Ensure an administrator exists even when the company was created by an earlier schema.
        cid=c.execute(text('SELECT id FROM companies ORDER BY id LIMIT 1')).scalar_one()
        if c.execute(text('SELECT COUNT(*) FROM users')).scalar()==0:
            c.execute(text("INSERT INTO users(company_id,username,full_name,password_hash,role) VALUES(:c,'admin','System Administrator',:p,'admin')"),{'c':cid,'p':hash_pw('ChangeMe123!')})
setup()
# Existing Neon installations may have been created from the earlier schema.
# Keep the application compatible by using the canonical company columns.
company=read('SELECT * FROM companies LIMIT 1').iloc[0].to_dict()
company.setdefault('name', company.get('trading_name') or company.get('legal_name') or 'Soulfyas Quality Restaurant')
company.setdefault('address', '')
company.setdefault('phone', '')
company.setdefault('zimra_tin', '')
company.setdefault('vat_number', '')
company.setdefault('nssa_number', '')

def login():
    st.title('🍽️ Soulfyas Quality Restaurant'); st.caption('Secure restaurant ERP')
    with st.form('login'):
        u=st.text_input('Username'); p=st.text_input('Password',type='password'); ok=st.form_submit_button('Sign in',use_container_width=True)
    if ok:
        d=read('SELECT * FROM users WHERE username=:u AND active=true',{'u':u.strip()})
        if len(d) and verify_pw(p,str(d.iloc[0].password_hash)): st.session_state.user=d.iloc[0].to_dict(); st.rerun()
        else: st.error('Invalid username or password')
    st.info('Initial login: admin / ChangeMe123! — change it immediately.')
if 'user' not in st.session_state: login(); st.stop()
u=st.session_state.user
pages=['Dashboard','Point of Sale','Invoices','Menu','Expenses','Inventory','Financial Statements','Tax & Payroll','Journal Adjustments','Customers & Suppliers','User Administration','Settings']
with st.sidebar:
    if os.path.exists(LOGO): st.image(LOGO,width=150)
    st.caption(f"{u['full_name']} · {u['role'].title()}"); page=st.radio('Navigate',pages)
    if st.button('Sign out'): del st.session_state.user; st.rerun()
st.title(page)

if page=='Dashboard':
    d=str(date.today()); rev=read('SELECT COALESCE(SUM(total),0) x FROM sales WHERE sale_date=:d',{'d':d}).iloc[0,0]; ex=read('SELECT COALESCE(SUM(amount),0) x FROM expenses WHERE expense_date=:d',{'d':d}).iloc[0,0]
    a,b,c=st.columns(3); a.metric('Today sales',f'${float(rev):,.2f}'); b.metric('Today expenses',f'${float(ex):,.2f}'); c.metric('Net',f'${float(rev-ex):,.2f}')
    st.dataframe(read('SELECT invoice_no,sale_date,payment_method,total,status FROM sales ORDER BY id DESC LIMIT 15'),use_container_width=True,hide_index=True)
elif page=='Point of Sale':
    items=read('SELECT * FROM menu_items WHERE company_id=:c AND active=true ORDER BY name',{'c':company['id']})
    if not len(items): st.warning('Add menu items first.'); st.stop()
    with st.form('pos'):
        selected=[]
        for i,r in items.iterrows():
            q=st.number_input(f"{r['name']} (${float(r['price']):,.2f})",0.0,step=1.0,key=f'item{i}')
            if q: selected.append((int(r.id),q,float(r.price),q*float(r.price)))
        method=st.selectbox('Payment method',['Cash','Card','Mobile money','Bank transfer','Credit']); ok=st.form_submit_button('Complete sale',type='primary')
    if ok and selected:
        sub=sum(x[3] for x in selected); tax=sub*0.0; total=sub+tax; inv=f"SQR-{datetime.now():%Y%m%d%H%M%S}-{secrets.token_hex(2).upper()}"
        with engine.begin() as c:
            sid=c.execute(text('INSERT INTO sales(company_id,invoice_no,sale_date,payment_method,subtotal,tax,total,created_by) VALUES(:c,:i,:d,:m,:s,:t,:v,:u) RETURNING id'),{'c':company['id'],'i':inv,'d':str(date.today()),'m':method,'s':sub,'t':tax,'v':total,'u':u['id']}).scalar_one()
            for iid,q,p,l in selected: c.execute(text('INSERT INTO sale_lines(sale_id,item_id,quantity,unit_price,line_total) VALUES(:s,:i,:q,:p,:l)'),{'s':sid,'i':iid,'q':q,'p':p,'l':l})
        st.success(f'{inv} recorded: ${total:,.2f}')
elif page=='Menu':
    with st.form('menu'):
        n=st.text_input('Item name'); cat=st.text_input('Category'); price=st.number_input('Selling price',0.0); cost=st.number_input('Cost',0.0); ok=st.form_submit_button('Add item')
    if ok and n: run('INSERT INTO menu_items(company_id,name,category,price,cost) VALUES(:c,:n,:g,:p,:o)',{'c':company['id'],'n':n,'g':cat,'p':price,'o':cost}); st.rerun()
    st.dataframe(read('SELECT id,name,category,price,cost,active FROM menu_items WHERE company_id=:c ORDER BY name',{'c':company['id']}),use_container_width=True,hide_index=True)
elif page=='Expenses':
    with st.form('expense'):
        dt=st.date_input('Date'); cat=st.text_input('Category'); desc=st.text_input('Description'); amount=st.number_input('Amount',0.0); supplier=st.text_input('Supplier'); method=st.selectbox('Payment method',['Cash','Card','Bank transfer','Mobile money']); ok=st.form_submit_button('Record expense')
    if ok and amount: run('INSERT INTO expenses(company_id,expense_date,category,description,amount,supplier,payment_method,created_by) VALUES(:c,:d,:g,:x,:a,:s,:m,:u)',{'c':company['id'],'d':str(dt),'g':cat,'x':desc,'a':amount,'s':supplier,'m':method,'u':u['id']}); st.rerun()
    df=read('SELECT * FROM expenses WHERE company_id=:c ORDER BY id DESC',{'c':company['id']}); st.dataframe(df,use_container_width=True,hide_index=True); csv_button(df,'Expenses'); pdf_button(df,'Expenses')
elif page=='Inventory':
    with st.form('inventory'):
        n=st.text_input('Item'); cat=st.text_input('Category'); unit=st.text_input('Unit',value='each'); qty=st.number_input('Quantity',0.0); reorder=st.number_input('Reorder level',0.0); cost=st.number_input('Unit cost',0.0); ok=st.form_submit_button('Add stock')
    if ok and n: run('INSERT INTO inventory(company_id,item_name,category,unit,quantity,reorder_level,unit_cost) VALUES(:c,:n,:g,:u,:q,:r,:o)',{'c':company['id'],'n':n,'g':cat,'u':unit,'q':qty,'r':reorder,'o':cost}); st.rerun()
    df=read('SELECT * FROM inventory WHERE company_id=:c ORDER BY item_name',{'c':company['id']}); st.dataframe(df,use_container_width=True,hide_index=True); csv_button(df,'Inventory'); pdf_button(df,'Inventory')
elif page=='Invoices':
    df=read('SELECT invoice_no,sale_date,payment_method,subtotal,tax,total,status FROM sales WHERE company_id=:c ORDER BY id DESC',{'c':company['id']}); st.dataframe(df,use_container_width=True,hide_index=True); csv_button(df,'Invoices'); pdf_button(df,'Invoices')
elif page=='Financial Statements':
    start=st.date_input('From',date(date.today().year,1,1)); end=st.date_input('To',date.today()); revenue=float(read('SELECT COALESCE(SUM(subtotal),0) x FROM sales WHERE sale_date BETWEEN :a AND :b',{'a':str(start),'b':str(end)}).iloc[0,0]); expenses=float(read('SELECT COALESCE(SUM(amount),0) x FROM expenses WHERE expense_date BETWEEN :a AND :b',{'a':str(start),'b':str(end)}).iloc[0,0]); profit=revenue-expenses
    df=pd.DataFrame({'IFRS 18 statement of profit or loss':['Revenue','Operating expenses','Operating profit','Profit before financing and income taxes','Income tax expense','Profit for the period'],'Amount':[revenue,expenses,profit,profit,0,profit]}); st.dataframe(df,use_container_width=True,hide_index=True); csv_button(df,'Income Statement'); pdf_button(df,'Income Statement'); st.info('IFRS 18 is effective for annual periods beginning 1 January 2027. Final statutory reporting requires a complete trial balance and accountant-reviewed configuration.')
elif page=='Tax & Payroll':
    st.subheader('Zimbabwe tax configuration'); st.write('Configure ZIMRA TIN, VAT, PAYE, withholding tax, IMTT, fiscalisation and NSSA POBS/APWCS. Rates and ceilings must be updated from current official notices.'); st.table(pd.DataFrame({'Obligation':['VAT','PAYE','Withholding tax','IMTT','NSSA POBS','NSSA APWCS','Fiscalisation'],'Authority':['ZIMRA','ZIMRA','ZIMRA','ZIMRA','NSSA','NSSA','ZIMRA']}))
elif page=='Journal Adjustments':
    if u['role'] not in ('admin','manager'): st.error('Top-management access required.'); st.stop()
    with st.form('journal'):
        dt=st.date_input('Date'); ref=st.text_input('Reference'); desc=st.text_input('Description'); account=st.text_input('Account'); debit=st.number_input('Debit',0.0); credit=st.number_input('Credit',0.0); ok=st.form_submit_button('Record adjustment')
    if ok and ref and account and ((debit>0) ^ (credit>0)): run('INSERT INTO journals(company_id,entry_date,reference,description,status,created_by) VALUES(:c,:d,:r,:x,\'posted\',:u)',{'c':company['id'],'d':str(dt),'r':ref,'x':desc,'u':u['id']}); st.success('Adjustment recorded; approval and balanced batch review required.')
elif page=='Customers & Suppliers':
    a,b=st.tabs(['Customers','Suppliers'])
    with a:
        with st.form('customer'): n=st.text_input('Customer name'); p=st.text_input('Phone'); e=st.text_input('Email'); ok=st.form_submit_button('Add customer')
        if ok and n: run('INSERT INTO customers(company_id,name,phone,email) VALUES(:c,:n,:p,:e)',{'c':company['id'],'n':n,'p':p,'e':e}); st.rerun()
        st.dataframe(read('SELECT * FROM customers WHERE company_id=:c',{'c':company['id']}),use_container_width=True,hide_index=True)
    with b:
        with st.form('supplier'): n=st.text_input('Supplier name'); p=st.text_input('Phone'); e=st.text_input('Email'); ok=st.form_submit_button('Add supplier')
        if ok and n: run('INSERT INTO suppliers(company_id,name,phone,email) VALUES(:c,:n,:p,:e)',{'c':company['id'],'n':n,'p':p,'e':e}); st.rerun()
        st.dataframe(read('SELECT * FROM suppliers WHERE company_id=:c',{'c':company['id']}),use_container_width=True,hide_index=True)
elif page=='User Administration':
    if u['role']!='admin': st.error('Administrator access required.'); st.stop()
    with st.form('newuser'):
        un=st.text_input('Username'); fn=st.text_input('Full name'); pw=st.text_input('Temporary password',type='password'); role=st.selectbox('Role',['employee','manager','admin']); ok=st.form_submit_button('Create account')
    if ok and un and fn and pw:
        run('INSERT INTO users(company_id,username,full_name,password_hash,role) VALUES(:c,:u,:f,:p,:r)',{'c':company['id'],'u':un,'f':fn,'p':hash_pw(pw),'r':role}); st.success('Account created')
    st.dataframe(read('SELECT id,username,full_name,role,active,created_at FROM users WHERE company_id=:c',{'c':company['id']}),use_container_width=True,hide_index=True)
elif page=='Settings':
    if u['role']!='admin': st.error('Administrator access required.'); st.stop()
    with st.form('settings'):
        n=st.text_input('Restaurant name',company['name']); a=st.text_input('Address',company['address']); p=st.text_input('Phone',company['phone']); tin=st.text_input('ZIMRA TIN',company['zimra_tin']); vat=st.text_input('VAT number',company['vat_number']); nssa=st.text_input('NSSA number',company['nssa_number']); ok=st.form_submit_button('Save settings')
    if ok: run('UPDATE companies SET name=:n,address=:a,phone=:p,zimra_tin=:t,vat_number=:v,nssa_number=:s WHERE id=:c',{'n':n,'a':a,'p':p,'t':tin,'v':vat,'s':nssa}); st.success('Settings saved. Refresh the app to reload company details.')
