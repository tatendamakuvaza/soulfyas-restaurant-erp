"""
Soulfyas Quality Restaurant ERP - Comprehensive Multi-Module Application
Enterprise Restaurant Management System with Multi-Currency (USD/ZiG), POS with Dish Modifiers & Split Bill,
Contactless Guest Table QR Ordering Portal, Kitchen Display System (KDS), Cashier Shifts & Z-Reports,
Automated Purchase Orders (BOM), IFRS 18 Financial Statements, Zimbabwe Statutory Tax & Payroll (ZIMRA & NSSA),
Double-Entry General Ledger, Tronc Tip Pool, and Branded ReportLab PDF Exports.
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
    .stApp {
        background-color: #fcfbf9;
    }
    
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e8e3d8;
        border-left: 5px solid #b78b2b;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #555555;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.35rem;
        color: #1a1a1a;
        font-weight: 700;
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
zig_rate = db.get_current_rate(company['id'], 'ZiG')

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
    
    # Real-time exchange rate badge
    st.caption(f"💱 **RBZ Rate**: 1 USD = **ZiG {zig_rate:.2f}**")
    st.markdown("---")
    
    # Categorized Modules
    modules = {
        "📊 Executive": ["Dashboard"],
        "🍽️ Front of House": ["Point of Sale (POS)", "Floor & Table Manager", "Guest Digital Menu & QR", "Invoices & Sales History"],
        "👨‍🍳 Kitchen & Menu": ["Kitchen Display System (KDS)", "Menu & Dishes", "Dish Modifiers & Add-ons", "Recipes & Food Costing (BOM)"],
        "📦 Supply Chain": ["Inventory & Stock Balances", "Stock Movements & Wastage", "Purchase Orders (Auto-Reorder)", "Suppliers Directory"],
        "💰 Cash & Operations": ["Cashier Shifts & Z-Reports", "Expenses Tracker", "Staff Attendance & Tip Pool (Tronc)"],
        "💼 Accounting & IFRS": ["IFRS 18 Financial Statements", "General Ledger Journals", "Chart of Accounts", "Exchange Rates Manager"],
        "🏛️ Tax & Payroll": ["Statutory Payroll Processor", "ZIMRA Tax & Statutory Hub"],
        "👥 People & Org": ["Organisation Structure", "Staff Directory", "Customer CRM & Loyalty"],
        "⚙️ Administration": ["User Administration & RBAC", "System Audit Trail", "Settings & Configuration"]
    }
    
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
    st.caption(f"Real-time operational & dual-currency financial overview for {company['name']} ({selected_branch})")
    
    today_str = str(date.today())
    
    # Daily metrics
    today_sales_df = db.read("SELECT COALESCE(SUM(total), 0) AS rev, COUNT(*) AS count, COALESCE(SUM(tax), 0) AS vat FROM sales WHERE sale_date = :d AND company_id = :c", {'d': today_str, 'c': company['id']})
    today_exp_df = db.read("SELECT COALESCE(SUM(amount), 0) AS exp FROM expenses WHERE expense_date = :d AND company_id = :c", {'d': today_str, 'c': company['id']})
    
    rev_today = float(today_sales_df.iloc[0]['rev'])
    orders_today = int(today_sales_df.iloc[0]['count'])
    exp_today = float(today_exp_df.iloc[0]['exp'])
    net_today = rev_today - exp_today
    avg_check = (rev_today / orders_today) if orders_today > 0 else 0.0
    
    # Low stock
    low_stock_df = db.read("SELECT * FROM inventory WHERE quantity <= reorder_level AND company_id = :c", {'c': company['id']})
    low_stock_count = len(low_stock_df)
    occupied_tables = db.read("SELECT COUNT(*) AS c FROM tables WHERE status = 'Occupied' AND company_id = :c", {'c': company['id']}).iloc[0]['c']
    
    # Top KPI Metrics Row
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Today Revenue (USD)", f"${rev_today:,.2f}", f"ZiG {rev_today * zig_rate:,.2f}")
    m2.metric("Orders Today", f"{orders_today} Invoices")
    m3.metric("Today Expenses", f"${exp_today:,.2f}")
    m4.metric("Net Daily Profit", f"${net_today:,.2f}", delta=f"{'+' if net_today >= 0 else ''}${net_today:,.2f}")
    m5.metric("Occupied Tables", f"{occupied_tables} Active")
    m6.metric("Low Stock Alerts", f"{low_stock_count} Items", delta=f"{low_stock_count} alerts" if low_stock_count else "Optimal", delta_color="inverse")
    
    if low_stock_count > 0:
        with st.expander(f"⚠️ **Low Stock Alert**: {low_stock_count} item(s) are below threshold", expanded=True):
            alert_items = [f"**{r['item_name']}**: {r['quantity']:g} {r['unit']} remaining (Reorder: {r['reorder_level']:g})" for _, r in low_stock_df.iterrows()]
            st.warning(" | ".join(alert_items))
            
    st.markdown("---")
    
    # Analytics Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 7-Day Revenue Trend")
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
        st.subheader("🔥 Top 5 Best-Selling Dishes")
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
                top_items.rename(columns={'name': 'Dish / Beverage', 'total_qty': 'Qty Sold', 'total_revenue': f'Revenue ({curr})'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No item sales logged yet.")

# ---------------------------------------------------------
# Page 2: Point of Sale (POS)
# ---------------------------------------------------------
elif current_page == "Point of Sale (POS)":
    st.title("🛒 Point of Sale & Order Terminal")
    st.caption(f"Live dual-currency POS (USD & ZiG @ {zig_rate:.2f}) with dish modifiers, table management, and instant ZIMRA QR tax receipts.")
    
    col_menu, col_cart = st.columns([3, 2])
    
    with col_menu:
        menu_items_all = db.read("SELECT * FROM menu_items WHERE company_id = :c AND active = 1 ORDER BY category, name", {'c': company['id']})
        modifiers_all = db.read("SELECT * FROM dish_modifiers WHERE company_id = :c AND active = 1 ORDER BY group_name, name", {'c': company['id']})
        
        if not len(menu_items_all):
            st.warning("No menu items found. Please add items in the Menu module.")
            st.stop()
            
        categories = ["All Categories"] + sorted(menu_items_all['category'].unique().tolist())
        
        sc1, sc2 = st.columns([2, 3])
        with sc1:
            selected_cat = st.selectbox("Category", categories, label_visibility="collapsed")
        with sc2:
            search_query = st.text_input("🔍 Search Dish...", label_visibility="collapsed")
            
        filtered_items = menu_items_all.copy()
        if selected_cat != "All Categories":
            filtered_items = filtered_items[filtered_items['category'] == selected_cat]
        if search_query.strip():
            filtered_items = filtered_items[filtered_items['name'].str.contains(search_query.strip(), case=False, na=False)]
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Display Menu Items with Modifiers Expander
        item_cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_items.iterrows()):
            with item_cols[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"**{row['name']}**")
                    tags = []
                    if row.get('is_vegetarian'):
                        tags.append("<span class='tag-veg'>🌱 Vegetarian</span>")
                    if row.get('is_spicy'):
                        tags.append("<span class='tag-spicy'>🌶️ Spicy</span>")
                    if tags:
                        st.markdown(" ".join(tags), unsafe_allow_html=True)
                    if row.get('description'):
                        st.caption(f"{row['description'][:60]}...")
                        
                    price_usd = float(row['price'])
                    price_zig = price_usd * zig_rate
                    st.markdown(f"**${price_usd:,.2f}** <small style='color:#777;'>/ ZiG {price_zig:,.2f}</small>", unsafe_allow_html=True)
                    
                    item_id = int(row['id'])
                    
                    # Optional Customization / Modifiers Expander
                    with st.expander("⚙️ Customize & Add to Order"):
                        # Modifiers
                        basting_mods = modifiers_all[modifiers_all['group_name'] == 'Basting & Heat']['name'].tolist()
                        side_mods = modifiers_all[modifiers_all['group_name'] == 'Side Choice']['name'].tolist()
                        extra_mods = modifiers_all[modifiers_all['group_name'] == 'Add-on Topping']
                        
                        sel_basting = st.selectbox("Basting / Spice", ["Standard"] + basting_mods, key=f"bast_{item_id}")
                        sel_side = st.selectbox("Side Choice", ["Standard Side"] + side_mods, key=f"side_{item_id}")
                        sel_extras = st.multiselect("Add-on Toppings", extra_mods['name'].tolist(), key=f"ext_{item_id}")
                        item_notes = st.text_input("Special Cooking Note", key=f"note_{item_id}", placeholder="e.g. Well done, sauce on side")
                        
                        extra_cost = 0.0
                        for ex in sel_extras:
                            extra_cost += float(extra_mods[extra_mods['name'] == ex].iloc[0]['additional_price'])
                            
                        tot_item_price = price_usd + extra_cost
                        
                        if st.button(f"➕ Add with Options (${tot_item_price:,.2f})", key=f"add_mod_{item_id}", type="primary", use_container_width=True):
                            custom_desc = []
                            if sel_basting != "Standard":
                                custom_desc.append(sel_basting)
                            if sel_side != "Standard Side":
                                custom_desc.append(sel_side)
                            if sel_extras:
                                custom_desc.extend(sel_extras)
                            if item_notes:
                                custom_desc.append(item_notes)
                                
                            cart_key = f"{item_id}_{'_'.join(custom_desc)}"
                            if cart_key in st.session_state.cart:
                                st.session_state.cart[cart_key]['qty'] += 1
                            else:
                                st.session_state.cart[cart_key] = {
                                    'id': item_id,
                                    'name': row['name'],
                                    'price': tot_item_price,
                                    'cost': float(row['cost']),
                                    'qty': 1,
                                    'notes': ", ".join(custom_desc)
                                }
                            st.rerun()

    with col_cart:
        with st.container(border=True):
            st.subheader("🛍️ Current Order Ticket")
            
            # Order type and table
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
                    
            cust_df = db.read("SELECT id, name, phone FROM customers WHERE company_id = :c ORDER BY name", {'c': company['id']})
            cust_options = {int(r['id']): f"{r['name']} ({r['phone']})" for _, r in cust_df.iterrows()}
            cust_options[0] = "Walk-in Guest"
            selected_cust_id = st.selectbox("Customer", options=list(cust_options.keys()), format_func=lambda x: cust_options[x], index=len(cust_options)-1)
            
            st.markdown("---")
            
            if not st.session_state.cart:
                st.info("🛒 Cart is empty. Select menu items to begin.")
            else:
                cart_items = list(st.session_state.cart.values())
                subtotal = 0.0
                
                for item in cart_items:
                    ckey = f"{item['id']}_{item.get('notes','')}"
                    line_tot = item['qty'] * item['price']
                    subtotal += line_tot
                    
                    cc1, cc2, cc3, cc4 = st.columns([3, 1, 1, 1])
                    with cc1:
                        notes_txt = f"<br/><small style='color:#666;'><i>{item['notes']}</i></small>" if item.get('notes') else ""
                        st.markdown(f"**{item['name']}**{notes_txt}<br/><small>${item['price']:,.2f} ea</small>", unsafe_allow_html=True)
                    with cc2:
                        if st.button("➖", key=f"dec_{ckey}"):
                            if st.session_state.cart[ckey]['qty'] > 1:
                                st.session_state.cart[ckey]['qty'] -= 1
                            else:
                                del st.session_state.cart[ckey]
                            st.rerun()
                    with cc3:
                        st.markdown(f"<p style='text-align:center; padding-top:6px;'><b>{item['qty']}</b></p>", unsafe_allow_html=True)
                    with cc4:
                        if st.button("➕", key=f"inc_{ckey}"):
                            st.session_state.cart[ckey]['qty'] += 1
                            st.rerun()
                            
                st.markdown("---")
                
                disc_c, tip_c = st.columns(2)
                with disc_c:
                    discount_amt = st.number_input("Discount ($)", min_value=0.0, max_value=float(subtotal), value=0.0, step=1.0)
                with tip_c:
                    tip_amt = st.number_input("Tip / Gratuity ($)", min_value=0.0, value=0.0, step=1.0)
                    
                taxable_base = max(0.0, subtotal - discount_amt)
                tax_rate = 0.15 # 15% ZIMRA VAT
                vat_amount = round(taxable_base * tax_rate, 2)
                grand_total = round(taxable_base + vat_amount + tip_amt, 2)
                grand_total_zig = round(grand_total * zig_rate, 2)
                
                st.markdown(f"""
                <div style='background-color:#fcfbf9; padding:10px; border-radius:6px; border:1px solid #e8e3d8;'>
                    <div style='display:flex; justify-content:space-between;'><span>Subtotal:</span><b>${subtotal:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>Discount:</span><b style='color:red;'>-${discount_amt:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>VAT (15% ZIMRA):</span><b>${vat_amount:,.2f}</b></div>
                    <div style='display:flex; justify-content:space-between;'><span>Tip / Gratuity:</span><b>${tip_amt:,.2f}</b></div>
                    <hr style='margin:6px 0;'/>
                    <div style='display:flex; justify-content:space-between; font-size:1.25rem; color:#9b721d;'>
                        <span><b>TOTAL (USD):</b></span><b>${grand_total:,.2f}</b>
                    </div>
                    <div style='display:flex; justify-content:space-between; font-size:1.05rem; color:#444444;'>
                        <span><b>TOTAL (ZiG):</b></span><b>ZiG {grand_total_zig:,.2f}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br/>", unsafe_allow_html=True)
                payment_method = st.selectbox("💳 Payment Method", ["Cash (USD)", "Cash (ZiG)", "Card (Visa/Mastercard)", "Ecocash (USD)", "Ecocash (ZiG)", "Bank Transfer", "Split Payment / Credit"])
                
                # Split Bill Feature
                split_count = st.number_input("Split Bill Across Diners", min_value=1, max_value=10, value=1)
                if split_count > 1:
                    st.info(f"Each person pays: **${grand_total/split_count:,.2f}** (or **ZiG {grand_total_zig/split_count:,.2f}**)")
                    
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if st.button("🗑️ Clear Cart", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()
                with btn_c2:
                    if st.button("✅ Complete Sale & Print", type="primary", use_container_width=True):
                        inv_no = f"SQR-{datetime.now():%Y%m%d%H%M%S}-{secrets.token_hex(2).upper()}"
                        
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
                            
                        # Deplete stock
                        db.deduct_inventory_for_sale(company['id'], sale_id, u['id'])
                        
                        if order_type == "Dine-In" and selected_table != "N/A":
                            db.run("UPDATE tables SET status = 'Occupied' WHERE table_number = :tn AND company_id = :c", {'tn': selected_table, 'c': company['id']})
                            
                        db.log_audit(company['id'], u['id'], 'POS_SALE', 'Sales', sale_id, f"Completed sale {inv_no} for ${grand_total:,.2f} via {payment_method}")
                        
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

    # Completed Sale Receipt Banner
    if st.session_state.last_completed_sale:
        last = st.session_state.last_completed_sale
        st.success(f"🎉 **Sale Completed!** Invoice: `{last['invoice_no']}` | Total: **${last['total']:,.2f}** (ZiG {last['total']*zig_rate:,.2f})")
        
        pdf_bytes = pdf_gen.generate_receipt_pdf(company, last, last['items'], zig_rate=zig_rate)
        
        rc1, rc2 = st.columns([1, 1])
        with rc1:
            st.download_button(
                label="📄 Download Official ZIMRA QR Tax Receipt (PDF)",
                data=pdf_bytes,
                file_name=f"Receipt_{last['invoice_no']}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        with rc2:
            if st.button("✖️ Start Next Order", use_container_width=True):
                st.session_state.last_completed_sale = None
                st.rerun()

# ---------------------------------------------------------
# Page 3: Floor & Table Manager
# ---------------------------------------------------------
elif current_page == "Floor & Table Manager":
    st.title("🪑 Floor Plan & Table Management")
    st.caption("Live dining room status, guest seating, and table QR code generation.")
    
    tables_df = db.read("SELECT * FROM tables WHERE company_id = :c ORDER BY section, table_number", {'c': company['id']})
    
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Total Tables", len(tables_df))
    tc2.metric("Available", len(tables_df[tables_df['status'] == 'Available']))
    tc3.metric("Occupied", len(tables_df[tables_df['status'] == 'Occupied']))
    tc4.metric("Reserved", len(tables_df[tables_df['status'] == 'Reserved']))
    
    st.markdown("---")
    
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
                    
                    new_status = st.selectbox(
                        "Status",
                        ["Available", "Occupied", "Reserved", "Cleaning / Billed"],
                        index=["Available", "Occupied", "Reserved", "Cleaning / Billed"].index(status) if status in ["Available", "Occupied", "Reserved", "Cleaning / Billed"] else 0,
                        key=f"status_tbl_{tbl['id']}"
                    )
                    if new_status != status:
                        db.run("UPDATE tables SET status = :s WHERE id = :tid", {'s': new_status, 'tid': int(tbl['id'])})
                        st.rerun()
                        
                    # Generate Table QR Code Placard PDF
                    order_url = f"https://soulfyas.co.zw/order?table={tbl['table_number']}"
                    qr_placard = pdf_gen.generate_table_qr_placard_pdf(company, tbl['table_number'], order_url)
                    st.download_button(
                        label=f"🖨️ QR Placard (Table {tbl['table_number']})",
                        data=qr_placard,
                        file_name=f"QR_Placard_Table_{tbl['table_number']}.pdf",
                        mime="application/pdf",
                        key=f"qr_btn_{tbl['id']}",
                        use_container_width=True
                    )

# ---------------------------------------------------------
# Page 4: Guest Digital Menu & QR
# ---------------------------------------------------------
elif current_page == "Guest Digital Menu & QR":
    st.title("📱 Customer-Facing Digital Menu & Self-Ordering")
    st.caption("Contactless guest ordering portal accessed via Table QR Codes.")
    
    st.info("💡 **Guest Perspective**: Diners scan the Table QR placard on their phones to view this digital menu and submit orders directly to the Kitchen Display System.")
    
    g_tab1, g_tab2 = st.tabs(["📖 Digital Menu Catalog", "🛎️ Submit Contactless Table Order"])
    
    with g_tab1:
        menu_items_all = db.read("SELECT * FROM menu_items WHERE company_id = :c AND active = 1 ORDER BY category, name", {'c': company['id']})
        cats = sorted(menu_items_all['category'].unique().tolist())
        
        for c in cats:
            st.subheader(f"🍴 {c}")
            c_items = menu_items_all[menu_items_all['category'] == c]
            for _, r in c_items.iterrows():
                with st.container(border=True):
                    c_col1, c_col2 = st.columns([4, 1])
                    with c_col1:
                        st.markdown(f"### {r['name']}")
                        tags = []
                        if r.get('is_vegetarian'):
                            tags.append("🌱 Vegetarian")
                        if r.get('is_spicy'):
                            tags.append("🌶️ Spicy")
                        if tags:
                            st.caption(" · ".join(tags))
                        st.write(r.get('description', 'Delicious chef specialty prepared fresh to order.'))
                    with c_col2:
                        p_usd = float(r['price'])
                        st.markdown(f"### ${p_usd:,.2f}")
                        st.caption(f"ZiG {p_usd * zig_rate:,.2f}")
                        
    with g_tab2:
        with st.form("guest_order_form"):
            st.subheader("Place Order from Table")
            g_table = st.selectbox("Your Table Number", ["T1", "T2", "T3", "T4", "T5", "P1", "P2", "VIP-1", "BAR-1"])
            g_name = st.text_input("Your Name", placeholder="e.g. Tendai")
            g_dish = st.selectbox("Select Dish", menu_items_all['name'].tolist())
            g_qty = st.number_input("Quantity", min_value=1, max_value=10, value=1)
            g_notes = st.text_input("Special Cooking Request", placeholder="e.g. Extra hot peri-peri, no onions")
            
            sub_g_order = st.form_submit_button("🛎️ Send Order to Kitchen", type="primary")
            
        if sub_g_order:
            dish_row = menu_items_all[menu_items_all['name'] == g_dish].iloc[0]
            dish_price = float(dish_row['price'])
            tot_price = dish_price * g_qty
            inv_no = f"SQR-GUEST-{datetime.now():%H%M%S}-{secrets.token_hex(2).upper()}"
            
            sid = db.execute_insert("""
                INSERT INTO sales(company_id, branch_id, invoice_no, sale_date, order_type, payment_method, subtotal, tax, total, status, kitchen_status, created_by)
                VALUES(:c, 1, :inv, :d, 'Dine-In', 'Pending Table Settlement', :sub, :tx, :tot, 'Pending', 'Pending', :u)
            """, {
                'c': company['id'], 'inv': inv_no, 'd': str(date.today()),
                'sub': tot_price, 'tx': tot_price*0.15, 'tot': tot_price*1.15, 'u': u['id']
            })
            
            db.run("""
                INSERT INTO kitchen_orders(sale_id, item_name, table_number, quantity, notes, status)
                VALUES(:sid, :iname, :tbl, :q, :nt, 'Pending')
            """, {'sid': sid, 'iname': g_dish, 'tbl': g_table, 'q': g_qty, 'nt': f"Guest: {g_name} | {g_notes}"})
            
            db.run("UPDATE tables SET status = 'Occupied' WHERE table_number = :tn AND company_id = :c", {'tn': g_table, 'c': company['id']})
            
            st.success(f"🎉 Thank you {g_name}! Your order for {g_qty}x {g_dish} has been sent to the kitchen for Table {g_table}.")

# ---------------------------------------------------------
# Page 5: Invoices & Sales History
# ---------------------------------------------------------
elif current_page == "Invoices & Sales History":
    st.title("🧾 Invoices & Order History")
    
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        date_from = st.date_input("From Date", date.today() - timedelta(days=30))
    with fc2:
        date_to = st.date_input("To Date", date.today())
    with fc3:
        filter_status = st.selectbox("Status", ["All", "Paid", "Pending", "Cancelled"])
    with fc4:
        search_inv = st.text_input("Search Invoice", "")
        
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
    
    ic1, ic2, ic3 = st.columns(3)
    tot_sales_vol = float(sales_df['total'].sum()) if len(sales_df) else 0.0
    tot_tax_vol = float(sales_df['tax'].sum()) if len(sales_df) else 0.0
    ic1.metric("Period Sales (USD)", f"${tot_sales_vol:,.2f}", f"ZiG {tot_sales_vol*zig_rate:,.2f}")
    ic2.metric("15% VAT Collected", f"${tot_tax_vol:,.2f}")
    ic3.metric("Total Invoices", len(sales_df))
    
    st.markdown("---")
    if len(sales_df):
        st.dataframe(sales_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        
        sel_invoice = st.selectbox("Select Invoice to Inspect / Reprint", sales_df['invoice_no'].tolist())
        if sel_invoice:
            sel_sale = sales_df[sales_df['invoice_no'] == sel_invoice].iloc[0].to_dict()
            lines_df = db.read("""
                SELECT mi.name, sl.quantity, sl.unit_price, sl.line_total, sl.notes
                FROM sale_lines sl
                JOIN menu_items mi ON mi.id = sl.item_id
                WHERE sl.sale_id = :sid
            """, {'sid': int(sel_sale['id'])})
            
            st.write(f"**Items in {sel_invoice}:**")
            st.dataframe(lines_df, use_container_width=True, hide_index=True)
            
            pdf_bytes = pdf_gen.generate_receipt_pdf(company, sel_sale, lines_df.to_dict('records'), zig_rate=zig_rate)
            
            pcol1, pcol2 = st.columns(2)
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
                    label="📊 Export Sales History (CSV)",
                    data=sales_df.to_csv(index=False),
                    file_name=f"sales_{date_from}_{date_to}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# ---------------------------------------------------------
# Page 6: Kitchen Display System (KDS)
# ---------------------------------------------------------
elif current_page == "Kitchen Display System (KDS)":
    st.title("👨‍🍳 Kitchen Display System (KDS)")
    st.caption("Live kitchen ticketing board and service flow.")
    
    orders_df = db.read("""
        SELECT ko.id, ko.sale_id, ko.item_name, ko.table_number, ko.quantity, ko.notes, ko.status, ko.created_at,
               s.invoice_no
        FROM kitchen_orders ko
        JOIN sales s ON s.id = ko.sale_id
        WHERE ko.status != 'Served'
        ORDER BY ko.id ASC
    """)
    
    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("⏳ Pending", len(orders_df[orders_df['status'] == 'Pending']))
    kc2.metric("🍳 In Preparation", len(orders_df[orders_df['status'] == 'In Preparation']))
    kc3.metric("🛎️ Ready for Service", len(orders_df[orders_df['status'] == 'Ready']))
    
    st.markdown("---")
    
    if not len(orders_df):
        st.success("🎉 All kitchen orders have been prepared and served! Kitchen is clear.")
    else:
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
                    if st.button("✅ Mark Served", key=f"serve_{ord_row['id']}", use_container_width=True):
                        db.run("UPDATE kitchen_orders SET status = 'Served' WHERE id = :id", {'id': int(ord_row['id'])})
                        st.rerun()

# ---------------------------------------------------------
# Page 7: Dish Modifiers & Add-ons
# ---------------------------------------------------------
elif current_page == "Dish Modifiers & Add-ons":
    st.title("⚙️ Dish Modifiers, Bastings & Add-on Options")
    st.caption("Manage side choices, cooking heat levels, sauces, and extra toppings for menu items.")
    
    t1, t2 = st.tabs(["📋 Modifiers Catalog", "➕ Add New Modifier"])
    
    with t1:
        mods_df = db.read("""
            SELECT m.id, m.group_name, m.name, m.additional_price, m.cost,
                   inv.item_name AS linked_ingredient, m.inventory_deduct_qty, m.active
            FROM dish_modifiers m
            LEFT JOIN inventory inv ON inv.id = m.inventory_item_id
            WHERE m.company_id = :c
            ORDER BY m.group_name, m.name
        """, {'c': company['id']})
        
        st.dataframe(
            mods_df.drop(columns=['id']).rename(columns={
                'group_name': 'Group / Category', 'name': 'Modifier Name',
                'additional_price': f'Extra Price ({curr})', 'cost': f'Food Cost ({curr})',
                'linked_ingredient': 'Linked Raw Ingredient', 'inventory_deduct_qty': 'Deduct Qty'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with t2:
        with st.form("new_modifier_form"):
            m_name = st.text_input("Modifier Name *", placeholder="e.g. Creamy Pepper Sauce")
            m_grp = st.selectbox("Group", ["Side Choice", "Basting & Heat", "Add-on Topping", "Salad Dressing", "Meat Temperature"])
            
            c1, c2 = st.columns(2)
            with c1:
                m_price = st.number_input(f"Additional Price ({curr})", min_value=0.0, value=1.5, step=0.5)
            with c2:
                m_cost = st.number_input(f"Estimated Cost ({curr})", min_value=0.0, value=0.4, step=0.1)
                
            inv_items = db.read("SELECT id, item_name, unit FROM inventory WHERE company_id = :c ORDER BY item_name", {'c': company['id']})
            inv_dict = {int(r['id']): f"{r['item_name']} ({r['unit']})" for _, r in inv_items.iterrows()}
            inv_dict[0] = "No Inventory Deduction"
            sel_inv = st.selectbox("Link to Raw Inventory", options=list(inv_dict.keys()), format_func=lambda x: inv_dict[x])
            m_deduct_qty = st.number_input("Deduct Qty per Portion", min_value=0.0, value=0.05, step=0.01)
            
            sub_mod = st.form_submit_button("Save Modifier", type="primary")
            
        if sub_mod and m_name:
            db.run("""
                INSERT INTO dish_modifiers(company_id, name, group_name, additional_price, cost, inventory_item_id, inventory_deduct_qty, active)
                VALUES(:c, :n, :g, :p, :co, :iid, :iq, 1)
            """, {
                'c': company['id'], 'n': m_name.strip(), 'g': m_grp, 'p': m_price, 'co': m_cost,
                'iid': sel_inv if sel_inv > 0 else None, 'iq': m_deduct_qty
            })
            db.log_audit(company['id'], u['id'], 'MODIFIER_ADD', 'DishModifiers', 0, f"Added modifier {m_name} to {m_grp}")
            st.success(f"Modifier '{m_name}' created!")
            st.rerun()

# ---------------------------------------------------------
# Page 8: Cashier Shifts & Z-Reports
# ---------------------------------------------------------
elif current_page == "Cashier Shifts & Z-Reports":
    st.title("💰 Cashier Shift Management & End-of-Day Z-Reports")
    st.caption("Cash drawer floats, tender reconciliations, physical cash counts, and printable Z-Reports.")
    
    shifts_df = db.read("""
        SELECT cs.id, cs.shift_start, cs.shift_end, u.full_name AS cashier_name,
               cs.opening_float, cs.cash_sales, cs.card_sales, cs.ecocash_sales, cs.bank_sales,
               (cs.cash_sales + cs.card_sales + cs.ecocash_sales + cs.bank_sales) AS total_revenue,
               cs.actual_cash_counted, cs.variance, cs.status
        FROM cashier_shifts cs
        JOIN users u ON u.id = cs.user_id
        WHERE cs.company_id = :c
        ORDER BY cs.id DESC
    """, {'c': company['id']})
    
    t1, t2, t3 = st.tabs(["📋 Shift History & Z-Reports", "🟢 Active Shift Tender Reconcile", "➕ Open New Shift"])
    
    with t1:
        if len(shifts_df):
            st.dataframe(shifts_df.drop(columns=['id']), use_container_width=True, hide_index=True)
            
            st.subheader("🖨️ Generate & Download Shift Z-Report (PDF)")
            sel_s_id = st.selectbox("Select Shift", shifts_df['id'].tolist(), format_func=lambda x: f"Shift #{x} - {shifts_df[shifts_df['id']==x].iloc[0]['cashier_name']} ({shifts_df[shifts_df['id']==x].iloc[0]['shift_start']})")
            
            if sel_s_id:
                s_data = shifts_df[shifts_df['id'] == sel_s_id].iloc[0].to_dict()
                z_pdf = pdf_gen.generate_z_report_pdf(company, s_data)
                st.download_button(
                    label=f"📄 Download Shift #{sel_s_id} Z-Report (PDF)",
                    data=z_pdf,
                    file_name=f"Z_Report_Shift_{sel_s_id}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
        else:
            st.info("No recorded cashier shifts.")
            
    with t2:
        open_shifts = shifts_df[shifts_df['status'] == 'open']
        if not len(open_shifts):
            st.info("No active open shift currently. Open a new shift below.")
        else:
            active_shift = open_shifts.iloc[0].to_dict()
            st.subheader(f"Active Shift #{active_shift['id']} - {active_shift['cashier_name']}")
            
            # Recalculate today sales by method
            today_s = db.read("""
                SELECT payment_method, COALESCE(SUM(total), 0) AS tot
                FROM sales
                WHERE company_id = :c AND sale_date = :d
                GROUP BY payment_method
            """, {'c': company['id'], 'd': str(date.today())})
            
            cash_sales = float(today_s[today_s['payment_method'].str.contains('Cash', case=False, na=False)]['tot'].sum()) if len(today_s) else 0.0
            card_sales = float(today_s[today_s['payment_method'].str.contains('Card', case=False, na=False)]['tot'].sum()) if len(today_s) else 0.0
            eco_sales = float(today_s[today_s['payment_method'].str.contains('Ecocash', case=False, na=False)]['tot'].sum()) if len(today_s) else 0.0
            bank_sales = float(today_s[today_s['payment_method'].str.contains('Bank', case=False, na=False)]['tot'].sum()) if len(today_s) else 0.0
            
            op_float = float(active_shift['opening_float'])
            expected_cash = op_float + cash_sales
            
            ac1, ac2, ac3, ac4 = st.columns(4)
            ac1.metric("Opening Float", f"${op_float:,.2f}")
            ac2.metric("Cash Sales Collected", f"${cash_sales:,.2f}")
            ac3.metric("Digital / Card Sales", f"${card_sales + eco_sales + bank_sales:,.2f}")
            ac4.metric("Expected Cash in Drawer", f"${expected_cash:,.2f}")
            
            with st.form("close_shift_form"):
                st.markdown("### 🔒 Close Cashier Shift & Perform End-of-Day Reconciliation")
                actual_counted = st.number_input("Physical Cash Counted in Drawer ($)", min_value=0.0, value=expected_cash, step=10.0)
                shift_notes = st.text_area("Shift Supervisor Notes", "Standard shift closeout")
                sub_close = st.form_submit_button("Finalize Shift & Generate Z-Report", type="primary")
                
            if sub_close:
                var = actual_counted - expected_cash
                db.run("""
                    UPDATE cashier_shifts
                    SET shift_end = :send, cash_sales = :cs, card_sales = :cd, ecocash_sales = :ec, bank_sales = :bs,
                        actual_cash_counted = :ac, variance = :vr, status = 'closed', notes = :nt
                    WHERE id = :sid
                """, {
                    'send': datetime.now(), 'cs': cash_sales, 'cd': card_sales, 'ec': eco_sales, 'bs': bank_sales,
                    'ac': actual_counted, 'vr': var, 'nt': shift_notes, 'sid': int(active_shift['id'])
                })
                db.log_audit(company['id'], u['id'], 'SHIFT_CLOSE', 'CashierShifts', active_shift['id'], f"Closed shift #{active_shift['id']} with variance ${var:,.2f}")
                st.success(f"Shift #{active_shift['id']} closed successfully! Variance: ${var:,.2f}")
                st.rerun()

    with t3:
        with st.form("open_new_shift_form"):
            st.subheader("Open Cashier Register Shift")
            cashiers = db.read("SELECT id, full_name FROM users WHERE company_id = :c AND role IN ('cashier', 'manager', 'admin')", {'c': company['id']})
            cashier_dict = {int(r['id']): r['full_name'] for _, r in cashiers.iterrows()}
            sel_cashier = st.selectbox("Assigned Cashier", options=list(cashier_dict.keys()), format_func=lambda x: cashier_dict[x])
            start_float = st.number_input("Opening Float Cash Provided ($)", min_value=0.0, value=100.0, step=10.0)
            sub_open = st.form_submit_button("Open Shift Register", type="primary")
            
        if sub_open:
            sid = db.execute_insert("""
                INSERT INTO cashier_shifts(company_id, branch_id, user_id, shift_start, opening_float, status)
                VALUES(:c, 1, :uid, :start_time, :flt, 'open')
            """, {'c': company['id'], 'uid': sel_cashier, 'start_time': datetime.now(), 'flt': start_float})
            db.log_audit(company['id'], u['id'], 'SHIFT_OPEN', 'CashierShifts', sid, f"Opened shift #{sid} with float ${start_float:,.2f}")
            st.success(f"Shift #{sid} is now open with ${start_float:,.2f} float!")
            st.rerun()

# ---------------------------------------------------------
# Page 9: Purchase Orders (Auto-Reorder)
# ---------------------------------------------------------
elif current_page == "Purchase Orders (Auto-Reorder)":
    st.title("📦 Supplier Purchase Orders & Auto-Reordering")
    st.caption("Generate formal purchase orders for food suppliers based on stock depletion and par levels.")
    
    t1, t2, t3 = st.tabs(["📋 Purchase Orders List", "🤖 Auto-Generate PO for Low Stock", "➕ Create Manual PO"])
    
    with t1:
        po_df = db.read("""
            SELECT po.id, po.po_number, po.order_date, po.expected_delivery_date,
                   s.name AS supplier_name, po.subtotal, po.tax, po.total, po.status,
                   u.full_name AS created_by_name
            FROM purchase_orders po
            JOIN suppliers s ON s.id = po.supplier_id
            LEFT JOIN users u ON u.id = po.created_by
            WHERE po.company_id = :c
            ORDER BY po.id DESC
        """, {'c': company['id']})
        
        if len(po_df):
            st.dataframe(po_df.drop(columns=['id']), use_container_width=True, hide_index=True)
            
            st.subheader("📄 Download Supplier Purchase Order (PDF)")
            sel_po_id = st.selectbox("Select PO", po_df['id'].tolist(), format_func=lambda x: f"{po_df[po_df['id']==x].iloc[0]['po_number']} - {po_df[po_df['id']==x].iloc[0]['supplier_name']}")
            
            if sel_po_id:
                po_row = po_df[po_df['id'] == sel_po_id].iloc[0].to_dict()
                sup_row = db.read("SELECT * FROM suppliers WHERE name = :n", {'n': po_row['supplier_name']}).iloc[0].to_dict()
                po_row['contact_person'] = sup_row.get('contact_person', 'Sales Rep')
                po_row['phone'] = sup_row.get('phone', 'N/A')
                po_row['email'] = sup_row.get('email', 'N/A')
                
                po_lines = db.read("""
                    SELECT inv.item_name, inv.unit, pol.quantity, pol.unit_cost, pol.line_total
                    FROM purchase_order_lines pol
                    JOIN inventory inv ON inv.id = pol.inventory_item_id
                    WHERE pol.po_id = :poid
                """, {'poid': sel_po_id}).to_dict('records')
                
                po_pdf = pdf_gen.generate_purchase_order_pdf(company, po_row, po_lines)
                st.download_button(
                    label=f"📄 Download {po_row['po_number']} PDF",
                    data=po_pdf,
                    file_name=f"PO_{po_row['po_number']}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
        else:
            st.info("No purchase orders created yet.")
            
    with t2:
        st.subheader("Auto-Calculate Restock Requirements")
        low_items = db.read("""
            SELECT i.id, i.item_name, i.category, i.unit, i.quantity, i.reorder_level, i.unit_cost,
                   (i.reorder_level * 2 - i.quantity) AS suggested_order_qty,
                   s.id AS supplier_id, s.name AS supplier_name
            FROM inventory i
            LEFT JOIN suppliers s ON s.id = i.supplier_id
            WHERE i.company_id = :c AND i.quantity <= i.reorder_level
        """, {'c': company['id']})
        
        if not len(low_items):
            st.success("🎉 All inventory stock levels are currently above reorder thresholds!")
        else:
            st.dataframe(low_items.drop(columns=['id', 'supplier_id']), use_container_width=True, hide_index=True)
            
            if st.button("🚀 Auto-Generate Purchase Orders for All Low Stock Items", type="primary"):
                # Group by supplier
                for sup_id, group in low_items.groupby('supplier_id'):
                    if pd.isna(sup_id) or sup_id == 0:
                        sup_id = 1
                    po_no = f"PO-{datetime.now():%Y%m%d%H%M}-{secrets.token_hex(2).upper()}"
                    
                    po_tot = sum(max(1.0, float(r['suggested_order_qty'])) * float(r['unit_cost']) for _, r in group.iterrows())
                    
                    poid = db.execute_insert("""
                        INSERT INTO purchase_orders(company_id, po_number, supplier_id, order_date, expected_delivery_date, subtotal, total, status, created_by)
                        VALUES(:c, :po, :sid, :d, :ed, :sub, :tot, 'Sent', :u)
                    """, {
                        'c': company['id'], 'po': po_no, 'sid': int(sup_id), 'd': str(date.today()),
                        'ed': str(date.today() + timedelta(days=2)), 'sub': po_tot, 'tot': po_tot, 'u': u['id']
                    })
                    
                    for _, r in group.iterrows():
                        sqty = max(1.0, float(r['suggested_order_qty']))
                        db.run("""
                            INSERT INTO purchase_order_lines(po_id, inventory_item_id, quantity, unit_cost, line_total)
                            VALUES(:poid, :invid, :q, :co, :lt)
                        """, {'poid': poid, 'invid': int(r['id']), 'q': sqty, 'co': float(r['unit_cost']), 'lt': sqty * float(r['unit_cost'])})
                        
                st.success("Auto-generated Purchase Orders for suppliers! Check the Purchase Orders List tab.")
                st.rerun()

    with t3:
        with st.form("manual_po_form"):
            st.subheader("Create Custom Purchase Order")
            sup_all = db.read("SELECT id, name FROM suppliers WHERE company_id = :c", {'c': company['id']})
            sup_dict = {int(r['id']): r['name'] for _, r in sup_all.iterrows()}
            sel_sup = st.selectbox("Supplier", options=list(sup_dict.keys()), format_func=lambda x: sup_dict[x])
            
            inv_all = db.read("SELECT id, item_name, unit, unit_cost FROM inventory WHERE company_id = :c", {'c': company['id']})
            sel_inv = st.selectbox("Inventory Item", inv_all['item_name'].tolist())
            
            c1, c2 = st.columns(2)
            with c1:
                p_qty = st.number_input("Order Quantity", min_value=1.0, value=25.0, step=5.0)
            with c2:
                p_cost = st.number_input("Unit Cost ($)", min_value=0.0, value=3.5, step=0.5)
                
            sub_m_po = st.form_submit_button("Create Purchase Order", type="primary")
            
        if sub_m_po and sel_inv:
            inv_row = inv_all[inv_all['item_name'] == sel_inv].iloc[0]
            po_no = f"PO-{datetime.now():%Y%m%d%H%M}-{secrets.token_hex(2).upper()}"
            tot_val = p_qty * p_cost
            
            poid = db.execute_insert("""
                INSERT INTO purchase_orders(company_id, po_number, supplier_id, order_date, expected_delivery_date, subtotal, total, status, created_by)
                VALUES(:c, :po, :sid, :d, :ed, :sub, :tot, 'Draft', :u)
            """, {
                'c': company['id'], 'po': po_no, 'sid': sel_sup, 'd': str(date.today()),
                'ed': str(date.today() + timedelta(days=2)), 'sub': tot_val, 'tot': tot_val, 'u': u['id']
            })
            
            db.run("""
                INSERT INTO purchase_order_lines(po_id, inventory_item_id, quantity, unit_cost, line_total)
                VALUES(:poid, :invid, :q, :co, :lt)
            """, {'poid': poid, 'invid': int(inv_row['id']), 'q': p_qty, 'co': p_cost, 'lt': tot_val})
            
            st.success(f"Purchase Order {po_no} created successfully!")
            st.rerun()

# ---------------------------------------------------------
# Page 10: Staff Attendance & Tip Pool (Tronc)
# ---------------------------------------------------------
elif current_page == "Staff Attendance & Tip Pool (Tronc)":
    st.title("👥 Staff Attendance & Tip Pool (Tronc) Distribution")
    st.caption("Shift clock-in/out tracking and fair service tip pool distribution based on hours worked.")
    
    t1, t2 = st.tabs(["🕒 Daily Clock-In / Attendance", "🎁 Service Tip Pool (Tronc) Calculator"])
    
    with t1:
        employees_df = db.read("SELECT id, employee_no, full_name, job_title FROM employees WHERE company_id = :c AND active = 1 ORDER BY employee_no", {'c': company['id']})
        
        with st.form("attendance_form"):
            st.subheader("Log Staff Shift Hours")
            att_emp = st.selectbox("Employee", employees_df['full_name'].tolist())
            att_date = st.date_input("Work Date", date.today())
            att_hrs = st.number_input("Hours Worked", min_value=1.0, max_value=16.0, value=8.0, step=0.5)
            att_stat = st.selectbox("Status", ["Present", "Late", "Overtime", "Half-Day"])
            sub_att = st.form_submit_button("Record Shift Attendance", type="primary")
            
        if sub_att and att_emp:
            emp_id = int(employees_df[employees_df['full_name'] == att_emp].iloc[0]['id'])
            db.run("""
                INSERT INTO staff_attendance(company_id, employee_id, work_date, hours_worked, status)
                VALUES(:c, :eid, :d, :hrs, :st)
            """, {'c': company['id'], 'eid': emp_id, 'd': str(att_date), 'hrs': att_hrs, 'st': att_stat})
            st.success(f"Logged {att_hrs} hours for {att_emp} on {att_date}!")
            
        st.markdown("---")
        st.subheader("Recent Attendance Records")
        att_df = db.read("""
            SELECT sa.id, sa.work_date, emp.employee_no, emp.full_name, emp.job_title, sa.hours_worked, sa.status
            FROM staff_attendance sa
            JOIN employees emp ON emp.id = sa.employee_id
            WHERE sa.company_id = :c
            ORDER BY sa.work_date DESC, sa.id DESC
            LIMIT 30
        """, {'c': company['id']})
        if len(att_df):
            st.dataframe(att_df.drop(columns=['id']), use_container_width=True, hide_index=True)
            
    with t2:
        st.subheader("Distribute Collected Service Gratuities (Tronc Pool)")
        
        # Calculate total tips collected from sales
        total_tips_collected = float(db.read("SELECT COALESCE(SUM(tip), 0) AS t FROM sales WHERE company_id = :c", {'c': company['id']}).iloc[0]['t'])
        
        st.metric("Total Tips Collected in Register", f"${total_tips_collected:,.2f}", f"ZiG {total_tips_collected*zig_rate:,.2f}")
        
        staff_pool = db.read("""
            SELECT emp.id AS employee_id, emp.full_name AS employee_name, emp.job_title AS role,
                   COALESCE(SUM(sa.hours_worked), 8.0) AS hours_worked
            FROM employees emp
            LEFT JOIN staff_attendance sa ON sa.employee_id = emp.id
            WHERE emp.company_id = :c AND emp.active = 1
            GROUP BY emp.id, emp.full_name, emp.job_title
        """, {'c': company['id']}).to_dict('records')
        
        dist_records = tc.calculate_tronc_distribution(total_tips_collected, staff_pool)
        dist_df = pd.DataFrame(dist_records)
        
        st.dataframe(
            dist_df[['employee_name', 'role', 'hours_worked', 'hourly_tip_rate', 'tip_payout']].rename(columns={
                'employee_name': 'Staff Member', 'role': 'Position', 'hours_worked': 'Hours on Shift',
                'hourly_tip_rate': f'Tip Rate / Hr ({curr})', 'tip_payout': f'Gratuity Payout ({curr})'
            }),
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# Page 11: Exchange Rates Manager
# ---------------------------------------------------------
elif current_page == "Exchange Rates Manager":
    st.title("💱 Foreign Exchange & RBZ Rate Manager")
    st.caption("Manage official Zimbabwe Gold (ZiG), South African Rand (ZAR), and currency conversions.")
    
    rates_df = db.read("SELECT id, base_currency, target_currency, rate, effective_date, is_current FROM exchange_rates WHERE company_id = :c ORDER BY id DESC", {'c': company['id']})
    st.dataframe(rates_df.drop(columns=['id']), use_container_width=True, hide_index=True)
    
    with st.form("update_rate_form"):
        st.subheader("Update Currency Exchange Rate")
        c_target = st.selectbox("Target Currency", ["ZiG", "ZAR", "EUR", "GBP"])
        c_rate = st.number_input("New Rate (1 USD = X)", min_value=0.0001, value=float(zig_rate) if c_target=='ZiG' else 18.20, step=0.1, format="%.4f")
        sub_rate = st.form_submit_button("Update Exchange Rate", type="primary")
        
    if sub_rate:
        db.run("""
            UPDATE exchange_rates SET is_current = 0 WHERE company_id = :c AND target_currency = :t
        """, {'c': company['id'], 't': c_target})
        
        db.run("""
            INSERT INTO exchange_rates(company_id, base_currency, target_currency, rate, effective_date, is_current)
            VALUES(:c, 'USD', :t, :r, :d, 1)
        """, {'c': company['id'], 't': c_target, 'r': c_rate, 'd': str(date.today())})
        
        db.log_audit(company['id'], u['id'], 'EXCHANGE_RATE_UPDATE', 'ExchangeRates', 0, f"Updated 1 USD = {c_rate} {c_target}")
        st.success(f"Exchange rate updated: 1 USD = {c_rate} {c_target}!")
        st.rerun()

# ---------------------------------------------------------
# Page 12: Menu & Dishes
# ---------------------------------------------------------
elif current_page == "Menu & Dishes":
    st.title("🍽️ Menu Items & Dish Catalog")
    
    t1, t2 = st.tabs(["📋 Current Menu Catalog", "➕ Add Menu Item"])
    
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
                mi_prep = st.number_input("Prep Time (mins)", min_value=1, max_value=120, value=15)
                
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
            st.success(f"Menu item '{mi_name}' created!")
            st.rerun()

# ---------------------------------------------------------
# Page 13: Recipes & Food Costing (BOM)
# ---------------------------------------------------------
elif current_page == "Recipes & Food Costing (BOM)":
    st.title("🧪 Recipes & Bill of Materials (BOM)")
    st.caption("Link dishes to raw ingredients for automatic stock deduction upon sale and exact food costing.")
    
    recipes_df = db.read("""
        SELECT r.id, r.menu_item_id, mi.name as dish_name, mi.price as selling_price,
               r.yield_quantity, r.instructions
        FROM recipes r
        JOIN menu_items mi ON mi.id = r.menu_item_id
        WHERE r.company_id = :c AND r.active = 1
        ORDER BY mi.name
    """, {'c': company['id']})
    
    if len(recipes_df):
        selected_dish = st.selectbox("Select Dish", recipes_df['dish_name'].tolist())
        sel_rec = recipes_df[recipes_df['dish_name'] == selected_dish].iloc[0]
        rec_id = int(sel_rec['id'])
        
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
        
        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("Selling Price", f"${selling_price:,.2f}")
        rc2.metric("Calculated Food Cost", f"${total_recipe_cost:,.2f}")
        rc3.metric("Gross Profit", f"${selling_price - total_recipe_cost:,.2f}")
        rc4.metric("Food Cost %", f"{food_cost_pct:.1f}%", delta=f"{food_cost_pct:.1f}% Target: <35%", delta_color="inverse")
        
        st.markdown("---")
        st.dataframe(lines.drop(columns=['id']), use_container_width=True, hide_index=True)
        
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

# ---------------------------------------------------------
# Page 14: Inventory & Stock Balances
# ---------------------------------------------------------
elif current_page == "Inventory & Stock Balances":
    st.title("📦 Inventory & Raw Materials")
    
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
    iv1.metric("Total Stock Valuation", f"${tot_inv_val:,.2f}", f"ZiG {tot_inv_val*zig_rate:,.2f}")
    iv2.metric("Total Inventory Items", len(inv_df))
    iv3.metric("Items Below Reorder Level", len(low_stock), delta=f"{len(low_stock)} items", delta_color="inverse")
    
    st.markdown("---")
    
    t1, t2, t3 = st.tabs(["📋 Current Stock List", "➕ Add Raw Material", "🔄 Quick Restock Delivery"])
    
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
        
        pdf_val_bytes = pdf_gen.generate_inventory_valuation_pdf(company, inv_df)
        dcol1, dcol2 = st.columns(2)
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
                file_name=f"stock_{date.today()}.csv",
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
            st.success(f"Inventory item '{in_name}' created!")
            st.rerun()

    with t3:
        with st.form("quick_restock_form"):
            restock_item = st.selectbox("Select Raw Material", inv_df['item_name'].tolist())
            rc1, rc2 = st.columns(2)
            with rc1:
                add_qty = st.number_input("Quantity Received", min_value=0.1, value=10.0, step=1.0)
            with rc2:
                new_unit_cost = st.number_input(f"Purchase Unit Cost ({curr})", min_value=0.0, value=2.0, step=0.1)
            invoice_ref = st.text_input("Delivery Note / Invoice Ref", placeholder="e.g. GRN-9921")
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
            
            st.success(f"Added {add_qty} {inv_row['unit']} to '{restock_item}'!")
            st.rerun()

# ---------------------------------------------------------
# Page 15: Stock Movements & Wastage
# ---------------------------------------------------------
elif current_page == "Stock Movements & Wastage":
    st.title("🔄 Stock Movements & Food Wastage Tracking")
    
    t1, t2 = st.tabs(["📜 Stock Movements Log", "⚠️ Log Kitchen Wastage"])
    
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
            
    with t2:
        with st.form("log_wastage_form"):
            inv_items = db.read("SELECT id, item_name, unit, unit_cost FROM inventory WHERE company_id = :c ORDER BY item_name", {'c': company['id']})
            waste_item = st.selectbox("Select Wasted Ingredient", inv_items['item_name'].tolist())
            
            c1, c2 = st.columns(2)
            with c1:
                w_qty = st.number_input("Quantity Wasted", min_value=0.01, value=1.0, step=0.5)
            with c2:
                w_reason = st.selectbox("Reason Code", ["Burnt / Kitchen Prep Error", "Expired / Spoilage", "Dropped / Spillage", "Quality Defect on Inspection"])
            w_notes = st.text_input("Detailed Explanation")
            sub_waste = st.form_submit_button("Record Wastage & Deduct Stock", type="primary")
            
        if sub_waste and waste_item:
            irow = inv_items[inv_items['item_name'] == waste_item].iloc[0]
            iid = int(irow['id'])
            
            db.run("""
                UPDATE inventory SET quantity = MAX(0.0, quantity - :q) WHERE id = :iid AND company_id = :c
            """, {'q': w_qty, 'iid': iid, 'c': company['id']})
            
            db.run("""
                INSERT INTO stock_movements(company_id, inventory_item_id, movement_type, quantity, unit_cost, reference, reason, created_by)
                VALUES(:c, :iid, 'Wastage', :q, :co, 'WASTE-LOG', :r, :u)
            """, {'c': company['id'], 'iid': iid, 'q': -w_qty, 'co': float(irow['unit_cost']), 'r': f"{w_reason}: {w_notes}", 'u': u['id']})
            
            st.error(f"Wastage recorded: -{w_qty} {irow['unit']} deducted from {waste_item}.")
            st.rerun()

# ---------------------------------------------------------
# Page 16: Suppliers Directory
# ---------------------------------------------------------
elif current_page == "Suppliers Directory":
    st.title("🏢 Supplier Directory & Purchasing Contacts")
    
    t1, t2 = st.tabs(["📋 Supplier Directory", "➕ Add New Supplier"])
    
    with t1:
        sup_df = db.read("SELECT * FROM suppliers WHERE company_id = :c ORDER BY name", {'c': company['id']})
        st.dataframe(sup_df.drop(columns=['id', 'company_id']), use_container_width=True, hide_index=True)
        
    with t2:
        with st.form("new_supplier_form"):
            s_name = st.text_input("Supplier Name *", placeholder="e.g. Koala Butchery & Meats")
            s_cat = st.selectbox("Category", ["Poultry & Meat", "Fresh Produce & Vegetables", "Grains & Bakery", "Beverages & Liquor", "Packaging & Consumables", "Utilities & Services"])
            s_contact = st.text_input("Contact Person")
            
            c1, c2 = st.columns(2)
            with c1:
                s_phone = st.text_input("Phone Number", "+263 ")
            with c2:
                s_email = st.text_input("Email Address", "orders@supplier.co.zw")
            s_tax = st.text_input("ZIMRA Tax Clearance / TIN (ITF 263)")
            sub_sup = st.form_submit_button("Save Supplier", type="primary")
            
        if sub_sup and s_name:
            db.run("""
                INSERT INTO suppliers(company_id, name, contact_person, phone, email, tax_id, category)
                VALUES(:c, :n, :cp, :p, :e, :t, :cat)
            """, {'c': company['id'], 'n': s_name.strip(), 'cp': s_contact, 'p': s_phone, 'e': s_email, 't': s_tax, 'cat': s_cat})
            st.success(f"Supplier '{s_name}' registered!")
            st.rerun()

# ---------------------------------------------------------
# Page 17: Expenses Tracker
# ---------------------------------------------------------
elif current_page == "Expenses Tracker":
    st.title("💵 Restaurant Expenses & Purchases Tracker")
    
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
        st.metric("Total Expenses Logged", f"${tot_exp:,.2f}", f"ZiG {tot_exp*zig_rate:,.2f}")
        
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
                e_pay_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Ecocash / Mobile Money", "Card"])
                
            c3, c4 = st.columns(2)
            with c3:
                e_supplier = st.text_input("Supplier / Vendor Name")
            with c4:
                e_receipt = st.text_input("Receipt / Invoice Number")
                
            sub_exp = st.form_submit_button("Record Expense", type="primary")
            
        if sub_exp and e_desc:
            eid = db.execute_insert("""
                INSERT INTO expenses(company_id, branch_id, expense_date, category, description, amount, supplier, payment_method, receipt_no, tax_deductible, created_by)
                VALUES(:c, 1, :d, :cat, :desc, :amt, :sup, :pm, :rec, 1, :u)
            """, {
                'c': company['id'], 'd': str(e_date), 'cat': e_cat, 'desc': e_desc,
                'amt': e_amt, 'sup': e_supplier, 'pm': e_pay_method, 'rec': e_receipt, 'u': u['id']
            })
            st.success(f"Expense of ${e_amt:,.2f} recorded!")
            st.rerun()

# ---------------------------------------------------------
# Page 18: IFRS 18 Financial Statements
# ---------------------------------------------------------
elif current_page == "IFRS 18 Financial Statements":
    st.title("💼 IFRS 18 Financial Statements & Statutory Reports")
    
    fc1, fc2 = st.columns(2)
    with fc1:
        f_start = st.date_input("Period Start", date(date.today().year, 1, 1))
    with fc2:
        f_end = st.date_input("Period End", date.today())
        
    period_str = f"{f_start.strftime('%d-%b-%Y')} to {f_end.strftime('%d-%b-%Y')}"
    
    sales_res = db.read("""
        SELECT COALESCE(SUM(subtotal), 0) AS rev, COALESCE(SUM(discount), 0) AS disc
        FROM sales WHERE company_id = :c AND sale_date BETWEEN :d1 AND :d2
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    net_revenue = float(sales_res.iloc[0]['rev']) - float(sales_res.iloc[0]['disc'])
    
    cogs_res = db.read("""
        SELECT COALESCE(SUM(sl.quantity * mi.cost), 0) AS cogs
        FROM sale_lines sl JOIN menu_items mi ON mi.id = sl.item_id JOIN sales s ON s.id = sl.sale_id
        WHERE s.company_id = :c AND s.sale_date BETWEEN :d1 AND :d2
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    cost_of_sales = float(cogs_res.iloc[0]['cogs'])
    gross_profit = net_revenue - cost_of_sales
    
    exp_res = db.read("""
        SELECT category, COALESCE(SUM(amount), 0) AS cat_amt
        FROM expenses WHERE company_id = :c AND expense_date BETWEEN :d1 AND :d2
        GROUP BY category
    """, {'c': company['id'], 'd1': str(f_start), 'd2': str(f_end)})
    total_operating_expenses = float(exp_res['cat_amt'].sum()) if len(exp_res) else 0.0
    operating_profit = gross_profit - total_operating_expenses
    financing_costs = total_operating_expenses * 0.02
    profit_before_tax = operating_profit - financing_costs
    income_tax_expense = max(0.0, profit_before_tax * 0.2472) if profit_before_tax > 0 else 0.0
    profit_for_period = profit_before_tax - income_tax_expense
    
    st_tabs = st.tabs([
        "1️⃣ Statement of Profit or Loss (IFRS 18)",
        "2️⃣ Statement of Financial Position (Balance Sheet)",
        "3️⃣ Cash Flow Statement",
        "4️⃣ Management Performance Measures (MPMs)"
    ])
    
    with st_tabs[0]:
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
        
        pnl_pdf = pdf_gen.generate_financial_report_pdf(company, pnl_df, period_str=period_str)
        st.download_button(
            label="📄 Download Official IFRS 18 Financial Statements (PDF)",
            data=pnl_pdf,
            file_name=f"Financial_Statements_{f_start}_{f_end}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
    with st_tabs[1]:
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
            ("Equity: Retained Earnings / Current Surplus", retained_earnings),
            ("TOTAL EQUITY & LIABILITIES", tot_liab + share_capital + retained_earnings)
        ]
        bs_df = pd.DataFrame(bs_lines, columns=["Balance Sheet Line Item", f"Amount ({curr})"])
        st.dataframe(bs_df, use_container_width=True, hide_index=True)
        
    with st_tabs[2]:
        cf_lines = [
            ("Cash Receipts from Restaurant Customers", net_revenue),
            ("Cash Payments to Food Suppliers & Vendors", -(cost_of_sales * 0.8)),
            ("Cash Payments for Operating Expenses & Utilities", -total_operating_expenses),
            ("NET CASH FLOW FROM OPERATING ACTIVITIES", net_revenue - (cost_of_sales * 0.8) - total_operating_expenses),
            ("Cash Flows from Investing Activities: Equipment Purchases", 0.0),
            ("Cash Flows from Financing Activities: Capital Contributions", 0.0),
            ("NET INCREASE IN CASH AND CASH EQUIVALENTS", net_revenue - (cost_of_sales * 0.8) - total_operating_expenses)
        ]
        cf_df = pd.DataFrame(cf_lines, columns=["Cash Flow Line Item", f"Amount ({curr})"])
        st.dataframe(cf_df, use_container_width=True, hide_index=True)
        
    with st_tabs[3]:
        food_cost_margin = (cost_of_sales / net_revenue * 100) if net_revenue > 0 else 0.0
        gross_margin = (gross_profit / net_revenue * 100) if net_revenue > 0 else 0.0
        ebitda_margin = (operating_profit / net_revenue * 100) if net_revenue > 0 else 0.0
        
        mpm1, mpm2, mpm3 = st.columns(3)
        mpm1.metric("Gross Profit Margin", f"{gross_margin:.1f}%", "Target: >65%")
        mpm2.metric("Food Cost % (COGS)", f"{food_cost_margin:.1f}%", "Target: <32%", delta_color="inverse")
        mpm3.metric("Operating EBITDA Margin", f"{ebitda_margin:.1f}%", "Target: >20%")

# ---------------------------------------------------------
# Page 19: General Ledger Journals
# ---------------------------------------------------------
elif current_page == "General Ledger Journals":
    st.title("⚖️ Double-Entry General Ledger Journals")
    
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
            
    with t2:
        accounts_df = db.read("SELECT id, code, name, account_type FROM accounts WHERE company_id = :c ORDER BY code", {'c': company['id']})
        acc_dict = {int(r['id']): f"{r['code']} - {r['name']} ({r['account_type']})" for _, r in accounts_df.iterrows()}
        
        with st.form("journal_entry_form"):
            jc1, jc2 = st.columns(2)
            with jc1:
                j_date = st.date_input("Entry Date", date.today())
                j_ref = st.text_input("Reference *", f"JV-{datetime.now():%Y%m%d%H%M}")
            with jc2:
                j_desc = st.text_input("Description *", "Period end adjustment")
                
            d_col1, d_col2 = st.columns([3, 2])
            with d_col1:
                debit_acc = st.selectbox("Debit Account *", options=list(acc_dict.keys()), format_func=lambda x: acc_dict[x], key="deb_acc")
            with d_col2:
                debit_amt = st.number_input(f"Debit Amount ({curr}) *", min_value=0.01, value=100.0, step=10.0, key="deb_amt")
                
            c_col1, c_col2 = st.columns([3, 2])
            with c_col1:
                credit_acc = st.selectbox("Credit Account *", options=list(acc_dict.keys()), format_func=lambda x: acc_dict[x], key="cred_acc", index=min(1, len(acc_dict)-1))
            with c_col2:
                credit_amt = st.number_input(f"Credit Amount ({curr}) *", min_value=0.01, value=100.0, step=10.0, key="cred_amt")
                
            is_balanced = round(debit_amt, 2) == round(credit_amt, 2)
            if not is_balanced:
                st.error(f"❌ Journal is out of balance! Difference: ${abs(debit_amt - credit_amt):,.2f}")
            else:
                st.success("✅ Journal is balanced (Debits = Credits)")
                
            sub_jv = st.form_submit_button("Post Journal Entry", type="primary")
            
        if sub_jv and is_balanced and debit_acc != credit_acc:
            jid = db.execute_insert("""
                INSERT INTO journals(company_id, entry_date, reference, description, status, created_by)
                VALUES(:c, :d, :r, :desc, 'posted', :u)
            """, {'c': company['id'], 'd': str(j_date), 'r': j_ref, 'desc': j_desc, 'u': u['id']})
            
            db.run("""
                INSERT INTO journal_lines(journal_id, account_id, debit, credit)
                VALUES(:jid, :acc, :deb, 0.0), (:jid, :cracc, 0.0, :cred)
            """, {'jid': jid, 'acc': debit_acc, 'deb': debit_amt, 'cracc': credit_acc, 'cred': credit_amt})
            
            st.success(f"Journal {j_ref} posted successfully!")
            st.rerun()

# ---------------------------------------------------------
# Page 20: Chart of Accounts
# ---------------------------------------------------------
elif current_page == "Chart of Accounts":
    st.title("📚 IFRS Chart of Accounts")
    accounts_df = db.read("SELECT code, name, account_type, ifrs_category, balance, active FROM accounts WHERE company_id = :c ORDER BY code", {'c': company['id']})
    st.dataframe(accounts_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 21: Statutory Payroll Processor
# ---------------------------------------------------------
elif current_page == "Statutory Payroll Processor":
    st.title("🏛️ Zimbabwe Statutory Payroll Processor")
    
    employees_df = db.read("SELECT * FROM employees WHERE company_id = :c AND active = 1 ORDER BY employee_no", {'c': company['id']})
    payroll_month = st.selectbox("Payroll Month", ["October 2026", "September 2026", "August 2026", "November 2026"])
    
    payroll_records = []
    total_gross = total_paye = total_nssa = total_net = 0.0
    
    for _, emp in employees_df.iterrows():
        slip = tc.compute_employee_payslip(emp['full_name'], emp['employee_no'], float(emp['salary']), float(emp['allowances']))
        payroll_records.append(slip)
        total_gross += slip['gross_earnings']
        total_paye += slip['total_paye']
        total_nssa += (slip['nssa_employee'] + slip['nssa_employer'])
        total_net += slip['net_pay']
        
    pr_df = pd.DataFrame(payroll_records)
    
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("Gross Payroll", f"${total_gross:,.2f}")
    pc2.metric("ZIMRA PAYE", f"${total_paye:,.2f}")
    pc3.metric("NSSA Remittance", f"${total_nssa:,.2f}")
    pc4.metric("Net Disbursed", f"${total_net:,.2f}")
    
    st.markdown("---")
    st.dataframe(
        pr_df[['employee_no', 'employee_name', 'basic_salary', 'allowances', 'gross_earnings', 'nssa_employee', 'base_paye', 'aids_levy', 'total_paye', 'net_pay']],
        use_container_width=True,
        hide_index=True
    )
    
    sel_emp = st.selectbox("Select Employee for Payslip PDF", pr_df['employee_name'].tolist())
    if sel_emp:
        slip_data = pr_df[pr_df['employee_name'] == sel_emp].iloc[0].to_dict()
        payslip_pdf = pdf_gen.generate_payslip_pdf(company, slip_data, payroll_month)
        st.download_button(
            label=f"📄 Download Confidential Payslip for {sel_emp} (PDF)",
            data=payslip_pdf,
            file_name=f"Payslip_{slip_data['employee_no']}.pdf",
            mime="application/pdf",
            type="primary"
        )

# ---------------------------------------------------------
# Page 22: ZIMRA Tax & Statutory Hub
# ---------------------------------------------------------
elif current_page == "ZIMRA Tax & Statutory Hub":
    st.title("🏛️ ZIMRA Tax & Statutory Compliance Hub")
    
    sales_vat = db.read("SELECT COALESCE(SUM(subtotal), 0) AS sub, COALESCE(SUM(tax), 0) AS vat FROM sales WHERE company_id = :c", {'c': company['id']})
    taxable_sales = float(sales_vat.iloc[0]['sub'])
    output_vat = float(sales_vat.iloc[0]['vat'])
    
    exp_vat = db.read("SELECT COALESCE(SUM(amount), 0) AS exp FROM expenses WHERE company_id = :c AND tax_deductible = 1", {'c': company['id']})
    taxable_purchases = float(exp_vat.iloc[0]['exp'])
    input_vat = round(taxable_purchases * 0.15, 2)
    net_vat_payable = output_vat - input_vat
    
    vc1, vc2, vc3 = st.columns(3)
    vc1.metric("Output VAT (Sales)", f"${output_vat:,.2f}")
    vc2.metric("Input VAT (Expenses)", f"${input_vat:,.2f}")
    vc3.metric("Net VAT Payable", f"${net_vat_payable:,.2f}", delta_color="inverse")
    
    st.markdown("---")
    vat_summary_table = pd.DataFrame([
        ("Box 1: Total Standard Rated Supplies (Net Sales)", taxable_sales),
        ("Box 2: Output VAT Charged to Customers (15%)", output_vat),
        ("Box 3: Total Allowable Taxable Purchases & Expenses", taxable_purchases),
        ("Box 4: Input VAT Claimable on Invoices (15%)", input_vat),
        ("Box 5: NET VAT PAYABLE / (REFUND) TO ZIMRA", net_vat_payable)
    ], columns=["ZIMRA VAT 7 Section", f"Amount ({curr})"])
    st.dataframe(vat_summary_table, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 23: Organisation Structure
# ---------------------------------------------------------
elif current_page == "Organisation Structure":
    st.title("🏛️ Organisation Structure & Directorates")
    org_units = db.read("SELECT * FROM organisation_units WHERE company_id = :c ORDER BY unit_type, name", {'c': company['id']})
    directorates = org_units[org_units['unit_type'] == 'Directorate']
    
    d_cols = st.columns(3)
    for idx, (_, d_row) in enumerate(directorates.iterrows()):
        with d_cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### 🏢 {d_row['name']}")
                st.caption(d_row.get('description', 'Operational Directorate'))
                st.markdown("✅ **Active Directorate**")
                
    st.markdown("---")
    st.subheader("Departmental Units")
    st.dataframe(org_units.drop(columns=['id', 'company_id', 'parent_id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 24: Staff Directory
# ---------------------------------------------------------
elif current_page == "Staff Directory":
    st.title("👥 Staff Directory & Employee Management")
    staff_df = db.read("""
        SELECT e.id, e.employee_no, e.full_name, e.job_title, b.name AS branch_name,
               e.salary, e.allowances, e.national_id, e.nssa_number, e.hire_date, e.active
        FROM employees e LEFT JOIN branches b ON b.id = e.branch_id WHERE e.company_id = :c ORDER BY e.employee_no
    """, {'c': company['id']})
    st.dataframe(staff_df.drop(columns=['id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 25: Customer CRM & Loyalty
# ---------------------------------------------------------
elif current_page == "Customer CRM & Loyalty":
    st.title("🤝 Customer CRM & Loyalty Programs")
    cust_df = db.read("""
        SELECT c.id, c.name, c.phone, c.email, c.loyalty_points, c.notes,
               COUNT(s.id) AS total_visits, COALESCE(SUM(s.total), 0) AS lifetime_spend
        FROM customers c LEFT JOIN sales s ON s.customer_id = c.id WHERE c.company_id = :c
        GROUP BY c.id, c.name, c.phone, c.email, c.loyalty_points, c.notes ORDER BY lifetime_spend DESC
    """, {'c': company['id']})
    st.dataframe(cust_df.drop(columns=['id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 26: User Administration & RBAC
# ---------------------------------------------------------
elif current_page == "User Administration & RBAC":
    st.title("👤 User Administration & Access Control")
    if u['role'] not in ('admin', 'manager'):
        st.error("⛔ Administrator or Top-Management access required.")
        st.stop()
    users_df = db.read("SELECT id, username, full_name, role, active, created_at FROM users WHERE company_id = :c ORDER BY id", {'c': company['id']})
    st.dataframe(users_df.drop(columns=['id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 27: System Audit Trail
# ---------------------------------------------------------
elif current_page == "System Audit Trail":
    st.title("🛡️ Central System Audit Trail")
    audit_df = db.read("""
        SELECT a.id, a.created_at AS timestamp, u.full_name AS user, a.action, a.entity, a.entity_id, a.detail
        FROM audit_log a LEFT JOIN users u ON u.id = a.user_id WHERE a.company_id = :c ORDER BY a.id DESC LIMIT 100
    """, {'c': company['id']})
    st.dataframe(audit_df.drop(columns=['id']), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Page 28: Settings & Configuration
# ---------------------------------------------------------
elif current_page == "Settings & Configuration":
    st.title("⚙️ Restaurant Profile & ERP Settings")
    if u['role'] not in ('admin', 'manager'):
        st.error("⛔ Administrator access required.")
        st.stop()
        
    with st.form("restaurant_settings_form"):
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
            st_curr = st.selectbox("Functional Base Currency", ["USD", "ZiG", "ZAR", "GBP", "EUR"], index=0)
            
        sub_sett = st.form_submit_button("Save Settings", type="primary")
        
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
        st.success("Settings saved successfully!")
        st.rerun()
