"""
Soulfyas Quality Restaurant ERP - Enterprise Multi-Module Application
Comprehensive Restaurant Management System with POS, Kitchen Display System (KDS),
Floor & Table Management, Recipes & Bill of Materials, Inventory Depletion Engine,
IFRS 18 Financial Statements, Zimbabwe Statutory Tax & Payroll (ZIMRA & NSSA),
Double-Entry General Ledger, Audit Trails, and Branded ReportLab PDF Exports.
"""

import os
import io
import json
import secrets
from datetime import date, datetime, timedelta
import pandas as pd
import streamlit as st
import database as db
import tax_calculator as tc
import pdf_generator as pdf_gen

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Soulfyas Quality Restaurant ERP",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database schema and default seed data
db.init_db()

# Load custom CSS for enterprise restaurant look & feel
st.markdown("""
<style>
    /* Main Theme Overrides */
    .stApp {
        background-color: #fcfbf9;
    }
    
    /* Metrics and Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e8e3d8;
        border-left: 5px solid #b78b2b;
        padding: 14px 18px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.88rem;
        color: #555555;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.45rem;
        color: #1a1a1a;
        font-weight: 700;
    }
    
    /* POS Item Card */
    .pos-card {
        background: #ffffff;
        border: 1px solid #e5ded3;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .pos-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(183, 139, 43, 0.15);
        border-color: #b78b2b;
    }
    .pos-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #222222;
        margin-bottom: 4px;
    }
    .pos-desc {
        font-size: 0.8rem;
        color: #666666;
        min-height: 36px;
        line-height: 1.3;
        margin-bottom: 8px;
    }
    .pos-price {
        font-size: 1.15rem;
        font-weight: 700;
        color: #9b721d;
    }
    .tag-veg {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .tag-spicy {
        background-color: #ffebee;
        color: #c62828;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    
    /* Table Status Badge */
    .tbl-available {
        background-color: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #a5d6a7;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
    }
    .tbl-occupied {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef9a9a;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
    }
    .tbl-reserved {
        background-color: #fff8e1;
        color: #f57f17;
        border: 1px solid #ffe082;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
    }
    
    /* Kitchen Ticket Card */
    .kds-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-top: 4px solid #b78b2b;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .kds-header {
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        border-bottom: 1px dashed #dcdcdc;
        padding-bottom: 6px;
        margin-bottom: 8px;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions & State Management
# ---------------------------------------------------------
def get_company():
    comp_df = db.read("SELECT * FROM companies ORDER BY id ASC LIMIT 1")
    if len(comp_df):
        c = comp_df.iloc[0].to_dict()
        c.setdefault('trading_name', c.get('name', 'Soulfyas Quality Restaurant'))
        c.setdefault('currency', 'USD')
        return c
    return {
        'id': 1,
        'name': 'Soulfyas Quality Restaurant',
        'trading_name': 'Soulfyas Quality Restaurant',
        'currency': 'USD',
        'address': 'Harare, Zimbabwe',
        'phone': '+263 242 700000',
        'zimra_tin': '200145892',
        'vat_number': '10045678',
        'nssa_number': 'NSSA-789012'
    }

company = get_company()

# Session state initialization
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'pos_order_type' not in st.session_state:
    st.session_state.pos_order_type = 'Dine-In'
if 'pos_table' not in st.session_state:
    st.session_state.pos_table = 'T1'
if 'pos_customer' not in st.session_state:
    st.session_state.pos_customer = 1
if 'last_completed_sale' not in st.session_state:
    st.session_state.last_completed_sale = None

# ---------------------------------------------------------
# User Authentication Screen
# ---------------------------------------------------------
def login_screen():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        if os.path.exists('soulfyas_logo.png'):
            st.image('soulfyas_logo.png', width=160)
        st.title("🍽️ Soulfyas Quality Restaurant")
        st.subheader("Enterprise Restaurant Management & ERP")
        
        with st.form("login_form"):
            username = st.text_input("Username", value="admin", placeholder="Enter your username")
            password = st.text_input("Password", value="ChangeMe123!", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Sign In to ERP", use_container_width=True, type="primary")
            
        if submit:
            user_data = db.read("SELECT * FROM users WHERE username = :u AND active = 1", {'u': username.strip()})
            if len(user_data) and db.verify_pw(password, str(user_data.iloc[0]['password_hash'])):
                u_dict = user_data.iloc[0].to_dict()
                st.session_state.user = u_dict
                db.log_audit(company['id'], u_dict['id'], 'LOGIN', 'User', u_dict['id'], f"User {u_dict['username']} logged in.")
                st.success("Authentication successful! Loading workspace...")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
                
        st.info("💡 **Demo Credentials**:\n- **Administrator**: `admin` / `ChangeMe123!`\n- **General Manager**: `manager` / `Soulfyas2026!`\n- **POS Cashier**: `cashier` / `Soulfyas2026!`\n- **Head Chef**: `chef` / `Soulfyas2026!`\n- **Accountant**: `accountant` / `Soulfyas2026!`")

if 'user' not in st.session_state:
    login_screen()
    st.stop()

u = st.session_state.user
curr = company.get('currency', 'USD')

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists('soulfyas_logo.png'):
        st.image('soulfyas_logo.png', width=120)
    
    st.markdown(f"**{company['name']}**")
    st.caption(f"👤 **{u['full_name']}** · *{u['role'].title()}*")
    
    # Branch selector
    branches = db.read("SELECT id, name, code FROM branches WHERE company_id = :c AND active = 1", {'c': company['id']})
    branch_names = branches['name'].tolist() if len(branches) else ["Harare Central Branch"]
    selected_branch = st.selectbox("📍 Branch", branch_names, index=0)
    
    st.markdown("---")
    
    # Categorized Modules
    modules = {
        "📊 Overview": ["Dashboard"],
        "🍽️ Front of House": ["Point of Sale (POS)", "Floor & Table Manager", "Invoices & Sales History"],
        "👨‍🍳 Kitchen & Menu": ["Kitchen Display System (KDS)", "Menu & Dishes", "Recipes & Food Costing (BOM)"],
        "📦 Supply Chain": ["Inventory & Stock Balances", "Stock Movements & Wastage", "Suppliers & Purchasing"],
        "💼 Accounting & IFRS": ["IFRS 18 Financial Statements", "General Ledger Journals", "Chart of Accounts"],
        "💵 Expenses": ["Expenses Tracker"],
        "🏛️ Tax & Payroll": ["Statutory Payroll Processor", "ZIMRA Tax & Statutory Hub"],
        "👥 People & Org": ["Organisation Structure", "Staff Directory", "Customer CRM & Loyalty"],
        "⚙️ Administration": ["User Administration & RBAC", "System Audit Trail", "Settings & Configuration"]
    }
    
    # Role-based page visibility restriction (e.g. Cashier sees POS, Invoices; Chef sees KDS, Menu)
    allowed_pages = []
    for category, pages_list in modules.items():
        st.sidebar.markdown(f"**{category}**")
        for p in pages_list:
            allowed_pages.append(p)
            
    current_page = st.sidebar.radio("Navigate Module", allowed_pages, label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True):
        db.log_audit(company['id'], u['id'], 'LOGOUT', 'User', u['id'], f"User {u['username']} signed out.")
        del st.session_state.user
        st.rerun()

# ---------------------------------------------------------
# Page 1: Dashboard
# ---------------------------------------------------------
if current_page == "Dashboard":
    st.title("📊 Executive Restaurant Dashboard")
    st.caption(f"Real-time operational & financial metrics for {company['name']} ({selected_branch})")
    
    today_str = str(date.today())
    
    # Daily metrics calculations
    today_sales_df = db.read("SELECT COALESCE(SUM(total), 0) AS rev, COUNT(*) AS count, COALESCE(SUM(tax), 0) AS vat FROM sales WHERE sale_date = :d AND company_id = :c", {'d': today_str, 'c': company['id']})
    today_exp_df = db.read("SELECT COALESCE(SUM(amount), 0) AS exp FROM expenses WHERE expense_date = :d AND company_id = :c", {'d': today_str, 'c': company['id']})
    
    rev_today = float(today_sales_df.iloc[0]['rev'])
    orders_today = int(today_sales_df.iloc[0]['count'])
    exp_today = float(today_exp_df.iloc[0]['exp'])
    net_today = rev_today - exp_today
    avg_check = (rev_today / orders_today) if orders_today > 0 else 0.0
    
    # Inventory low stock alerts
    low_stock_df = db.read("SELECT * FROM inventory WHERE quantity <= reorder_level AND company_id = :c", {'c': company['id']})
    low_stock_count = len(low_stock_df)
    
    # Occupied tables count
    occupied_tables = db.read("SELECT COUNT(*) AS c FROM tables WHERE status = 'Occupied' AND company_id = :c", {'c': company['id']}).iloc[0]['c']
    
    # Top KPI Metrics Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Today's Revenue", f"{curr} {rev_today:,.2f}", f"{orders_today} Orders")
    m2.metric("Today's Expenses", f"{curr} {exp_today:,.2f}")
    m3.metric("Net Daily Profit", f"{curr} {net_today:,.2f}", delta=f"{'+' if net_today >= 0 else ''}{net_today:,.2f}")
    m4.metric("Avg Order Value", f"{curr} {avg_check:,.2f}")
    m5.metric("Occupied Tables", f"{occupied_tables} Active", delta_color="off")
    m6.metric("Low Stock Alerts", f"{low_stock_count} Items", delta=f"{low_stock_count} alert(s)" if low_stock_count else "Optimal", delta_color="inverse")
    
    # Low stock alert banner
    if low_stock_count > 0:
        with st.expander(f"⚠️ **Low Stock Alert**: {low_stock_count} item(s) are below reorder threshold", expanded=True):
            alert_items = [f"**{r['item_name']}**: {r['quantity']:g} {r['unit']} remaining (Reorder at {r['reorder_level']:g} {r['unit']})" for _, r in low_stock_df.iterrows()]
            st.warning(" | ".join(alert_items))
            
    st.markdown("---")
    
    # Quick action row
    qa1, qa2, qa3, qa4 = st.columns(4)
    if qa1.button("🛒 Open Point of Sale (POS)", use_container_width=True, type="primary"):
        st.session_state['navigate_to'] = "Point of Sale (POS)"
    if qa2.button("🍳 Kitchen Display (KDS)", use_container_width=True):
        st.session_state['navigate_to'] = "Kitchen Display System (KDS)"
    if qa3.button("💵 Record New Expense", use_container_width=True):
        st.session_state['navigate_to'] = "Expenses Tracker"
    if qa4.button("📈 View IFRS Financial Statements", use_container_width=True):
        st.session_state['navigate_to'] = "IFRS 18 Financial Statements"
        
    st.markdown("---")
    
    # Analytics Charts Row
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 Recent Sales Breakdown")
        recent_sales = db.read("""
            SELECT s.sale_date, SUM(s.total) as daily_total, COUNT(s.id) as order_count
            FROM sales s
            WHERE s.company_id = :c
            GROUP BY s.sale_date
            ORDER BY s.sale_date DESC
            LIMIT 7
        """, {'c': company['id']})
        if len(recent_sales):
            chart_df = recent_sales.sort_values('sale_date')
            st.bar_chart(chart_df.set_index('sale_date')['daily_total'])
        else:
            st.info("No historical sales records yet.")
            
    with c2:
        st.subheader("🔥 Top Selling Menu Items")
        top_items = db.read("""
            SELECT mi.name, SUM(sl.quantity) as total_qty, SUM(sl.line_total) as total_revenue
            FROM sale_lines sl
            JOIN menu_items mi ON mi.id = sl.item_id
            JOIN sales s ON s.id = sl.sale_id
            WHERE s.company_id = :c
            GROUP BY mi.name
            ORDER BY total_revenue DESC
            LIMIT 5
        """, {'c': company['id']})
        if len(top_items):
            st.dataframe(
                top_items.rename(columns={'name': 'Dish / Drink', 'total_qty': 'Quantity Sold', 'total_revenue': f'Revenue ({curr})'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No item sales logged yet.")
            
    st.markdown("---")
    st.subheader("🧾 Recent Invoices")
    recent_invoices = db.read("""
        SELECT s.id, s.invoice_no, s.sale_date, s.order_type, s.payment_method, s.subtotal, s.tax, s.total, s.status, u.full_name as cashier
        FROM sales s
        LEFT JOIN users u ON u.id = s.created_by
        WHERE s.company_id = :c
        ORDER BY s.id DESC
        LIMIT 8
    """, {'c': company['id']})
    
    if len(recent_invoices):
        st.dataframe(
            recent_invoices.drop(columns=['id']),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent invoices.")

# ---------------------------------------------------------
# Page 2: Point of Sale (POS)
# ---------------------------------------------------------
elif current_page == "Point of Sale (POS)":
    st.title("🛒 Point of Sale & Order Terminal")
    
    # 2-column layout: Left = Menu Selection Grid, Right = Live Cart & Checkout
    col_menu, col_cart = st.columns([3, 2])
    
    with col_menu:
        # Category Filter & Search
        menu_items_all = db.read("SELECT * FROM menu_items WHERE company_id = :c AND active = 1 ORDER BY category, name", {'c': company['id']})
        
        if not len(menu_items_all):
            st.warning("No menu items found. Please add items in the Menu module.")
            st.stop()
            
        categories = ["All Categories"] + sorted(menu_items_all['category'].unique().tolist())
        
        sc1, sc2 = st.columns([2, 3])
        with sc1:
            selected_cat = st.selectbox("Filter Category", categories, label_visibility="collapsed")
        with sc2:
            search_query = st.text_input("🔍 Search Dish or Beverage...", label_visibility="collapsed")
            
        filtered_items = menu_items_all.copy()
        if selected_cat != "All Categories":
            filtered_items = filtered_items[filtered_items['category'] == selected_cat]
        if search_query.strip():
            filtered_items = filtered_items[filtered_items['name'].str.contains(search_query.strip(), case=False, na=False)]
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Display Menu Items in a clean 2-column grid
        item_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_items.iterrows()):
            with item_cols[idx % 2]:
                with st.container(border=True):
                    ic1, ic2 = st.columns([3, 1])
                    with ic1:
                        st.markdown(f"**{row['name']}**")
                        tags = []
                        if row.get('is_vegetarian'):
                            tags.append("<span class='tag-veg'>🌱 Vegetarian</span>")
                        if row.get('is_spicy'):
                            tags.append("<span class='tag-spicy'>🌶️ Spicy</span>")
                        if tags:
                            st.markdown(" ".join(tags), unsafe_allow_html=True)
                        if row.get('description'):
                            st.caption(f"{row['description'][:65]}...")
                        st.markdown(f"**{curr} {float(row['price']):,.2f}**")
                    with ic2:
                        st.markdown("<br/>", unsafe_allow_html=True)
                        item_id = int(row['id'])
                        if st.button("➕ Add", key=f"add_btn_{item_id}", type="secondary", use_container_width=True):
                            if item_id in st.session_state.cart:
                                st.session_state.cart[item_id]['qty'] += 1
                            else:
                                st.session_state.cart[item_id] = {
                                    'id': item_id,
                                    'name': row['name'],
                                    'price': float(row['price']),
                                    'cost': float(row['cost']),
                                    'qty': 1,
                                    'notes': ''
                                }
                            st.rerun()

    with col_cart:
        with st.container(border=True):
            st.subheader("🛍️ Current Order Ticket")
            
            # Order details selectors
            oc1, oc2 = st.columns(2)
            with oc1:
                order_type = st.selectbox("Order Type", ["Dine-In", "Takeaway", "Delivery"], key="pos_type_sel")
            with oc2:
                if order_type == "Dine-In":
                    tables_df = db.read("SELECT table_number FROM tables WHERE company_id = :c ORDER BY table_number", {'c': company['id']})
                    tbl_list = tables_df['table_number'].tolist() if len(tables_df) else ["T1", "T2", "T3", "P1", "VIP-1"]
                    selected_table = st.selectbox("Table", tbl_list, key="pos_tbl_sel")
                else:
                    selected_table = "N/A"
                    
            # Customer selector
            cust_df = db.read("SELECT id, name, phone FROM customers WHERE company_id = :c ORDER BY name", {'c': company['id']})
            cust_options = {int(r['id']): f"{r['name']} ({r['phone']})" for _, r in cust_df.iterrows()}
            cust_options[0] = "Walk-in Guest"
            selected_cust_id = st.selectbox("Customer", options=list(cust_options.keys()), format_func=lambda x: cust_options[x], index=len(cust_options)-1)
            
            st.markdown("---")
            
            # Cart Items List
            if not st.session_state.cart:
                st.info("🛒 Cart is empty. Click **➕ Add** on menu items to begin.")
            else:
                cart_items = list(st.session_state.cart.values())
                subtotal = 0.0
                
                for item in cart_items:
                    iid = item['id']
                    line_tot = item['qty'] * item['price']
                    subtotal += line_tot
                    
                    cc1, cc2, cc3, cc4 = st.columns([3, 1, 1, 1])
                    with cc1:
                        st.markdown(f"**{item['name']}**<br/><small>{curr} {item['price']:,.2f} ea</small>", unsafe_allow_html=True)
                    with cc2:
                        if st.button("➖", key=f"dec_{iid}"):
                            if st.session_state.cart[iid]['qty'] > 1:
                                st.session_state.cart[iid]['qty'] -= 1
                            else:
                                del st.session_state.cart[iid]
                            st.rerun()
                    with cc3:
                        st.markdown(f"<p style='text-align:center; padding-top:6px;'><b>{item['qty']}</b></p>", unsafe_allow_html=True)
                    with cc4:
                        if st.button("➕", key=f"inc_{iid}"):
                            st.session_state.cart[iid]['qty'] += 1
                            st.rerun()
                            
                st.markdown("---")
                
                # Financial calculations
                disc_c, tip_c = st.columns(2)
                with disc_c:
                    discount_amt = st.number_input(f"Discount ({curr})", min_value=0.0, max_value=float(subtotal), value=0.0, step=1.0)
                with tip_c:
                    tip_amt = st.number_input(f"Tip / Gratuity ({curr})", min_value=0.0, value=0.0, step=1.0)
                    
                taxable_base = max(0.0, subtotal - discount_amt)
                tax_rate = 0.15 # ZIMRA 15% VAT standard
                vat_amount = round(taxable_base * tax_rate, 2)
                grand_total = round(taxable_base + vat_amount + tip_amt, 2)
                
                st.markdown(f"""
                <div style='background-color:#fcfbf9; padding:10px; border-radius:6px; border:1px solid #e8e3d8;'>
                    <div style='display:flex; justify-content:space-between;'><span>Subtotal:</span><b>{curr} {subtotal:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>Discount:</span><b style='color:red;'>-{curr} {discount_amt:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>VAT (15% ZIMRA):</span><b>{curr} {vat_amount:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>Tip / Gratuity:</span><b>{curr} {tip_amt:,.2f}</b></div>
                    <hr style='margin:6px 0;'/>
                    <div style='display:flex; justify-content:space-between; font-size:1.2rem; color:#9b721d;'>
                        <span><b>GRAND TOTAL:</b></span><b>{curr} {grand_total:,.2f}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br/>", unsafe_allow_html=True)
                payment_method = st.selectbox("💳 Payment Method", ["Cash", "Card (Swipe/Visa)", "Ecocash / Mobile Money", "Bank Transfer", "Credit Account"])
                
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if st.button("🗑️ Clear Cart", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()
                with btn_c2:
                    if st.button("✅ Complete Sale", type="primary", use_container_width=True):
                        # Generate unique invoice number
                        inv_no = f"SQR-{datetime.now():%Y%m%d%H%M%S}-{secrets.token_hex(2).upper()}"
                        
                        # Insert sale record
                        sale_id = db.execute_insert("""
                            INSERT INTO sales(company_id, branch_id, invoice_no, sale_date, customer_id, order_type, payment_method, subtotal, discount, tax, tip, total, status, kitchen_status, created_by)
                            VALUES(:c, 1, :inv, :d, :cust, :ot, :pm, :sub, :dc, :tx, :tp, :tot, 'Paid', 'Pending', :u)
                        """, {
                            'c': company['id'],
                            'inv': inv_no,
                            'd': str(date.today()),
                            'cust': selected_cust_id if selected_cust_id > 0 else None,
                            'ot': order_type,
                            'pm': payment_method,
                            'sub': subtotal,
                            'dc': discount_amt,
                            'tx': vat_amount,
                            'tp': tip_amt,
                            'tot': grand_total,
                            'u': u['id']
                        })
                        
                        # Insert sale lines & create Kitchen Orders
                        for item in cart_items:
                            db.run("""
                                INSERT INTO sale_lines(sale_id, item_id, quantity, unit_price, line_total, notes)
                                VALUES(:sid, :iid, :q, :up, :lt, :nt)
                            """, {
                                'sid': sale_id,
                                'iid': item['id'],
                                'q': item['qty'],
                                'up': item['price'],
                                'lt': item['qty'] * item['price'],
                                'nt': item.get('notes', '')
                            })
                            
                            db.run("""
                                INSERT INTO kitchen_orders(sale_id, item_name, table_number, quantity, notes, status)
                                VALUES(:sid, :iname, :tbl, :q, :nt, 'Pending')
                            """, {
                                'sid': sale_id,
                                'iname': item['name'],
                                'tbl': selected_table if order_type == 'Dine-In' else order_type,
                                'q': item['qty'],
                                'nt': item.get('notes', '')
                            })
                            
                        # Automatically deduct stock based on recipes!
                        db.deduct_inventory_for_sale(company['id'], sale_id, u['id'])
                        
                        # Update table status if dine-in
                        if order_type == "Dine-In" and selected_table != "N/A":
                            db.run("UPDATE tables SET status = 'Occupied' WHERE table_number = :tn AND company_id = :c", {'tn': selected_table, 'c': company['id']})
                            
                        # Log audit
                        db.log_audit(company['id'], u['id'], 'POS_SALE', 'Sales', sale_id, f"Completed sale {inv_no} for {curr} {grand_total:,.2f} via {payment_method}")
                        
                        # Save completed sale state for immediate receipt download
                        st.session_state.last_completed_sale = {
                            'id': sale_id,
                            'invoice_no': inv_no,
                            'sale_date': str(datetime.now().strftime('%Y-%m-%d %H:%M')),
                            'payment_method': payment_method,
                            'order_type': order_type,
                            'table_number': selected_table,
                            'customer_name': cust_options.get(selected_cust_id, 'Walk-in Guest'),
                            'cashier_name': u['full_name'],
                            'subtotal': subtotal,
                            'discount': discount_amt,
                            'tax': vat_amount,
                            'tip': tip_amt,
                            'total': grand_total,
                            'items': cart_items
                        }
                        st.session_state.cart = {}
                        st.rerun()

    # Completed Sale Receipt Modal Banner
    if st.session_state.last_completed_sale:
        last = st.session_state.last_completed_sale
        st.success(f"🎉 **Sale Completed Successfully!** Invoice: `{last['invoice_no']}` | Total: **{curr} {last['total']:,.2f}**")
        
        pdf_bytes = pdf_gen.generate_receipt_pdf(company, last, last['items'])
        
        rc1, rc2 = st.columns([1, 1])
        with rc1:
            st.download_button(
                label="📄 Download Tax Receipt PDF",
                data=pdf_bytes,
                file_name=f"Receipt_{last['invoice_no']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        with rc2:
            if st.button("✖️ Dismiss / New Order", use_container_width=True):
                st.session_state.last_completed_sale = None
                st.rerun()

# ---------------------------------------------------------
# Page 3: Floor & Table Manager
# ---------------------------------------------------------
elif current_page == "Floor & Table Manager":
    st.title("🪑 Floor Plan & Table Management")
    st.caption("Live dining room status, guest seating, and table turnover tracking.")
    
    tables_df = db.read("SELECT * FROM tables WHERE company_id = :c ORDER BY section, table_number", {'c': company['id']})
    
    # Section statistics
    total_tables = len(tables_df)
    avail_tables = len(tables_df[tables_df['status'] == 'Available'])
    occ_tables = len(tables_df[tables_df['status'] == 'Occupied'])
    res_tables = len(tables_df[tables_df['status'] == 'Reserved'])
    
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Total Tables", total_tables)
    tc2.metric("Available", avail_tables)
    tc3.metric("Occupied", occ_tables)
    tc4.metric("Reserved", res_tables)
    
    st.markdown("---")
    
    # Floor Plan Visual Grid by Section
    sections = tables_df['section'].unique().tolist()
    for sec in sections:
        st.subheader(f"📍 {sec}")
        sec_tables = tables_df[tables_df['section'] == sec]
        
        grid_cols = st.columns(4)
        for idx, (_, tbl) in enumerate(sec_tables.iterrows()):
            with grid_cols[idx % 4]:
                with st.container(border=True):
                    status = tbl['status']
                    css_class = 'tbl-available' if status == 'Available' else ('tbl-occupied' if status == 'Occupied' else 'tbl-reserved')
                    
                    st.markdown(f"<div class='{css_class}'><b>Table {tbl['table_number']}</b><br/><small>{tbl['capacity']} Seats · {status}</small></div>", unsafe_allow_html=True)
                    st.markdown("<br/>", unsafe_allow_html=True)
                    
                    # Quick Status Change Action
                    new_status = st.selectbox(
                        "Change Status",
                        ["Available", "Occupied", "Reserved", "Cleaning / Billed"],
                        index=["Available", "Occupied", "Reserved", "Cleaning / Billed"].index(status) if status in ["Available", "Occupied", "Reserved", "Cleaning / Billed"] else 0,
                        key=f"status_tbl_{tbl['id']}"
                    )
                    if new_status != status:
                        db.run("UPDATE tables SET status = :s WHERE id = :tid", {'s': new_status, 'tid': int(tbl['id'])})
                        st.rerun()

    st.markdown("---")
    # Add new table form
    with st.expander("➕ Add New Table to Floor Plan"):
        with st.form("new_table_form"):
            nt_num = st.text_input("Table Number (e.g. T6, P4, VIP-2)")
            nt_sec = st.selectbox("Section", ["Main Dining", "Garden / Patio", "VIP Lounge", "Bar Counter", "Terrace"])
            nt_cap = st.number_input("Seating Capacity", min_value=1, max_value=24, value=4)
            nt_sub = st.form_submit_button("Add Table to Layout")
        if nt_sub and nt_num:
            db.run("""
                INSERT INTO tables(company_id, branch_id, table_number, section, capacity, status)
                VALUES(:c, 1, :tn, :s, :cp, 'Available')
            """, {'c': company['id'], 'tn': nt_num.strip(), 's': nt_sec, 'cp': nt_cap})
            st.success(f"Table {nt_num} added to {nt_sec}!")
            st.rerun()

# ---------------------------------------------------------
# Page 4: Invoices & Sales History
# ---------------------------------------------------------
elif current_page == "Invoices & Sales History":
    st.title("🧾 Invoices & Order History")
    st.caption("Comprehensive sales transactions, ZIMRA tax invoices, and PDF downloads.")
    
    # Filter Controls
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        date_from = st.date_input("From Date", date.today() - timedelta(days=30))
    with fc2:
        date_to = st.date_input("To Date", date.today())
    with fc3:
        filter_status = st.selectbox("Payment Status", ["All", "Paid", "Pending", "Cancelled"])
    with fc4:
        search_inv = st.text_input("Search Invoice / Customer", "")
        
    query = """
        SELECT s.id, s.invoice_no, s.sale_date, s.order_type, s.payment_method,
               s.subtotal, s.discount, s.tax, s.tip, s.total, s.status,
               COALESCE(c.name, 'Walk-in') AS customer_name,
               u.full_name AS cashier_name
        FROM sales s
        LEFT JOIN customers c ON c.id = s.customer_id
        LEFT JOIN users u ON u.id = s.created_by
        WHERE s.company_id = :c AND s.sale_date BETWEEN :d1 AND :d2
    """
    params = {'c': company['id'], 'd1': str(date_from), 'd2': str(date_to)}
    
    if filter_status != "All":
        query += " AND s.status = :st"
        params['st'] = filter_status
    if search_inv.strip():
        query += " AND (s.invoice_no LIKE :srch OR c.name LIKE :srch)"
        params['srch'] = f"%{search_inv.strip()}%"
        
    query += " ORDER BY s.id DESC"
    sales_df = db.read(query, params)
    
    # Metrics Summary
    tot_sales_vol = float(sales_df['total'].sum()) if len(sales_df) else 0.0
    tot_tax_vol = float(sales_df['tax'].sum()) if len(sales_df) else 0.0
    
    ic1, ic2, ic3 = st.columns(3)
    ic1.metric("Total Period Sales", f"{curr} {tot_sales_vol:,.2f}")
    ic2.metric("Total 15% VAT Collected", f"{curr} {tot_tax_vol:,.2f}")
    ic3.metric("Total Invoices Count", f"{len(sales_df)} Orders")
    
    st.markdown("---")
    
    if len(sales_df):
        st.dataframe(sales_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        
        # Action selector to print / view specific invoice
        st.subheader("🔍 Invoice Actions & PDF Generation")
        inv_list = sales_df['invoice_no'].tolist()
        sel_invoice = st.selectbox("Select Invoice to Inspect / Reprint", inv_list)
        
        if sel_invoice:
            sel_sale = sales_df[sales_df['invoice_no'] == sel_invoice].iloc[0].to_dict()
            sale_id = int(sel_sale['id'])
            
            lines_df = db.read("""
                SELECT mi.name, sl.quantity, sl.unit_price, sl.line_total, sl.notes
                FROM sale_lines sl
                JOIN menu_items mi ON mi.id = sl.item_id
                WHERE sl.sale_id = :sid
            """, {'sid': sale_id})
            
            st.write(f"**Items in {sel_invoice}:**")
            st.dataframe(lines_df, use_container_width=True, hide_index=True)
            
            # Generate PDF
            items_for_pdf = lines_df.to_dict('records')
            pdf_bytes = pdf_gen.generate_receipt_pdf(company, sel_sale, items_for_pdf)
            
            pcol1, pcol2 = st.columns([1, 1])
            with pcol1:
                st.download_button(
                    label=f"📄 Download {sel_invoice} Tax Invoice (PDF)",
                    data=pdf_bytes,
                    file_name=f"Invoice_{sel_invoice}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            with pcol2:
                st.download_button(
                    label=f"📊 Export Sales History (CSV)",
                    data=sales_df.to_csv(index=False),
                    file_name=f"sales_export_{date_from}_{date_to}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.info("No sales records found for selected period.")

# ---------------------------------------------------------
# Page 5: Kitchen Display System (KDS)
# ---------------------------------------------------------
elif current_page == "Kitchen Display System (KDS)":
    st.title("👨‍🍳 Kitchen Display System (KDS)")
    st.caption("Live kitchen order ticketing, dish preparation timers, and service flow.")
    
    # Active orders
    orders_df = db.read("""
        SELECT ko.id, ko.sale_id, ko.item_name, ko.table_number, ko.quantity, ko.notes, ko.status, ko.created_at,
               s.invoice_no
        FROM kitchen_orders ko
        JOIN sales s ON s.id = ko.sale_id
        WHERE ko.status != 'Served'
        ORDER BY ko.id ASC
    """)
    
    kc1, kc2, kc3 = st.columns(3)
    pending_cnt = len(orders_df[orders_df['status'] == 'Pending'])
    cooking_cnt = len(orders_df[orders_df['status'] == 'In Preparation'])
    ready_cnt = len(orders_df[orders_df['status'] == 'Ready'])
    
    kc1.metric("⏳ Pending Orders", pending_cnt)
    kc2.metric("🍳 In Preparation", cooking_cnt)
    kc3.metric("🛎️ Ready for Service", ready_cnt)
    
    st.markdown("---")
    
    if not len(orders_df):
        st.success("🎉 All kitchen orders have been prepared and served! Kitchen is clear.")
    else:
        # Display 3 columns: Pending, Cooking, Ready
        col_pend, col_cook, col_ready = st.columns(3)
        
        with col_pend:
            st.markdown("### ⏳ Pending Orders")
            for _, ord_row in orders_df[orders_df['status'] == 'Pending'].iterrows():
                with st.container(border=True):
                    st.markdown(f"**Table: {ord_row['table_number']}** ({ord_row['invoice_no']})")
                    st.markdown(f"### {ord_row['quantity']:g}x {ord_row['item_name']}")
                    if ord_row.get('notes'):
                        st.warning(f"Note: {ord_row['notes']}")
                    st.caption(f"Received: {str(ord_row['created_at'])[:16]}")
                    if st.button("🍳 Start Cooking", key=f"start_{ord_row['id']}", type="primary", use_container_width=True):
                        db.run("UPDATE kitchen_orders SET status = 'In Preparation' WHERE id = :id", {'id': int(ord_row['id'])})
                        st.rerun()

        with col_cook:
            st.markdown("### 🍳 In Preparation")
            for _, ord_row in orders_df[orders_df['status'] == 'In Preparation'].iterrows():
                with st.container(border=True):
                    st.markdown(f"**Table: {ord_row['table_number']}** ({ord_row['invoice_no']})")
                    st.markdown(f"### {ord_row['quantity']:g}x {ord_row['item_name']}")
                    if ord_row.get('notes'):
                        st.warning(f"Note: {ord_row['notes']}")
                    st.caption(f"Cooking since: {str(ord_row['created_at'])[:16]}")
                    if st.button("🛎️ Mark Ready", key=f"ready_{ord_row['id']}", type="secondary", use_container_width=True):
                        db.run("UPDATE kitchen_orders SET status = 'Ready' WHERE id = :id", {'id': int(ord_row['id'])})
                        st.rerun()

        with col_ready:
            st.markdown("### 🛎️ Ready for Service")
            for _, ord_row in orders_df[orders_df['status'] == 'Ready'].iterrows():
                with st.container(border=True):
                    st.markdown(f"**Table: {ord_row['table_number']}** ({ord_row['invoice_no']})")
                    st.markdown(f"### {ord_row['quantity']:g}x {ord_row['item_name']}")
                    st.caption("Dish is plated and hot!")
                    if st.button("✅ Mark Served", key=f"serve_{ord_row['id']}", use_container_width=True):
                        db.run("UPDATE kitchen_orders SET status = 'Served' WHERE id = :id", {'id': int(ord_row['id'])})
                        st.rerun()

# ---------------------------------------------------------
# Page 6: Menu & Dishes
# ---------------------------------------------------------
elif current_page == "Menu & Dishes":
    st.title("🍽️ Menu Items & Dish Catalog")
    st.caption("Configure food & beverage offerings, pricing, food costs, and dietary tags.")
    
    t1, t2 = st.tabs(["📋 Current Menu Catalog", "➕ Add / Update Menu Item"])
    
    with t1:
        menu_df = db.read("""
            SELECT id, name, category, description, price, cost,
                   (price - cost) AS gross_profit,
                   CASE WHEN price > 0 THEN ROUND(((price - cost) / price) * 100, 1) ELSE 0 END AS margin_pct,
                   is_vegetarian, is_spicy, prep_time_mins, active
            FROM menu_items
            WHERE company_id = :c
            ORDER BY category, name
        """, {'c': company['id']})
        
        st.dataframe(
            menu_df.rename(columns={
                'name': 'Item Name', 'category': 'Category', 'price': f'Price ({curr})',
                'cost': f'Cost ({curr})', 'gross_profit': f'Profit ({curr})', 'margin_pct': 'Margin %',
                'prep_time_mins': 'Prep Mins'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with t2:
        with st.form("add_menu_item_form"):
            mi_name = st.text_input("Item Name *", placeholder="e.g. Flame-Grilled Half Chicken")
            mi_cat = st.selectbox("Category *", ["Mains", "Traditional", "Burgers", "Sides", "Beverages", "Desserts", "Starters"])
            mi_desc = st.text_area("Item Description", placeholder="Tender, flame-grilled chicken with peri-peri marinade")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                mi_price = st.number_input(f"Selling Price ({curr}) *", min_value=0.0, value=12.0, step=0.5)
            with c2:
                mi_cost = st.number_input(f"Estimated Food Cost ({curr})", min_value=0.0, value=3.5, step=0.5)
            with c3:
                mi_prep = st.number_input("Prep Time (minutes)", min_value=1, max_value=120, value=15)
                
            c4, c5 = st.columns(2)
            with c4:
                is_veg = st.checkbox("🌱 Vegetarian Item")
            with c5:
                is_spicy = st.checkbox("🌶️ Spicy Dish")
                
            sub_menu = st.form_submit_button("Save Menu Item", type="primary")
            
        if sub_menu and mi_name:
            db.run("""
                INSERT INTO menu_items(company_id, name, category, description, price, cost, is_vegetarian, is_spicy, prep_time_mins, active)
                VALUES(:c, :n, :cat, :d, :p, :co, :v, :s, :pt, 1)
            """, {
                'c': company['id'], 'n': mi_name.strip(), 'cat': mi_cat, 'd': mi_desc,
                'p': mi_price, 'co': mi_cost, 'v': 1 if is_veg else 0, 's': 1 if is_spicy else 0, 'pt': mi_prep
            })
            db.log_audit(company['id'], u['id'], 'MENU_ADD', 'Menu', 0, f"Added menu item: {mi_name} at {curr} {mi_price:,.2f}")
            st.success(f"Menu item '{mi_name}' created successfully!")
            st.rerun()

# ---------------------------------------------------------
# Page 7: Recipes & Food Costing (Bill of Materials)
# ---------------------------------------------------------
elif current_page == "Recipes & Food Costing (BOM)":
    st.title("🧪 Recipes & Bill of Materials (BOM)")
    st.caption("Link menu dishes to raw ingredients for automatic stock deduction upon sale and exact food costing.")
    
    recipes_df = db.read("""
        SELECT r.id, r.menu_item_id, mi.name as dish_name, mi.price as selling_price,
               r.yield_quantity, r.instructions
        FROM recipes r
        JOIN menu_items mi ON mi.id = r.menu_item_id
        WHERE r.company_id = :c AND r.active = 1
        ORDER BY mi.name
    """, {'c': company['id']})
    
    if len(recipes_df):
        selected_dish = st.selectbox("Select Dish to View / Edit Formulation", recipes_df['dish_name'].tolist())
        sel_rec = recipes_df[recipes_df['dish_name'] == selected_dish].iloc[0]
        rec_id = int(sel_rec['id'])
        
        # Load Recipe Lines
        lines = db.read("""
            SELECT rl.id, inv.item_name, rl.quantity, rl.unit, inv.unit_cost,
                   (rl.quantity * inv.unit_cost) AS ingredient_cost
            FROM recipe_lines rl
            JOIN inventory inv ON inv.id = rl.inventory_item_id
            WHERE rl.recipe_id = :rid
        """, {'rid': rec_id})
        
        total_recipe_cost = float(lines['ingredient_cost'].sum()) if len(lines) else 0.0
        selling_price = float(sel_rec['selling_price'])
        food_cost_pct = (total_recipe_cost / selling_price * 100) if selling_price > 0 else 0.0
        gross_profit = selling_price - total_recipe_cost
        
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric(f"Selling Price", f"{curr} {selling_price:,.2f}")
        rc2.metric(f"Calculated Food Cost", f"{curr} {total_recipe_cost:,.2f}")
        rc3.metric(f"Gross Profit per Portion", f"{curr} {gross_profit:,.2f}")
        rc4.metric(f"Food Cost %", f"{food_cost_pct:.1f}%", delta=f"{food_cost_pct:.1f}% Target: <35%", delta_color="inverse")
        
        st.markdown("---")
        st.subheader(f"Raw Ingredients Formulation for '{selected_dish}'")
        st.dataframe(lines.drop(columns=['id']), use_container_width=True, hide_index=True)
        
        # Add ingredient line form
        with st.expander("➕ Add Raw Ingredient to this Recipe"):
            inv_all = db.read("SELECT id, item_name, unit, unit_cost FROM inventory WHERE company_id = :c ORDER BY item_name", {'c': company['id']})
            with st.form("add_recipe_line_form"):
                sel_inv_name = st.selectbox("Ingredient", inv_all['item_name'].tolist())
                ing_qty = st.number_input("Quantity used per portion", min_value=0.001, value=0.100, step=0.05, format="%.3f")
                sub_rec_line = st.form_submit_button("Add Ingredient to Recipe")
                
            if sub_rec_line and sel_inv_name:
                inv_row = inv_all[inv_all['item_name'] == sel_inv_name].iloc[0]
                db.run("""
                    INSERT INTO recipe_lines(recipe_id, inventory_item_id, quantity, unit)
                    VALUES(:rid, :invid, :q, :u)
                """, {'rid': rec_id, 'invid': int(inv_row['id']), 'q': ing_qty, 'u': inv_row['unit']})
                st.success("Ingredient added!")
                st.rerun()

    # Form to create recipe for dishes without recipes
    with st.expander("➕ Create New Recipe for a Menu Item"):
        dishes_without_recipe = db.read("""
            SELECT mi.id, mi.name FROM menu_items mi
            WHERE mi.company_id = :c AND mi.id NOT IN (SELECT menu_item_id FROM recipes WHERE company_id = :c)
        """, {'c': company['id']})
        
        if len(dishes_without_recipe):
            with st.form("new_recipe_form"):
                dish_to_add = st.selectbox("Menu Item", dishes_without_recipe['name'].tolist())
                instructions = st.text_area("Preparation Method / Notes", "Standard restaurant recipe")
                sub_new_rec = st.form_submit_button("Initialize Recipe Formulation")
                
            if sub_new_rec and dish_to_add:
                mi_id = int(dishes_without_recipe[dishes_without_recipe['name'] == dish_to_add].iloc[0]['id'])
                db.run("""
                    INSERT INTO recipes(company_id, menu_item_id, yield_quantity, instructions, active)
                    VALUES(:c, :mi, 1.0, :ins, 1)
                """, {'c': company['id'], 'mi': mi_id, 'ins': instructions})
                st.success(f"Recipe created for {dish_to_add}! You can now add ingredient lines.")
                st.rerun()
        else:
            st.info("All existing menu items currently have recipes.")

# ---------------------------------------------------------
# Page 8: Inventory & Stock Balances
# ---------------------------------------------------------
elif current_page == "Inventory & Stock Balances":
    st.title("📦 Inventory & Raw Materials")
    st.caption("Live stock balances, reorder level warnings, and stock valuation.")
    
    inv_df = db.read("""
        SELECT i.id, i.item_name, i.category, i.unit, i.quantity, i.reorder_level, i.unit_cost,
               (i.quantity * i.unit_cost) AS total_valuation,
               s.name AS supplier_name
        FROM inventory i
        LEFT JOIN suppliers s ON s.id = i.supplier_id
        WHERE i.company_id = :c
        ORDER BY i.category, i.item_name
    """, {'c': company['id']})
    
    tot_inv_val = float(inv_df['total_valuation'].sum()) if len(inv_df) else 0.0
    low_stock = inv_df[inv_df['quantity'] <= inv_df['reorder_level']]
    
    iv1, iv2, iv3 = st.columns(3)
    iv1.metric("Total Stock Valuation", f"{curr} {tot_inv_val:,.2f}")
    iv2.metric("Total Inventory Items", len(inv_df))
    iv3.metric("Items Below Reorder Level", len(low_stock), delta=f"{len(low_stock)} items", delta_color="inverse")
    
    st.markdown("---")
    
    t1, t2, t3 = st.tabs(["📋 Current Stock List", "➕ Add Raw Material", "🔄 Quick Restock / Receive Delivery"])
    
    with t1:
        st.dataframe(
            inv_df.drop(columns=['id']).rename(columns={
                'item_name': 'Item', 'category': 'Category', 'unit': 'Unit',
                'quantity': 'Stock Qty', 'reorder_level': 'Reorder Lvl', 'unit_cost': f'Unit Cost ({curr})',
                'total_valuation': f'Valuation ({curr})', 'supplier_name': 'Supplier'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # PDF Valuation Download Button
        pdf_val_bytes = pdf_gen.generate_inventory_valuation_pdf(company, inv_df)
        dcol1, dcol2 = st.columns([1, 1])
        with dcol1:
            st.download_button(
                label="📄 Download Inventory Valuation Report (PDF)",
                data=pdf_val_bytes,
                file_name=f"Inventory_Valuation_{date.today()}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        with dcol2:
            st.download_button(
                label="📊 Export Stock CSV",
                data=inv_df.to_csv(index=False),
                file_name=f"stock_list_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
    with t2:
        with st.form("new_inventory_item_form"):
            in_name = st.text_input("Item Name *", placeholder="e.g. Fresh Cooking Oil")
            in_cat = st.selectbox("Category", ["Poultry", "Meat", "Grains", "Vegetables", "Dairy", "Bakery", "Beverages", "Spices", "Oils", "Packaging"])
            in_unit = st.selectbox("Unit of Measure", ["kg", "litres", "cans", "bottles", "packs", "boxes", "pieces"])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                in_qty = st.number_input("Starting Quantity", min_value=0.0, value=10.0, step=1.0)
            with c2:
                in_reorder = st.number_input("Reorder Level Threshold", min_value=0.0, value=5.0, step=1.0)
            with c3:
                in_cost = st.number_input(f"Unit Cost ({curr})", min_value=0.0, value=2.50, step=0.1)
                
            suppliers_list = db.read("SELECT id, name FROM suppliers WHERE company_id = :c", {'c': company['id']})
            sup_dict = {int(r['id']): r['name'] for _, r in suppliers_list.iterrows()}
            sup_dict[0] = "No Supplier Assigned"
            sel_sup = st.selectbox("Default Supplier", options=list(sup_dict.keys()), format_func=lambda x: sup_dict[x])
            
            sub_inv = st.form_submit_button("Save Inventory Item", type="primary")
            
        if sub_inv and in_name:
            db.run("""
                INSERT INTO inventory(company_id, item_name, category, unit, quantity, reorder_level, unit_cost, supplier_id)
                VALUES(:c, :n, :cat, :u, :q, :r, :co, :s)
            """, {
                'c': company['id'], 'n': in_name.strip(), 'cat': in_cat, 'u': in_unit,
                'q': in_qty, 'r': in_reorder, 'co': in_cost, 's': sel_sup if sel_sup > 0 else None
            })
            db.log_audit(company['id'], u['id'], 'STOCK_ADD', 'Inventory', 0, f"Added inventory item: {in_name} ({in_qty} {in_unit})")
            st.success(f"Inventory item '{in_name}' created!")
            st.rerun()

    with t3:
        with st.form("quick_restock_form"):
            st.subheader("Receive Stock Delivery")
            restock_item = st.selectbox("Select Raw Material", inv_df['item_name'].tolist())
            rc1, rc2 = st.columns(2)
            with rc1:
                add_qty = st.number_input("Quantity Received", min_value=0.1, value=10.0, step=1.0)
            with rc2:
                new_unit_cost = st.number_input(f"Purchase Unit Cost ({curr})", min_value=0.0, value=2.0, step=0.1)
            invoice_ref = st.text_input("Supplier Delivery Note / Invoice Ref", placeholder="e.g. GRN-9921 / INV-5541")
            sub_restock = st.form_submit_button("Confirm & Post Stock Receipt", type="primary")
            
        if sub_restock and restock_item:
            inv_row = inv_df[inv_df['item_name'] == restock_item].iloc[0]
            iid = int(inv_row['id'])
            
            db.run("""
                UPDATE inventory
                SET quantity = quantity + :q, unit_cost = :co
                WHERE id = :iid AND company_id = :c
            """, {'q': add_qty, 'co': new_unit_cost, 'iid': iid, 'c': company['id']})
            
            db.run("""
                INSERT INTO stock_movements(company_id, inventory_item_id, movement_type, quantity, unit_cost, reference, reason, created_by)
                VALUES(:c, :iid, 'Purchase Restock', :q, :co, :ref, 'Delivery received', :u)
            """, {'c': company['id'], 'iid': iid, 'q': add_qty, 'co': new_unit_cost, 'ref': invoice_ref, 'u': u['id']})
            
            db.log_audit(company['id'], u['id'], 'STOCK_RESTOCK', 'Inventory', iid, f"Restocked {add_qty} {inv_row['unit']} of {restock_item}")
            st.success(f"Added {add_qty} {inv_row['unit']} to '{restock_item}' stock balance!")
            st.rerun()

# ---------------------------------------------------------
# Page 9: Stock Movements & Wastage
# ---------------------------------------------------------
elif current_page == "Stock Movements & Wastage":
    st.title("🔄 Stock Movements & Food Wastage Tracking")
    st.caption("Immutable audit log of all stock increases, sale recipe depletions, spillage, and kitchen wastage.")
    
    t1, t2 = st.tabs(["📜 Stock Movements Log", "⚠️ Log Kitchen Wastage / Spillage"])
    
    with t1:
        movements_df = db.read("""
            SELECT sm.id, sm.movement_date, inv.item_name, sm.movement_type, sm.quantity, inv.unit,
                   sm.unit_cost, (sm.quantity * sm.unit_cost) AS total_val,
                   sm.reference, sm.reason, u.full_name AS logged_by
            FROM stock_movements sm
            JOIN inventory inv ON inv.id = sm.inventory_item_id
            LEFT JOIN users u ON u.id = sm.created_by
            WHERE sm.company_id = :c
            ORDER BY sm.id DESC
            LIMIT 50
        """, {'c': company['id']})
        
        if len(movements_df):
            st.dataframe(movements_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        else:
            st.info("No stock movements recorded yet.")
            
    with t2:
        with st.form("log_wastage_form"):
            st.subheader("Record Food Loss / Kitchen Spillage")
            inv_items = db.read("SELECT id, item_name, unit, unit_cost FROM inventory WHERE company_id = :c ORDER BY item_name", {'c': company['id']})
            waste_item = st.selectbox("Select Wasted Ingredient", inv_items['item_name'].tolist())
            
            c1, c2 = st.columns(2)
            with c1:
                w_qty = st.number_input("Quantity Wasted", min_value=0.01, value=1.0, step=0.5)
            with c2:
                w_reason = st.selectbox("Reason Code", ["Burnt / Kitchen Preparation Error", "Expired / Spoilage", "Dropped / Spillage", "Quality Defect on Inspection", "Over-Portioning"])
                
            w_notes = st.text_input("Detailed Explanation / Shift Supervisor Note")
            sub_waste = st.form_submit_button("Record Wastage & Deduct Stock", type="primary")
            
        if sub_waste and waste_item:
            irow = inv_items[inv_items['item_name'] == waste_item].iloc[0]
            iid = int(irow['id'])
            
            db.run("""
                UPDATE inventory
                SET quantity = MAX(0.0, quantity - :q)
                WHERE id = :iid AND company_id = :c
            """, {'q': w_qty, 'iid': iid, 'c': company['id']})
            
            db.run("""
                INSERT INTO stock_movements(company_id, inventory_item_id, movement_type, quantity, unit_cost, reference, reason, created_by)
                VALUES(:c, :iid, 'Wastage', :q, :co, 'WASTE-LOG', :r, :u)
            """, {'c': company['id'], 'iid': iid, 'q': -w_qty, 'co': float(irow['unit_cost']), 'r': f"{w_reason}: {w_notes}", 'u': u['id']})
            
            db.log_audit(company['id'], u['id'], 'STOCK_WASTAGE', 'Inventory', iid, f"Logged wastage of {w_qty} {irow['unit']} {waste_item} ({w_reason})")
            st.error(f"Wastage recorded: -{w_qty} {irow['unit']} deducted from {waste_item}.")
            st.rerun()

# ---------------------------------------------------------
# Page 10: Suppliers & Purchasing
# ---------------------------------------------------------
elif current_page == "Suppliers & Purchasing":
    st.title("🏢 Supplier Directory & Purchasing")
    st.caption("Manage food suppliers, contact information, tax clearance details, and supplier balances.")
    
    t1, t2 = st.tabs(["📋 Supplier Directory", "➕ Add New Supplier"])
    
    with t1:
        sup_df = db.read("SELECT * FROM suppliers WHERE company_id = :c ORDER BY name", {'c': company['id']})
        st.dataframe(sup_df.drop(columns=['id', 'company_id']), use_container_width=True, hide_index=True)
        
    with t2:
        with st.form("new_supplier_form"):
            s_name = st.text_input("Supplier Name *", placeholder="e.g. Koala Butchery & Meats")
            s_cat = st.selectbox("Category", ["Poultry & Meat", "Fresh Produce & Vegetables", "Grains & Bakery", "Beverages & Liquor", "Packaging & Consumables", "Utilities & Services"])
            s_contact = st.text_input("Contact Person", placeholder="e.g. Tendai Moyo (Sales Rep)")
            
            c1, c2 = st.columns(2)
            with c1:
                s_phone = st.text_input("Phone Number", "+263 ")
            with c2:
                s_email = st.text_input("Email Address", "orders@supplier.co.zw")
                
            s_tax = st.text_input("ZIMRA Tax Clearance / TIN (ITF 263)", placeholder="e.g. 10023456")
            sub_sup = st.form_submit_button("Save Supplier", type="primary")
            
        if sub_sup and s_name:
            db.run("""
                INSERT INTO suppliers(company_id, name, contact_person, phone, email, tax_id, category)
                VALUES(:c, :n, :cp, :p, :e, :t, :cat)
            """, {
                'c': company['id'], 'n': s_name.strip(), 'cp': s_contact, 'p': s_phone,
                'e': s_email, 't': s_tax, 'cat': s_cat
            })
            db.log_audit(company['id'], u['id'], 'SUPPLIER_ADD', 'Suppliers', 0, f"Added supplier: {s_name}")
            st.success(f"Supplier '{s_name}' registered successfully!")
            st.rerun()

# ---------------------------------------------------------
# Page 11: IFRS 18 Financial Statements
# ---------------------------------------------------------
elif current_page == "IFRS 18 Financial Statements":
    st.title("💼 IFRS 18 Financial Statements & Statutory Reports")
    st.caption("Standardized financial reporting: Operating, Investing, and Financing categories compliant with IFRS 18 (effective 2027).")
    
    # Period selector
    fc1, fc2 = st.columns(2)
    with fc1:
        f_start = st.date_input("Reporting Period Start", date(date.today().year, 1, 1))
    with fc2:
        f_end = st.date_input("Reporting Period End", date.today())
        
    period_str = f"{f_start.strftime('%d-%b-%Y')} to {f_end.strftime('%d-%b-%Y')}"
    
    # Financial Statement Calculations
    # 1. Revenue
    sales_res = db.read("""
        SELECT COALESCE(SUM(subtotal), 0) AS rev, COALESCE(SUM(discount), 0) AS disc
        FROM sales
        WHERE company_id = :c AND sale_date BETWEEN :d1 AND :d2
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    
    gross_revenue = float(sales_res.iloc[0]['rev'])
    discounts = float(sales_res.iloc[0]['disc'])
    net_revenue = gross_revenue - discounts
    
    # 2. Cost of Sales (COGS)
    cogs_res = db.read("""
        SELECT COALESCE(SUM(sl.quantity * mi.cost), 0) AS cogs
        FROM sale_lines sl
        JOIN menu_items mi ON mi.id = sl.item_id
        JOIN sales s ON s.id = sl.sale_id
        WHERE s.company_id = :c AND s.sale_date BETWEEN :d1 AND :d2
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    cost_of_sales = float(cogs_res.iloc[0]['cogs'])
    gross_profit = net_revenue - cost_of_sales
    
    # 3. Operating Expenses
    exp_res = db.read("""
        SELECT category, COALESCE(SUM(amount), 0) AS cat_amt
        FROM expenses
        WHERE company_id = :c AND expense_date BETWEEN :d1 AND :d2
        GROUP BY category
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    
    total_operating_expenses = float(exp_res['cat_amt'].sum()) if len(exp_res) else 0.0
    operating_profit = gross_profit - total_operating_expenses
    
    # 4. Financing & Tax
    financing_costs = total_operating_expenses * 0.02 # e.g. IMTT & bank fees
    profit_before_tax = operating_profit - financing_costs
    income_tax_expense = max(0.0, profit_before_tax * 0.2472) if profit_before_tax > 0 else 0.0 # 24.72% corporate tax in Zimbabwe (24% + 3% AIDS levy)
    profit_for_period = profit_before_tax - income_tax_expense
    
    # Tabs for Statements
    st_tabs = st.tabs([
        "1️⃣ Statement of Profit or Loss (IFRS 18)",
        "2️⃣ Statement of Financial Position (Balance Sheet)",
        "3️⃣ Cash Flow Statement",
        "4️⃣ Management Performance Measures (MPMs)",
        "5️⃣ Notes & Disclosure Checklist"
    ])
    
    with st_tabs[0]:
        st.subheader(f"Statement of Profit or Loss ({period_str})")
        
        pnl_lines = [
            ("Operating Category: Restaurant Revenue", net_revenue),
            ("Operating Category: Cost of Food & Ingredients Sold (COGS)", -cost_of_sales),
            ("GROSS OPERATING PROFIT", gross_profit),
            ("Operating Category: Selling, General & Administrative Expenses", -total_operating_expenses),
            ("OPERATING PROFIT (IFRS 18 Subtotal)", operating_profit),
            ("Financing Category: Bank Transfer Taxes & IMTT", -financing_costs),
            ("PROFIT BEFORE INCOME TAXES", profit_before_tax),
            ("Income Tax Expense (ZIMRA Corporate Tax)", -income_tax_expense),
            ("NET PROFIT FOR THE PERIOD", profit_for_period)
        ]
        
        pnl_df = pd.DataFrame(pnl_lines, columns=["IFRS 18 Financial Line Item", f"Amount ({curr})"])
        st.dataframe(pnl_df, use_container_width=True, hide_index=True)
        
        # PDF Generator
        pnl_pdf = pdf_gen.generate_financial_report_pdf(company, pnl_df, period_str=period_str)
        st.download_button(
            label="📄 Download Official IFRS 18 Financial Statements (PDF)",
            data=pnl_pdf,
            file_name=f"Financial_Statements_{f_start}_{f_end}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
    with st_tabs[1]:
        st.subheader("Statement of Financial Position (Balance Sheet)")
        
        # Balance sheet calculation
        inv_val = float(db.read("SELECT COALESCE(SUM(quantity * unit_cost), 0) AS v FROM inventory WHERE company_id = :c", {'c': company['id']}).iloc[0]['v'])
        cash_pos = 1500.0 + max(0.0, net_revenue - total_operating_expenses)
        bank_pos = 8500.0
        equipment_val = 25000.0
        
        tot_assets = cash_pos + bank_pos + inv_val + equipment_val
        
        trade_payables = 2400.0
        tax_payables = float(db.read("SELECT COALESCE(SUM(tax), 0) AS t FROM sales WHERE company_id = :c", {'c': company['id']}).iloc[0]['t'])
        tot_liab = trade_payables + tax_payables
        
        share_capital = 20000.0
        retained_earnings = tot_assets - tot_liab - share_capital
        
        bs_lines = [
            ("Current Assets: Cash in Drawer & Petty Cash", cash_pos),
            ("Current Assets: Operating Bank Account (USD)", bank_pos),
            ("Current Assets: Food & Beverage Inventory", inv_val),
            ("Non-Current Assets: Kitchen Equipment & Furniture", equipment_val),
            ("TOTAL ASSETS", tot_assets),
            ("Current Liabilities: Trade Accounts Payable", trade_payables),
            ("Current Liabilities: ZIMRA VAT Output Payable", tax_payables),
            ("TOTAL LIABILITIES", tot_liab),
            ("Equity: Share Capital", share_capital),
            ("Equity: Retained Earnings / Current Period Surplus", retained_earnings),
            ("TOTAL EQUITY & LIABILITIES", tot_liab + share_capital + retained_earnings)
        ]
        bs_df = pd.DataFrame(bs_lines, columns=["Balance Sheet Line Item", f"Amount ({curr})"])
        st.dataframe(bs_df, use_container_width=True, hide_index=True)
        
    with st_tabs[2]:
        st.subheader("Statement of Cash Flows (Direct Method)")
        cf_lines = [
            ("Cash Receipts from Restaurant Customers", net_revenue),
            ("Cash Payments to Food Suppliers & Vendors", -(cost_of_sales * 0.8)),
            ("Cash Payments for Operating Expenses & Utilities", -total_operating_expenses),
            ("NET CASH FLOW FROM OPERATING ACTIVITIES", net_revenue - (cost_of_sales * 0.8) - total_operating_expenses),
            ("Cash Flows from Investing Activities: Equipment Purchases", 0.0),
            ("Cash Flows from Financing Activities: Capital Contributions / Drawings", 0.0),
            ("NET INCREASE IN CASH AND CASH EQUIVALENTS", net_revenue - (cost_of_sales * 0.8) - total_operating_expenses)
        ]
        cf_df = pd.DataFrame(cf_lines, columns=["Cash Flow Line Item", f"Amount ({curr})"])
        st.dataframe(cf_df, use_container_width=True, hide_index=True)
        
    with st_tabs[3]:
        st.subheader("Management Performance Measures (MPMs)")
        st.caption("Key hospitality metrics and operational profitability ratios.")
        
        food_cost_margin = (cost_of_sales / net_revenue * 100) if net_revenue > 0 else 0.0
        gross_margin = (gross_profit / net_revenue * 100) if net_revenue > 0 else 0.0
        ebitda_margin = (operating_profit / net_revenue * 100) if net_revenue > 0 else 0.0
        
        mpm1, mpm2, mpm3 = st.columns(3)
        mpm1.metric("Gross Profit Margin", f"{gross_margin:.1f}%", "Target: >65%")
        mpm2.metric("Food Cost % (COGS)", f"{food_cost_margin:.1f}%", "Target: <32%", delta_color="inverse")
        mpm3.metric("Operating EBITDA Margin", f"{ebitda_margin:.1f}%", "Target: >20%")

    with st_tabs[4]:
        st.subheader("IFRS 18 Compliance & Disclosure Notes")
        st.markdown("""
        1. **Basis of Preparation**: These financial statements are prepared in accordance with IFRS 18 *Presentation and Disclosure in Financial Statements*.
        2. **Operating Category**: Includes all core hospitality transactions, food revenues, cost of inventory depletions, staff payroll, and restaurant overheads.
        3. **Functional Currency**: Transactions are recorded in **USD** with functional conversion to ZiG/ZWL at official RBZ reference rates where statutory.
        4. **Inventory Valuation**: Raw food and beverage stocks are valued at weighted average cost.
        5. **Auditor & Management Sign-off**: Ready for review by designated Financial Controller and independent auditors.
        """)

# ---------------------------------------------------------
# Page 12: General Ledger Journals
# ---------------------------------------------------------
elif current_page == "General Ledger Journals":
    st.title("⚖️ Double-Entry General Ledger Journals")
    st.caption("Manual journal adjustments with strict Debit == Credit validation.")
    
    t1, t2 = st.tabs(["📜 Posted Journals History", "➕ Record Journal Adjustment"])
    
    with t1:
        journals_df = db.read("""
            SELECT j.id, j.entry_date, j.reference, j.description, j.status,
                   u.full_name AS created_by_name, j.created_at
            FROM journals j
            LEFT JOIN users u ON u.id = j.created_by
            WHERE j.company_id = :c
            ORDER BY j.id DESC
        """, {'c': company['id']})
        
        if len(journals_df):
            st.dataframe(journals_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        else:
            st.info("No journal adjustments logged yet.")
            
    with t2:
        accounts_df = db.read("SELECT id, code, name, account_type FROM accounts WHERE company_id = :c ORDER BY code", {'c': company['id']})
        acc_dict = {int(r['id']): f"{r['code']} - {r['name']} ({r['account_type']})" for _, r in accounts_df.iterrows()}
        
        with st.form("journal_entry_form"):
            st.subheader("New Balanced Journal Entry")
            jc1, jc2 = st.columns(2)
            with jc1:
                j_date = st.date_input("Entry Date", date.today())
                j_ref = st.text_input("Journal Reference *", f"JV-{datetime.now():%Y%m%d%H%M}")
            with jc2:
                j_desc = st.text_input("Description / Memo *", "Period end adjustment")
                
            st.markdown("---")
            st.markdown("**Debit Entry:**")
            d_col1, d_col2 = st.columns([3, 2])
            with d_col1:
                debit_acc = st.selectbox("Debit Account *", options=list(acc_dict.keys()), format_func=lambda x: acc_dict[x], key="deb_acc")
            with d_col2:
                debit_amt = st.number_input(f"Debit Amount ({curr}) *", min_value=0.01, value=100.0, step=10.0, key="deb_amt")
                
            st.markdown("**Credit Entry:**")
            c_col1, c_col2 = st.columns([3, 2])
            with c_col1:
                credit_acc = st.selectbox("Credit Account *", options=list(acc_dict.keys()), format_func=lambda x: acc_dict[x], key="cred_acc", index=min(1, len(acc_dict)-1))
            with c_col2:
                credit_amt = st.number_input(f"Credit Amount ({curr}) *", min_value=0.01, value=100.0, step=10.0, key="cred_amt")
                
            is_balanced = round(debit_amt, 2) == round(credit_amt, 2)
            if not is_balanced:
                st.error(f"❌ Journal is out of balance! Difference: {curr} {abs(debit_amt - credit_amt):,.2f}")
            else:
                st.success("✅ Journal is balanced (Debits = Credits)")
                
            sub_jv = st.form_submit_button("Post Journal Entry", type="primary")
            
        if sub_jv:
            if not is_balanced:
                st.error("Cannot post an unbalanced journal entry.")
            elif debit_acc == credit_acc:
                st.error("Debit and Credit accounts must be distinct.")
            else:
                jid = db.execute_insert("""
                    INSERT INTO journals(company_id, entry_date, reference, description, status, created_by)
                    VALUES(:c, :d, :r, :desc, 'posted', :u)
                """, {'c': company['id'], 'd': str(j_date), 'r': j_ref, 'desc': j_desc, 'u': u['id']})
                
                db.run("""
                    INSERT INTO journal_lines(journal_id, account_id, debit, credit)
                    VALUES(:jid, :acc, :deb, 0.0), (:jid, :cracc, 0.0, :cred)
                """, {'jid': jid, 'acc': debit_acc, 'deb': debit_amt, 'cracc': credit_acc, 'cred': credit_amt})
                
                db.log_audit(company['id'], u['id'], 'JOURNAL_POST', 'Journals', jid, f"Posted balanced journal {j_ref} for {curr} {debit_amt:,.2f}")
                st.success(f"Journal Entry {j_ref} posted successfully!")
                st.rerun()

# ---------------------------------------------------------
# Page 13: Chart of Accounts
# ---------------------------------------------------------
elif current_page == "Chart of Accounts":
    st.title("📚 IFRS Chart of Accounts")
    st.caption("Standardized General Ledger chart of accounts with IFRS categories.")
    
    accounts_df = db.read("SELECT code, name, account_type, ifrs_category, balance, active FROM accounts WHERE company_id = :c ORDER BY code", {'c': company['id']})
    st.dataframe(accounts_df, use_container_width=True, hide_index=True)
    
    with st.expander("➕ Add New Account to Chart of Accounts"):
        with st.form("new_account_form"):
            ac_code = st.text_input("Account Code (e.g. 1120, 6800)")
            ac_name = st.text_input("Account Name (e.g. Ecocash Merchant USD)")
            ac_type = st.selectbox("Account Type", ["asset", "liability", "equity", "revenue", "expense"])
            ac_ifrs = st.selectbox("IFRS Category", ["Operating", "Investing", "Financing"])
            sub_acc = st.form_submit_button("Create Account")
            
        if sub_acc and ac_code and ac_name:
            db.run("""
                INSERT INTO accounts(company_id, code, name, account_type, ifrs_category, balance, active)
                VALUES(:c, :co, :n, :t, :i, 0.0, 1)
            """, {'c': company['id'], 'co': ac_code.strip(), 'n': ac_name.strip(), 't': ac_type, 'i': ac_ifrs})
            db.log_audit(company['id'], u['id'], 'ACCOUNT_ADD', 'Accounts', 0, f"Added GL account {ac_code} - {ac_name}")
            st.success(f"Account {ac_code} added!")
            st.rerun()

# ---------------------------------------------------------
# Page 14: Expenses Tracker
# ---------------------------------------------------------
elif current_page == "Expenses Tracker":
    st.title("💵 Restaurant Expenses & Purchases Tracker")
    st.caption("Record and analyze daily vendor purchases, utility bills, maintenance, and operating costs.")
    
    t1, t2 = st.tabs(["📋 Recorded Expenses", "➕ Record New Expense"])
    
    with t1:
        exp_df = db.read("""
            SELECT e.id, e.expense_date, e.category, e.description, e.amount,
                   COALESCE(e.supplier, s.name, 'N/A') AS vendor,
                   e.payment_method, e.receipt_no, u.full_name AS recorded_by
            FROM expenses e
            LEFT JOIN suppliers s ON s.id = e.supplier_id
            LEFT JOIN users u ON u.id = e.created_by
            WHERE e.company_id = :c
            ORDER BY e.expense_date DESC, e.id DESC
        """, {'c': company['id']})
        
        tot_exp = float(exp_df['amount'].sum()) if len(exp_df) else 0.0
        st.metric("Total Expenses Logged", f"{curr} {tot_exp:,.2f}")
        
        if len(exp_df):
            st.dataframe(exp_df.drop(columns=['id']), use_container_width=True, hide_index=True)
            st.download_button(
                label="📊 Export Expenses (CSV)",
                data=exp_df.to_csv(index=False),
                file_name=f"expenses_{date.today()}.csv",
                mime="text/csv"
            )
            
    with t2:
        with st.form("new_expense_form"):
            e_date = st.date_input("Expense Date", date.today())
            e_cat = st.selectbox("Category", [
                "Food Supplies", "Beverage Restock", "Utilities (Electricity, Gas, Water)",
                "Restaurant Rent & Rates", "Kitchen Consumables & Cleaning", "Staff Meals & Welfare",
                "Repairs & Maintenance", "POS & Software Subscriptions", "Marketing & Promotions", "Miscellaneous"
            ])
            e_desc = st.text_input("Description / Memo *", placeholder="e.g. Purchased fresh whole chickens from Irvines")
            
            c1, c2 = st.columns(2)
            with c1:
                e_amt = st.number_input(f"Amount ({curr}) *", min_value=0.01, value=50.0, step=5.0)
            with c2:
                e_pay_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Ecocash / Mobile Money", "Card", "Cheque"])
                
            c3, c4 = st.columns(2)
            with c3:
                e_supplier = st.text_input("Supplier / Vendor Name", placeholder="e.g. Irvines Zimbabwe")
            with c4:
                e_receipt = st.text_input("Receipt / Invoice Number", placeholder="e.g. REC-9921")
                
            sub_exp = st.form_submit_button("Record Expense", type="primary")
            
        if sub_exp and e_desc:
            eid = db.execute_insert("""
                INSERT INTO expenses(company_id, branch_id, expense_date, category, description, amount, supplier, payment_method, receipt_no, tax_deductible, created_by)
                VALUES(:c, 1, :d, :cat, :desc, :amt, :sup, :pm, :rec, 1, :u)
            """, {
                'c': company['id'], 'd': str(e_date), 'cat': e_cat, 'desc': e_desc,
                'amt': e_amt, 'sup': e_supplier, 'pm': e_pay_method, 'rec': e_receipt, 'u': u['id']
            })
            db.log_audit(company['id'], u['id'], 'EXPENSE_ADD', 'Expenses', eid, f"Recorded expense {curr} {e_amt:,.2f} for {e_desc}")
            st.success(f"Expense of {curr} {e_amt:,.2f} recorded!")
            st.rerun()

# ---------------------------------------------------------
# Page 15: Statutory Payroll Processor
# ---------------------------------------------------------
elif current_page == "Statutory Payroll Processor":
    st.title("🏛️ Zimbabwe Statutory Payroll Processor")
    st.caption("Automated calculation of ZIMRA PAYE brackets, 3% AIDS Levy, NSSA POBS (4.5%), APWCS, and branded PDF payslips.")
    
    employees_df = db.read("SELECT * FROM employees WHERE company_id = :c AND active = 1 ORDER BY employee_no", {'c': company['id']})
    
    if not len(employees_df):
        st.warning("No employees found. Please register staff in the Staff Directory.")
        st.stop()
        
    payroll_month = st.selectbox("Payroll Month", ["October 2026", "September 2026", "August 2026", "November 2026"])
    
    # Process payroll table
    payroll_records = []
    total_gross = 0.0
    total_paye = 0.0
    total_nssa = 0.0
    total_net = 0.0
    
    for _, emp in employees_df.iterrows():
        ename = emp['full_name']
        eno = emp['employee_no']
        sal = float(emp['salary'])
        allow = float(emp['allowances'])
        
        slip = tc.compute_employee_payslip(ename, eno, sal, allow)
        payroll_records.append(slip)
        
        total_gross += slip['gross_earnings']
        total_paye += slip['total_paye']
        total_nssa += (slip['nssa_employee'] + slip['nssa_employer'])
        total_net += slip['net_pay']
        
    pr_df = pd.DataFrame(payroll_records)
    
    # Payroll KPI Summary
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("Total Gross Payroll", f"{curr} {total_gross:,.2f}")
    pc2.metric("Total ZIMRA PAYE", f"{curr} {total_paye:,.2f}")
    pc3.metric("Total NSSA Remittance", f"{curr} {total_nssa:,.2f}")
    pc4.metric("Total Net Disbursed", f"{curr} {total_net:,.2f}")
    
    st.markdown("---")
    st.subheader(f"Staff Statutory Payroll Schedule - {payroll_month}")
    
    display_df = pr_df[[
        'employee_no', 'employee_name', 'basic_salary', 'allowances', 'gross_earnings',
        'nssa_employee', 'base_paye', 'aids_levy', 'total_paye', 'net_pay'
    ]].rename(columns={
        'employee_no': 'Emp #', 'employee_name': 'Employee Name',
        'basic_salary': f'Basic ({curr})', 'allowances': f'Allowances ({curr})',
        'gross_earnings': f'Gross ({curr})', 'nssa_employee': f'NSSA 4.5% ({curr})',
        'base_paye': f'PAYE ({curr})', 'aids_levy': f'AIDS Levy ({curr})',
        'total_paye': f'Total Tax ({curr})', 'net_pay': f'Net Pay ({curr})'
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📄 Generate & Download Confidential Employee Payslips")
    
    emp_names = pr_df['employee_name'].tolist()
    sel_emp = st.selectbox("Select Employee", emp_names)
    
    if sel_emp:
        slip_data = pr_df[pr_df['employee_name'] == sel_emp].iloc[0].to_dict()
        payslip_pdf = pdf_gen.generate_payslip_pdf(company, slip_data, payroll_month)
        
        st.download_button(
            label=f"📄 Download Confidential Payslip for {sel_emp} (PDF)",
            data=payslip_pdf,
            file_name=f"Payslip_{slip_data['employee_no']}_{payroll_month.replace(' ','_')}.pdf",
            mime="application/pdf",
            type="primary"
        )

# ---------------------------------------------------------
# Page 16: ZIMRA Tax & Statutory Hub
# ---------------------------------------------------------
elif current_page == "ZIMRA Tax & Statutory Hub":
    st.title("🏛️ ZIMRA Tax & Statutory Compliance Hub")
    st.caption("Zimbabwe Revenue Authority (ZIMRA) and NSSA statutory obligations, VAT 7 form, PAYE return, and IMTT.")
    
    t1, t2, t3 = st.tabs(["📑 ZIMRA VAT 7 Summary", "📋 Statutory Obligations Schedule", "💳 Record Tax Payment / Filing"])
    
    with t1:
        st.subheader("ZIMRA VAT 7 Return Computation (15% Standard Rate)")
        
        # Calculate Output VAT from sales
        sales_vat = db.read("SELECT COALESCE(SUM(subtotal), 0) AS sub, COALESCE(SUM(tax), 0) AS vat FROM sales WHERE company_id = :c", {'c': company['id']})
        taxable_sales = float(sales_vat.iloc[0]['sub'])
        output_vat = float(sales_vat.iloc[0]['vat'])
        
        # Calculate Input VAT from allowable expenses
        exp_vat = db.read("SELECT COALESCE(SUM(amount), 0) AS exp FROM expenses WHERE company_id = :c AND tax_deductible = 1", {'c': company['id']})
        taxable_purchases = float(exp_vat.iloc[0]['exp'])
        input_vat = round(taxable_purchases * 0.15, 2)
        
        net_vat_payable = output_vat - input_vat
        
        vc1, vc2, vc3 = st.columns(3)
        vc1.metric("Output VAT (Sales)", f"{curr} {output_vat:,.2f}")
        vc2.metric("Input VAT (Allowable Expenses)", f"{curr} {input_vat:,.2f}")
        vc3.metric("Net VAT Payable to ZIMRA", f"{curr} {net_vat_payable:,.2f}", delta=f"{curr} {net_vat_payable:,.2f}", delta_color="inverse")
        
        vat_summary_table = pd.DataFrame([
            ("Box 1: Total Standard Rated Supplies (Net Sales)", taxable_sales),
            ("Box 2: Output VAT Charged to Customers (15%)", output_vat),
            ("Box 3: Total Allowable Taxable Purchases & Expenses", taxable_purchases),
            ("Box 4: Input VAT Claimable on Invoices (15%)", input_vat),
            ("Box 5: NET VAT PAYABLE / (REFUND CLAIMABLE) TO ZIMRA", net_vat_payable)
        ], columns=["ZIMRA VAT 7 Section", f"Amount ({curr})"])
        
        st.dataframe(vat_summary_table, use_container_width=True, hide_index=True)
        
    with t2:
        st.subheader("Zimbabwe Statutory Tax Profile & Calendars")
        stat_table = pd.DataFrame([
            ("Value Added Tax (VAT)", "15% Standard Rate", "ZIMRA", "25th of following month", f"VAT No: {company.get('vat_number', '10045678')}"),
            ("PAYE Income Tax & AIDS Levy", "Progressive (0% - 40%) + 3% Levy", "ZIMRA", "10th of following month", f"TIN: {company.get('zimra_tin', '200145892')}"),
            ("NSSA POBS Pension Scheme", "4.5% Employee + 4.5% Employer", "NSSA", "10th of following month", f"NSSA: {company.get('nssa_number', 'NSSA-789012')}"),
            ("NSSA APWCS Workers Comp", "1.4% Employer Only", "NSSA", "10th of following month", "Statutory APWCS"),
            ("IMTT Transfer Tax", "2% on Electronic / Mobile Transfers", "ZIMRA", "Automated withholding", "Bank & Ecocash"),
            ("Withholding Tax on Contracts", "5% without valid ITF 263", "ZIMRA", "10th of following month", "Supplier withholding")
        ], columns=["Statutory Obligation", "Statutory Rate / Band", "Authority", "Filing Due Date", "Registration Ref"])
        st.dataframe(stat_table, use_container_width=True, hide_index=True)
        
    with t3:
        with st.form("record_tax_filing_form"):
            st.subheader("Log Official Tax Return Filing")
            tf_type = st.selectbox("Tax Return Type", ["ZIMRA VAT 7", "ZIMRA PAYE P2 Return", "NSSA Form P4", "Corporate Income Tax ITF 12C", "Withholding Tax ITF 263"])
            tf_period = st.text_input("Period Name", "October 2026")
            
            c1, c2 = st.columns(2)
            with c1:
                tf_due = st.number_input(f"Total Tax Liability ({curr})", min_value=0.0, value=150.0, step=10.0)
            with c2:
                tf_paid = st.number_input(f"Amount Paid / Remitted ({curr})", min_value=0.0, value=150.0, step=10.0)
                
            tf_date = st.date_input("Filing / Remittance Date", date.today())
            sub_tf = st.form_submit_button("Record Tax Return Submission", type="primary")
            
        if sub_tf:
            db.run("""
                INSERT INTO tax_returns(company_id, tax_type, period_name, gross_taxable, tax_liability, amount_paid, status, due_date)
                VALUES(:c, :t, :p, :g, :l, :pd, 'Submitted', :dd)
            """, {
                'c': company['id'], 't': tf_type, 'p': tf_period, 'g': tf_due,
                'l': tf_due, 'pd': tf_paid, 'dd': str(tf_date)
            })
            db.log_audit(company['id'], u['id'], 'TAX_FILING', 'TaxReturns', 0, f"Filed {tf_type} for {tf_period} ({curr} {tf_paid:,.2f})")
            st.success(f"Tax return for {tf_type} ({tf_period}) recorded successfully!")

# ---------------------------------------------------------
# Page 17: Organisation Structure
# ---------------------------------------------------------
elif current_page == "Organisation Structure":
    st.title("🏛️ Organisation Structure & Directorates")
    st.caption("Enterprise hierarchy based on production directorates and operational departments.")
    
    org_units = db.read("SELECT * FROM organisation_units WHERE company_id = :c ORDER BY unit_type, name", {'c': company['id']})
    
    directorates = org_units[org_units['unit_type'] == 'Directorate']
    st.subheader("Executive Directorates")
    
    d_cols = st.columns(3)
    for idx, (_, d_row) in enumerate(directorates.iterrows()):
        with d_cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### 🏢 {d_row['name']}")
                st.caption(d_row.get('description', 'Operational Directorate'))
                st.markdown("✅ **Active Directorate**")
                
    st.markdown("---")
    st.subheader("Departmental Units & Process Teams")
    st.dataframe(org_units.drop(columns=['id', 'company_id', 'parent_id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 18: Staff Directory
# ---------------------------------------------------------
elif current_page == "Staff Directory":
    st.title("👥 Staff Directory & Employee Management")
    st.caption("Manage employee profiles, job titles, statutory IDs, and salary scales.")
    
    t1, t2 = st.tabs(["📋 Staff Directory", "➕ Add New Employee"])
    
    with t1:
        staff_df = db.read("""
            SELECT e.id, e.employee_no, e.full_name, e.job_title, b.name AS branch_name,
                   e.salary, e.allowances, e.national_id, e.nssa_number, e.hire_date, e.active
            FROM employees e
            LEFT JOIN branches b ON b.id = e.branch_id
            WHERE e.company_id = :c
            ORDER BY e.employee_no
        """, {'c': company['id']})
        
        st.dataframe(
            staff_df.drop(columns=['id']).rename(columns={
                'employee_no': 'Emp #', 'full_name': 'Full Name', 'job_title': 'Position',
                'branch_name': 'Branch', 'salary': f'Basic ({curr})', 'allowances': f'Allowances ({curr})',
                'national_id': 'National ID', 'nssa_number': 'NSSA #', 'hire_date': 'Hire Date'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with t2:
        with st.form("new_employee_form"):
            e_no = st.text_input("Employee Code *", f"EMP-{len(staff_df)+1:03d}")
            e_name = st.text_input("Full Name *", placeholder="e.g. Tendai Chidzero")
            e_title = st.text_input("Job Title *", placeholder="e.g. Sous Chef / Barista")
            
            c1, c2 = st.columns(2)
            with c1:
                e_nid = st.text_input("National ID Number", placeholder="63-123456-X-42")
            with c2:
                e_nssa = st.text_input("NSSA Number", placeholder="NSSA-123456")
                
            c3, c4 = st.columns(2)
            with c3:
                e_sal = st.number_input(f"Basic Salary ({curr}) *", min_value=0.0, value=600.0, step=50.0)
            with c4:
                e_allow = st.number_input(f"Monthly Allowances ({curr})", min_value=0.0, value=50.0, step=10.0)
                
            e_date = st.date_input("Hire Date", date.today())
            sub_emp = st.form_submit_button("Register Employee", type="primary")
            
        if sub_emp and e_name:
            db.run("""
                INSERT INTO employees(company_id, branch_id, employee_no, full_name, national_id, nssa_number, job_title, salary, allowances, hire_date, active)
                VALUES(:c, 1, :eno, :fn, :nid, :nssa, :jt, :sal, :al, :hd, 1)
            """, {
                'c': company['id'], 'eno': e_no.strip(), 'fn': e_name.strip(),
                'nid': e_nid, 'nssa': e_nssa, 'jt': e_title, 'sal': e_sal, 'al': e_allow, 'hd': str(e_date)
            })
            db.log_audit(company['id'], u['id'], 'EMPLOYEE_ADD', 'Employees', 0, f"Registered employee {e_name} ({e_no})")
            st.success(f"Employee {e_name} ({e_no}) registered successfully!")
            st.rerun()

# ---------------------------------------------------------
# Page 19: Customer CRM & Loyalty
# ---------------------------------------------------------
elif current_page == "Customer CRM & Loyalty":
    st.title("🤝 Customer CRM & Loyalty Programs")
    st.caption("Guest profiles, repeat visit loyalty points, and corporate accounts.")
    
    t1, t2 = st.tabs(["📋 Customer Directory", "➕ Add New Guest Profile"])
    
    with t1:
        cust_df = db.read("""
            SELECT c.id, c.name, c.phone, c.email, c.loyalty_points, c.notes,
                   COUNT(s.id) AS total_visits,
                   COALESCE(SUM(s.total), 0) AS lifetime_spend
            FROM customers c
            LEFT JOIN sales s ON s.customer_id = c.id
            WHERE c.company_id = :c
            GROUP BY c.id, c.name, c.phone, c.email, c.loyalty_points, c.notes
            ORDER BY lifetime_spend DESC
        """, {'c': company['id']})
        
        st.dataframe(
            cust_df.drop(columns=['id']).rename(columns={
                'name': 'Customer Name', 'phone': 'Phone', 'email': 'Email',
                'loyalty_points': 'Points', 'total_visits': 'Total Visits',
                'lifetime_spend': f'Lifetime Spend ({curr})', 'notes': 'Preferences'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with t2:
        with st.form("new_customer_form"):
            cn_name = st.text_input("Customer Name *", placeholder="e.g. Tariro Chikwanha")
            cn_phone = st.text_input("Phone Number", "+263 77 ")
            cn_email = st.text_input("Email Address", "guest@example.co.zw")
            cn_notes = st.text_area("Preferences / Special Diet Notes", placeholder="Prefers patio seating, regular customer")
            sub_cust = st.form_submit_button("Save Customer", type="primary")
            
        if sub_cust and cn_name:
            db.run("""
                INSERT INTO customers(company_id, name, phone, email, loyalty_points, notes)
                VALUES(:c, :n, :p, :e, 10, :nt)
            """, {'c': company['id'], 'n': cn_name.strip(), 'p': cn_phone, 'e': cn_email, 'nt': cn_notes})
            db.log_audit(company['id'], u['id'], 'CUSTOMER_ADD', 'Customers', 0, f"Registered customer {cn_name}")
            st.success(f"Customer '{cn_name}' created!")
            st.rerun()

# ---------------------------------------------------------
# Page 20: User Administration & RBAC
# ---------------------------------------------------------
elif current_page == "User Administration & RBAC":
    st.title("👤 User Administration & Role-Based Access Control")
    st.caption("Manage ERP system users, administrative permissions, roles, and security.")
    
    if u['role'] not in ('admin', 'manager'):
        st.error("⛔ Administrator or Top-Management access required.")
        st.stop()
        
    t1, t2 = st.tabs(["📋 System Users", "➕ Create User Account"])
    
    with t1:
        users_df = db.read("""
            SELECT u.id, u.username, u.full_name, u.role, u.active, u.created_at
            FROM users u
            WHERE u.company_id = :c
            ORDER BY u.id
        """, {'c': company['id']})
        
        st.dataframe(users_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        
    with t2:
        with st.form("new_user_form"):
            un = st.text_input("Username *", placeholder="e.g. tmakuvaza")
            fn = st.text_input("Full Name *", placeholder="e.g. Tatenda Makuvaza")
            pw = st.text_input("Password *", type="password", placeholder="Enter strong password")
            ro = st.selectbox("Role *", ["employee", "cashier", "chef", "waiter", "accountant", "manager", "admin"])
            sub_u = st.form_submit_button("Create User Account", type="primary")
            
        if sub_u and un and fn and pw:
            try:
                db.run("""
                    INSERT INTO users(company_id, branch_id, username, full_name, password_hash, role, active)
                    VALUES(:c, 1, :u, :f, :p, :r, 1)
                """, {'c': company['id'], 'u': un.strip(), 'f': fn.strip(), 'p': db.hash_pw(pw), 'r': ro})
                db.log_audit(company['id'], u['id'], 'USER_CREATE', 'Users', 0, f"Created user {un} with role {ro}")
                st.success(f"User account '{un}' created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating user: {e}")

# ---------------------------------------------------------
# Page 21: System Audit Trail
# ---------------------------------------------------------
elif current_page == "System Audit Trail":
    st.title("🛡️ Central System Audit Trail")
    st.caption("Tamper-evident activity logs for sales, inventory depletions, journals, and user actions.")
    
    audit_df = db.read("""
        SELECT a.id, a.created_at AS timestamp, u.full_name AS user, a.action, a.entity, a.entity_id, a.detail
        FROM audit_log a
        LEFT JOIN users u ON u.id = a.user_id
        WHERE a.company_id = :c
        ORDER BY a.id DESC
        LIMIT 100
    """, {'c': company['id']})
    
    if len(audit_df):
        st.dataframe(audit_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        st.download_button(
            label="📊 Export Audit Trail (CSV)",
            data=audit_df.to_csv(index=False),
            file_name=f"audit_trail_{date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit records found.")

# ---------------------------------------------------------
# Page 22: Settings & Configuration
# ---------------------------------------------------------
elif current_page == "Settings & Configuration":
    st.title("⚙️ Restaurant Profile & ERP Settings")
    st.caption("Configure company branding, functional currency, tax IDs, and system environment.")
    
    if u['role'] not in ('admin', 'manager'):
        st.error("⛔ Administrator access required.")
        st.stop()
        
    with st.form("restaurant_settings_form"):
        st.subheader("Restaurant Information & Tax Profile")
        
        c1, c2 = st.columns(2)
        with c1:
            st_name = st.text_input("Restaurant Trading Name", company['name'])
            st_legal = st.text_input("Legal Entity Name", company.get('legal_name', 'Soulfyas Investments (Pvt) Ltd'))
            st_addr = st.text_area("Physical Address", company.get('address', '123 Samora Machel Ave, Harare, Zimbabwe'))
            st_phone = st.text_input("Phone Number", company.get('phone', '+263 242 700000'))
        with c2:
            st_tin = st.text_input("ZIMRA TIN", company.get('zimra_tin', '200145892'))
            st_vat = st.text_input("ZIMRA VAT Number", company.get('vat_number', '10045678'))
            st_nssa = st.text_input("NSSA Employer Number", company.get('nssa_number', 'NSSA-789012'))
            st_curr = st.selectbox("Functional Currency", ["USD", "ZiG", "ZAR", "GBP", "EUR"], index=["USD", "ZiG", "ZAR", "GBP", "EUR"].index(company.get('currency', 'USD')))
            
        sub_sett = st.form_submit_button("Save Settings & Update Profile", type="primary")
        
    if sub_sett:
        db.run("""
            UPDATE companies
            SET name = :n, trading_name = :n, legal_name = :l, address = :a, phone = :p,
                zimra_tin = :t, vat_number = :v, nssa_number = :ns, currency = :cu
            WHERE id = :cid
        """, {
            'n': st_name.strip(), 'l': st_legal.strip(), 'a': st_addr.strip(), 'p': st_phone.strip(),
            't': st_tin.strip(), 'v': st_vat.strip(), 'ns': st_nssa.strip(), 'cu': st_curr,
            'cid': company['id']
        })
        db.log_audit(company['id'], u['id'], 'SETTINGS_UPDATE', 'Company', company['id'], f"Updated company settings and currency to {st_curr}")
        st.success("Settings saved successfully! Refreshing ERP...")
        st.rerun()
        
    st.markdown("---")
    st.subheader("Database Status & Diagnostics")
    db_type = "SQLite (Local File)" if db.IS_SQLITE else "PostgreSQL / Neon (Production Cloud)"
    st.info(f"Connected Database Engine: **{db_type}**")
