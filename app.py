import os, io, html, secrets
from datetime import date, datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from passlib.hash import bcrypt

st.set_page_config(page_title="Soulfyas ERP", page_icon="🍽️", layout="wide", initial_sidebar_state="expanded")
DB_URL=os.getenv("DATABASE_URL", "sqlite:///soulfyas.db")
engine=create_engine(DB_URL, future=True)
LOGO="soulfyas_logo.png"

SCHEMA='''
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, full_name TEXT NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'employee', active INTEGER DEFAULT 1, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS menu_items (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT, price REAL NOT NULL, cost REAL DEFAULT 0, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT, email TEXT);
CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT, email TEXT);
CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, invoice_no TEXT UNIQUE NOT NULL, sale_date TEXT NOT NULL, customer_id INTEGER, payment_method TEXT, subtotal REAL, tax REAL, total REAL, status TEXT DEFAULT 'Paid', created_by TEXT);
CREATE TABLE IF NOT EXISTS sale_lines (id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL, item_id INTEGER NOT NULL, quantity REAL NOT NULL, unit_price REAL NOT NULL, line_total REAL NOT NULL);
CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, expense_date TEXT NOT NULL, category TEXT, description TEXT, amount REAL NOT NULL, supplier TEXT, payment_method TEXT, created_by TEXT);
CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, item_name TEXT NOT NULL, category TEXT, unit TEXT, quantity REAL DEFAULT 0, reorder_level REAL DEFAULT 0, unit_cost REAL DEFAULT 0);
CREATE TABLE IF NOT EXISTS stock_movements (id INTEGER PRIMARY KEY, movement_date TEXT NOT NULL, item_id INTEGER, movement_type TEXT, quantity REAL, unit_cost REAL, notes TEXT, created_by TEXT);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS journal_entries (id INTEGER PRIMARY KEY, entry_date TEXT NOT NULL, account TEXT NOT NULL, description TEXT, debit REAL DEFAULT 0, credit REAL DEFAULT 0, reference TEXT, created_by TEXT, updated_at TEXT);
'''

def init_db():
    with engine.begin() as c:
        for stmt in SCHEMA.split(';'):
            if stmt.strip(): c.execute(text(stmt))
        n=c.execute(text('SELECT COUNT(*) FROM users')).scalar()
        if n==0:
            c.execute(text("INSERT INTO users(username,full_name,password_hash,role,created_at) VALUES(:u,:f,:p,'admin',:d)"), {"u":"admin","f":"System Administrator","p":bcrypt.hash("ChangeMe123!"),"d":datetime.now().isoformat()})
        defaults={"restaurant_name":"Soulfyas Quality Restaurant","address":"","phone":"","tax_rate":"0"}
        for k,v in defaults.items(): c.execute(text("INSERT OR IGNORE INTO settings(key,value) VALUES(:k,:v)"),{"k":k,"v":v})
init_db()

def q(sql, params=None):
    with engine.begin() as c:
        return pd.read_sql(text(sql), c, params=params or {})
def execsql(sql, params=None):
    with engine.begin() as c: return c.execute(text(sql), params or {})
def setting(k):
    d=q("SELECT value FROM settings WHERE key=:k",{"k":k}); return d.iloc[0,0] if len(d) else ""

def login():
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    if os.path.exists(LOGO): st.image(LOGO, width=180)
    st.title("Soulfyas ERP")
    st.caption("Restaurant operations, finance and controls")
    with st.form("login"):
        u=st.text_input("Username")
        p=st.text_input("Password", type="password")
        ok=st.form_submit_button("Sign in", use_container_width=True)
    if ok:
        d=q("SELECT * FROM users WHERE username=:u AND active=1",{"u":u.strip()})
        if len(d) and bcrypt.verify(p,d.iloc[0].password_hash):
            st.session_state.user=d.iloc[0].to_dict(); st.rerun()
        else: st.error("Invalid username or password")
    st.info("First login: admin / ChangeMe123! — change this immediately in User Administration.")
    st.markdown("</div>", unsafe_allow_html=True)

def money(x): return f"${float(x or 0):,.2f}"
def csv_download(df, label):
    st.download_button(f"Download {label} CSV", df.to_csv(index=False).encode('utf-8'), file_name=f"{label.lower().replace(' ','_')}.csv", mime='text/csv')
def pdf_download(title, df, label):
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=A4); w,h=A4; c.setFont('Helvetica-Bold',15); c.drawString(40,h-45,title); c.setFont('Helvetica',8); y=h-70
    for col in df.columns: c.drawString(40+list(df.columns).index(col)*85,y,str(col)[:13])
    y-=16
    for _,row in df.iterrows():
        for j,val in enumerate(row): c.drawString(40+j*85,y,str(val)[:14])
        y-=13
        if y<45: c.showPage(); y=h-45
    c.save(); st.download_button(f"Download {label} PDF",buf.getvalue(),file_name=f"{label.lower().replace(' ','_')}.pdf",mime='application/pdf')
def invoice_html(sale, lines):
    rows=''.join(f"<tr><td>{html.escape(str(x['name']))}</td><td>{x['quantity']}</td><td>{money(x['unit_price'])}</td><td>{money(x['line_total'])}</td></tr>" for _,x in lines.iterrows())
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{font-family:Arial;color:#222;padding:40px}}h1{{color:#b78b2b}}table{{width:100%;border-collapse:collapse;margin-top:25px}}td,th{{padding:10px;border-bottom:1px solid #ddd;text-align:left}}.total{{text-align:right;font-size:20px;margin-top:20px}}</style></head><body><h1>{html.escape(setting('restaurant_name'))}</h1><p>{html.escape(setting('address'))}<br>{html.escape(setting('phone'))}</p><h2>INVOICE {sale['invoice_no']}</h2><p>Date: {sale['sale_date']}<br>Payment: {sale['payment_method']}</p><table><tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>{rows}</table><div class="total">Subtotal: {money(sale['subtotal'])}<br>Tax: {money(sale['tax'])}<br><b>Total: {money(sale['total'])}</b></div><p>Thank you for dining with us.</p></body></html>'''

if 'user' not in st.session_state: login(); st.stop()
user=st.session_state.user
with st.sidebar:
    if os.path.exists(LOGO): st.image(LOGO, width=145)
    st.caption(f"{user['full_name']} · {user['role'].title()}")
    pages=["Dashboard","Point of Sale","Invoices","Menu","Expenses","Inventory","Financial Statements","Tax & Payroll","Journal Adjustments","Customers & Suppliers","User Administration","Settings"]
    page=st.radio("Navigate",pages)
    if st.button("Sign out"): del st.session_state.user; st.rerun()

st.title(page)
if page=="Dashboard":
    today=str(date.today()); sales=q("SELECT COALESCE(SUM(total),0) v FROM sales WHERE sale_date=:d",{"d":today}).iloc[0,0]; exp=q("SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE expense_date=:d",{"d":today}).iloc[0,0]; orders=q("SELECT COUNT(*) v FROM sales WHERE sale_date=:d",{"d":today}).iloc[0,0]
    a,b,c,d=st.columns(4); a.metric("Today's sales",money(sales)); b.metric("Today's expenses",money(exp)); c.metric("Orders",int(orders)); c.metric("Gross cash",money(sales-exp));
    st.subheader("Recent invoices"); st.dataframe(q("SELECT invoice_no,sale_date,payment_method,total,status,created_by FROM sales ORDER BY id DESC LIMIT 10"),use_container_width=True,hide_index=True)
    st.subheader("Low stock alerts"); low=q("SELECT item_name,quantity,reorder_level FROM inventory WHERE quantity<=reorder_level ORDER BY quantity"); st.dataframe(low,use_container_width=True,hide_index=True) if len(low) else st.success("No low-stock items.")

elif page=="Point of Sale":
    items=q("SELECT * FROM menu_items WHERE active=1 ORDER BY category,name")
    if not len(items): st.warning("Add menu items first."); st.stop()
    with st.form("sale"):
        cols=st.columns(3); chosen=[]
        for i,r in items.iterrows():
            with cols[i%3]:
                qty=st.number_input(f"{r['name']} ({money(r['price'])})",min_value=0.0,step=1.0,key=f"qty{i}")
                if qty: chosen.append((int(r.id),r['name'],qty,float(r.price),qty*float(r.price)))
        method=st.selectbox("Payment method",["Cash","Card","Mobile money","Bank transfer","Credit"]); submit=st.form_submit_button("Complete sale",type="primary")
    if submit:
        if not chosen: st.error("Select at least one item.")
        else:
            sub=sum(x[4] for x in chosen); tax=sub*float(setting('tax_rate') or 0)/100; total=sub+tax; inv=f"SQR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(2).upper()}"
            with engine.begin() as c:
                res=c.execute(text("INSERT INTO sales(invoice_no,sale_date,payment_method,subtotal,tax,total,created_by) VALUES(:i,:d,:m,:s,:t,:v,:u)"),{"i":inv,"d":str(date.today()),"m":method,"s":sub,"t":tax,"v":total,"u":user['username']}); sid=res.lastrowid
                for iid,n,qty,price,line in chosen: c.execute(text("INSERT INTO sale_lines(sale_id,item_id,quantity,unit_price,line_total) VALUES(:s,:i,:q,:p,:l)"),{"s":sid,"i":iid,"q":qty,"p":price,"l":line})
            st.success(f"Sale {inv} recorded: {money(total)}")

elif page=="Invoices":
    inv=q("SELECT * FROM sales ORDER BY id DESC"); st.dataframe(inv,use_container_width=True,hide_index=True); csv_download(inv,'Invoices'); pdf_download('Soulfyas Invoices',inv,'Invoices')
    if len(inv):
        no=st.selectbox("Download invoice",inv.invoice_no.tolist()); sale=inv[inv.invoice_no==no].iloc[0]; lines=q("SELECT m.name,l.quantity,l.unit_price,l.line_total FROM sale_lines l JOIN menu_items m ON m.id=l.item_id WHERE l.sale_id=:s",{"s":int(sale.id)}); st.download_button("Download invoice HTML",invoice_html(sale,lines),file_name=f"{no}.html",mime="text/html")

elif page=="Menu":
    with st.form("newmenu"):
        a,b,c,d=st.columns(4); name=a.text_input("Item name"); cat=b.text_input("Category"); price=c.number_input("Selling price",min_value=0.0); cost=d.number_input("Cost",min_value=0.0); ok=st.form_submit_button("Add item")
    if ok and name: execsql("INSERT INTO menu_items(name,category,price,cost) VALUES(:n,:c,:p,:o)",{"n":name,"c":cat,"p":price,"o":cost}); st.rerun()
    st.dataframe(q("SELECT * FROM menu_items ORDER BY category,name"),use_container_width=True,hide_index=True)

elif page=="Expenses":
    with st.form("expense"):
        a,b,c=st.columns(3); dt=a.date_input("Date"); cat=b.text_input("Category"); desc=c.text_input("Description"); amt=st.number_input("Amount",min_value=0.0); supplier=st.text_input("Supplier"); method=st.selectbox("Payment method",["Cash","Card","Bank transfer","Mobile money"]); ok=st.form_submit_button("Record expense")
    if ok and amt: execsql("INSERT INTO expenses(expense_date,category,description,amount,supplier,payment_method,created_by) VALUES(:d,:c,:x,:a,:s,:m,:u)",{"d":str(dt),"c":cat,"x":desc,"a":amt,"s":supplier,"m":method,"u":user['username']}); st.rerun()
    expdf=q("SELECT * FROM expenses ORDER BY id DESC"); st.dataframe(expdf,use_container_width=True,hide_index=True); csv_download(expdf,'Expenses'); pdf_download('Soulfyas Expenses',expdf,'Expenses')

elif page=="Inventory":
    with st.form("stock"):
        a,b,c,d,e=st.columns(5); n=a.text_input("Item"); cat=b.text_input("Category"); unit=c.text_input("Unit",value="each"); qty=d.number_input("Quantity",min_value=0.0); reorder=e.number_input("Reorder level",min_value=0.0); cost=st.number_input("Unit cost",min_value=0.0); ok=st.form_submit_button("Add stock item")
    if ok and n: execsql("INSERT INTO inventory(item_name,category,unit,quantity,reorder_level,unit_cost) VALUES(:n,:c,:u,:q,:r,:o)",{"n":n,"c":cat,"u":unit,"q":qty,"r":reorder,"o":cost}); st.rerun()
    invdf=q("SELECT * FROM inventory ORDER BY item_name"); st.dataframe(invdf,use_container_width=True,hide_index=True); csv_download(invdf,'Inventory'); pdf_download('Soulfyas Inventory',invdf,'Inventory')

elif page=="Financial Statements":
    st.info("IFRS 18-ready presentation is designed for annual periods beginning 1 January 2027. IFRS 18 replaces IAS 1 and introduces operating, investing and financing categories, operating profit, profit before financing and income taxes, MPM disclosures and stronger aggregation/disaggregation.")
    start=st.date_input("From",date(date.today().year,1,1)); end=st.date_input("To",date.today())
    revenue=float(q("SELECT COALESCE(SUM(subtotal),0) v FROM sales WHERE sale_date BETWEEN :a AND :b",{"a":str(start),"b":str(end)}).iloc[0,0]); tax=float(q("SELECT COALESCE(SUM(tax),0) v FROM sales WHERE sale_date BETWEEN :a AND :b",{"a":str(start),"b":str(end)}).iloc[0,0]); expenses=float(q("SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE expense_date BETWEEN :a AND :b",{"a":str(start),"b":str(end)}).iloc[0,0]); inventory_value=float(q("SELECT COALESCE(SUM(quantity*unit_cost),0) v FROM inventory").iloc[0,0]); cash=revenue-expenses
    tabs=st.tabs(["Profit or loss","Financial position","Cash flows","Changes in equity","Notes & disclosures"])
    pnl=pd.DataFrame({"Statement of profit or loss (IFRS 18)": ["Revenue","Cost of sales / inventory consumption","Gross profit","Other operating income","Operating expenses","Operating profit","Investing income/(expense)","Profit before financing and income taxes","Finance income/(cost)","Profit before income tax","Income tax expense","Profit for the period"],"Amount":[revenue,0,revenue,0,expenses,revenue-expenses,0,revenue-expenses,0,revenue-expenses,0,revenue-expenses]})
    with tabs[0]: st.dataframe(pnl,use_container_width=True,hide_index=True); csv_download(pnl,'Income Statement'); pdf_download('Soulfyas IFRS 18 Profit or Loss',pnl,'Income Statement')
    bs=pd.DataFrame({"Statement of financial position": ["Cash and cash equivalents (operational proxy)","Inventory","Total assets","Trade and other payables","Total liabilities","Share capital and retained earnings","Total equity and liabilities"],"Amount":[cash,inventory_value,cash+inventory_value,0,0,cash+inventory_value,cash+inventory_value]})
    with tabs[1]: st.dataframe(bs,use_container_width=True,hide_index=True); csv_download(bs,'Statement of Financial Position'); pdf_download('Soulfyas Statement of Financial Position',bs,'Statement of Financial Position')
    cf=pd.DataFrame({"Statement of cash flows": ["Cash flows from operating activities","Cash flows from investing activities","Cash flows from financing activities","Net increase/(decrease) in cash","Opening cash","Closing cash"],"Amount":[revenue-expenses,0,0,cash,0,cash]})
    with tabs[2]: st.dataframe(cf,use_container_width=True,hide_index=True); csv_download(cf,'Cash Flow Statement'); pdf_download('Soulfyas Cash Flow Statement',cf,'Cash Flow Statement')
    eq=pd.DataFrame({"Statement of changes in equity": ["Opening equity","Profit for the period","Dividends/distributions","Closing equity"],"Amount":[0,revenue-expenses,0,revenue-expenses]})
    with tabs[3]: st.dataframe(eq,use_container_width=True,hide_index=True); csv_download(eq,'Changes in Equity'); pdf_download('Soulfyas Changes in Equity',eq,'Changes in Equity')
    with tabs[4]:
        st.markdown("**Required design controls:** comparative prior-period columns; material accounting policy information; operating/investing/financing classification; MPM register and reconciliations; expense disaggregation by nature/function; going concern; related parties; events after reporting period; contingencies; commitments; tax; leases; employee benefits; revenue; financial instruments; impairment; inventory; PPE; provisions; and foreign exchange.")
        st.caption("These are operational statements based on the current starter data model, not a certified IFRS set. A Zimbabwe-registered accountant must configure the chart of accounts, tax rules, liabilities, equity, adjustments and disclosures before statutory use.")

elif page=="Tax & Payroll":
    st.subheader("Zimbabwe tax and statutory configuration")
    st.warning("Rates and thresholds change. Store effective-dated rules and verify every filing against ZIMRA/NSSA notices before submission.")
    with st.form("taxsettings"):
        a,b,c,d=st.columns(4); tin=a.text_input("ZIMRA TIN"); vat=b.text_input("VAT number"); nssa=b.text_input("NSSA employer number"); currency=c.selectbox("Functional currency",["USD","ZiG","Other"]); vat_rate=d.number_input("VAT rate %",min_value=0.0,value=15.0); ok=st.form_submit_button("Save tax profile")
    if ok:
        for k,v in [("zimra_tin",tin),("vat_number",vat),("nssa_number",nssa),("currency",currency),("vat_rate",str(vat_rate))]: execsql("INSERT OR REPLACE INTO settings(key,value) VALUES(:k,:v)",{"k":k,"v":v})
        st.success("Tax profile saved")
    st.subheader("NSSA Pension and Other Benefits Scheme")
    st.write("Default configurable rule: employee 4.5% and employer 4.5% of insurable earnings, subject to the current gazetted ceiling. The current NSSA site shows a USD 700 ceiling; verify the current quarter before payroll.")
    st.subheader("Tax obligations to support")
    taxob=pd.DataFrame({"Obligation":["VAT","PAYE","Withholding tax","IMTT","Corporate income tax","NSSA POBS","NSSA APWCS","Fiscalisation"],"Authority":["ZIMRA","ZIMRA","ZIMRA","ZIMRA","ZIMRA","NSSA","NSSA","ZIMRA"],"Status":["Configure","Configure","Configure","Configure","Configure","Enabled","Configure","Configure"]})
    st.dataframe(taxob,use_container_width=True,hide_index=True); csv_download(taxob,'Tax Obligations'); pdf_download('Soulfyas Tax Obligations',taxob,'Tax Obligations')
elif page=="Journal Adjustments":
    if user['role'] not in ('admin','manager'):
        st.error("Top management access required."); st.stop()
    st.warning("Use this controlled journal for approved corrections. Posted sales and expenses should not be silently overwritten; use a reversing or correcting entry with a reference.")
    with st.form("journal"):
        a,b,c,d,e=st.columns(5); dt=a.date_input("Entry date"); account=b.text_input("Account"); desc=c.text_input("Description"); debit=d.number_input("Debit",min_value=0.0); credit=e.number_input("Credit",min_value=0.0); ref=st.text_input("Approval/reference"); ok=st.form_submit_button("Post adjustment")
    if ok and account and (debit or credit) and ref:
        execsql("INSERT INTO journal_entries(entry_date,account,description,debit,credit,reference,created_by,updated_at) VALUES(:d,:a,:x,:dr,:cr,:r,:u,:t)",{"d":str(dt),"a":account,"x":desc,"dr":debit,"cr":credit,"r":ref,"u":user['username'],"t":datetime.now().isoformat()}); st.success("Adjustment posted")
    je=q("SELECT * FROM journal_entries ORDER BY id DESC"); st.dataframe(je,use_container_width=True,hide_index=True); csv_download(je,'Journal Adjustments'); pdf_download('Soulfyas Journal Adjustments',je,'Journal Adjustments')
    st.caption("For production, enforce balanced double-entry batches, approval workflow, period locks and immutable audit history.")

elif page=="Customers & Suppliers":
    tab1,tab2=st.tabs(["Customers","Suppliers"])
    with tab1:
        with st.form("cust"): n=st.text_input("Customer name"); p=st.text_input("Phone"); e=st.text_input("Email"); ok=st.form_submit_button("Add customer")
        if ok and n: execsql("INSERT INTO customers(name,phone,email) VALUES(:n,:p,:e)",{"n":n,"p":p,"e":e}); st.rerun()
        st.dataframe(q("SELECT * FROM customers"),use_container_width=True,hide_index=True)
    with tab2:
        with st.form("supp"): n=st.text_input("Supplier name"); p=st.text_input("Phone"); e=st.text_input("Email"); ok=st.form_submit_button("Add supplier")
        if ok and n: execsql("INSERT INTO suppliers(name,phone,email) VALUES(:n,:p,:e)",{"n":n,"p":p,"e":e}); st.rerun()
        st.dataframe(q("SELECT * FROM suppliers"),use_container_width=True,hide_index=True)

elif page=="User Administration":
    if user['role']!='admin': st.error("Administrator access required."); st.stop()
    with st.form("useradd"):
        a,b,c,d=st.columns(4); un=a.text_input("Username"); fn=b.text_input("Full name"); pw=c.text_input("Temporary password",type="password"); role=d.selectbox("Role",["employee","manager","admin"]); ok=st.form_submit_button("Create account")
    if ok and un and fn and pw:
        try: execsql("INSERT INTO users(username,full_name,password_hash,role,created_at) VALUES(:u,:f,:p,:r,:d)",{"u":un,"f":fn,"p":bcrypt.hash(pw),"r":role,"d":datetime.now().isoformat()}); st.success("Account created")
        except Exception as e: st.error(str(e))
    st.dataframe(q("SELECT id,username,full_name,role,active,created_at FROM users"),use_container_width=True,hide_index=True)

elif page=="Settings":
    if user['role']!='admin': st.error("Administrator access required."); st.stop()
    with st.form("settings"):
        n=st.text_input("Restaurant name",setting('restaurant_name')); a=st.text_input("Address",setting('address')); p=st.text_input("Phone",setting('phone')); tax=st.number_input("Tax rate %",value=float(setting('tax_rate') or 0)); ok=st.form_submit_button("Save settings")
    if ok:
        for k,v in [("restaurant_name",n),("address",a),("phone",p),("tax_rate",str(tax))]: execsql("INSERT OR REPLACE INTO settings(key,value) VALUES(:k,:v)",{"k":k,"v":v})
        st.success("Settings saved")

st.markdown("<style>.stApp{background:#fbfaf7}.login-card{max-width:520px;margin:5vh auto;padding:2rem;background:white;border-radius:18px;box-shadow:0 8px 32px #0001}.stButton>button{border-radius:8px}.stMetric{background:white;padding:10px;border-radius:10px}</style>",unsafe_allow_html=True)
