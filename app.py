import os
import io
import html
import secrets
from datetime import date, datetime

import bcrypt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


st.set_page_config(
    page_title="Soulfyas Quality Restaurant ERP",
    page_icon="🍽️",
    layout="wide"
)


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    try:
        DATABASE_URL = st.secrets["DATABASE_URL"]
    except Exception:
        DATABASE_URL = None

if not DATABASE_URL:
    st.error(
        "DATABASE_URL is not configured. "
        "Add it under Streamlit Cloud → Manage app → Settings → Secrets."
    )
    st.stop()

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True
)

LOGO = "soulfyas_logo.png"


# ---------------------------------------------------------
# PASSWORD SECURITY
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except Exception:
        return False


# ---------------------------------------------------------
# DATABASE HELPERS
# ---------------------------------------------------------

def execute_sql(sql, parameters=None):
    with engine.begin() as connection:
        return connection.execute(
            text(sql),
            parameters or {}
        )


def read_sql(sql, parameters=None):
    with engine.begin() as connection:
        return pd.read_sql(
            text(sql),
            connection,
            params=parameters or {}
        )


# ---------------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    zimra_tin TEXT DEFAULT '',
    vat_number TEXT DEFAULT '',
    nssa_number TEXT DEFAULT '',
    currency TEXT DEFAULT 'USD',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'employee',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS menu_items (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(18,2) NOT NULL DEFAULT 0,
    cost NUMERIC(18,2) DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS customers (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    item_name TEXT NOT NULL,
    category TEXT,
    unit TEXT,
    quantity NUMERIC(18,4) DEFAULT 0,
    reorder_level NUMERIC(18,4) DEFAULT 0,
    unit_cost NUMERIC(18,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sales (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    invoice_no TEXT UNIQUE NOT NULL,
    sale_date DATE NOT NULL,
    customer_id BIGINT REFERENCES customers(id),
    payment_method TEXT,
    subtotal NUMERIC(18,2),
    tax NUMERIC(18,2),
    total NUMERIC(18,2),
    status TEXT DEFAULT 'Paid',
    created_by BIGINT REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sale_lines (
    id BIGSERIAL PRIMARY KEY,
    sale_id BIGINT REFERENCES sales(id),
    item_id BIGINT REFERENCES menu_items(id),
    quantity NUMERIC(18,4),
    unit_price NUMERIC(18,2),
    line_total NUMERIC(18,2)
);

CREATE TABLE IF NOT EXISTS expenses (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT REFERENCES companies(id),
    expense_date DATE NOT NULL,
    category TEXT,
    description TEXT,
    amount NUMERIC(18,2) NOT NULL,
    supplier TEXT,
    payment_method TEXT,
    created_by BIGINT REFERENCES users(id)
);
"""


def initialise_database():
    with engine.begin() as connection:

        for statement in SCHEMA.split(";"):
            if statement.strip():
                connection.execute(text(statement))

        company = connection.execute(
            text("SELECT id FROM companies ORDER BY id LIMIT 1")
        ).fetchone()

        if not company:
            company_id = connection.execute(
                text("""
                    INSERT INTO companies
                    (name, address, phone, currency)
                    VALUES
                    (:name, :address, :phone, :currency)
                    RETURNING id
                """),
                {
                    "name": "Soulfyas Quality Restaurant",
                    "address": "",
                    "phone": "",
                    "currency": "USD"
                }
            ).scalar_one()
        else:
            company_id = company[0]

        user_count = connection.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar_one()

        if user_count == 0:
            connection.execute(
                text("""
                    INSERT INTO users
                    (company_id, username, full_name, password_hash, role)
                    VALUES
                    (:company_id, :username, :full_name, :password_hash, :role)
                """),
                {
                    "company_id": company_id,
                    "username": "admin",
                    "full_name": "System Administrator",
                    "password_hash": hash_password("ChangeMe123!"),
                    "role": "admin"
                }
            )


initialise_database()


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

def show_login():

    st.title("🍽️ Soulfyas Quality Restaurant")
    st.caption("Restaurant operations and management system")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(
            "Sign in",
            use_container_width=True
        )

    if submitted:

        user = read_sql(
            """
            SELECT *
            FROM users
            WHERE username = :username
            AND active = TRUE
            """,
            {"username": username.strip()}
        )

        if len(user) and verify_password(
            password,
            str(user.iloc[0]["password_hash"])
        ):
            st.session_state.user = user.iloc[0].to_dict()
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.info(
        "First login: admin / ChangeMe123! "
        "Change this password immediately."
    )


if "user" not in st.session_state:
    show_login()
    st.stop()


user = st.session_state.user


# ---------------------------------------------------------
# COMPANY DETAILS
# ---------------------------------------------------------

company = read_sql(
    "SELECT * FROM companies ORDER BY id LIMIT 1"
).iloc[0].to_dict()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

pages = [
    "Dashboard",
    "Point of Sale",
    "Invoices",
    "Menu",
    "Expenses",
    "Inventory",
    "Financial Statements",
    "Customers & Suppliers",
    "User Administration",
    "Settings"
]

with st.sidebar:

    if os.path.exists(LOGO):
        st.image(LOGO, width=150)

    st.caption(
        f"{user['full_name']} · {user['role'].title()}"
    )

    page = st.radio("Navigate", pages)

    if st.button("Sign out"):
        del st.session_state.user
        st.rerun()


st.title(page)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "Dashboard":

    today = str(date.today())

    sales = read_sql(
        """
        SELECT COALESCE(SUM(total), 0) AS value
        FROM sales
        WHERE sale_date = :today
        """,
        {"today": today}
    ).iloc[0]["value"]

    expenses = read_sql(
        """
        SELECT COALESCE(SUM(amount), 0) AS value
        FROM expenses
        WHERE expense_date = :today
        """,
        {"today": today}
    ).iloc[0]["value"]

    orders = read_sql(
        """
        SELECT COUNT(*) AS value
        FROM sales
        WHERE sale_date = :today
        """,
        {"today": today}
    ).iloc[0]["value"]

    a, b, c = st.columns(3)

    a.metric("Today's sales", f"${float(sales):,.2f}")
    b.metric("Today's expenses", f"${float(expenses):,.2f}")
    c.metric("Orders", int(orders))

    st.subheader("Recent invoices")

    st.dataframe(
        read_sql(
            """
            SELECT invoice_no, sale_date, payment_method,
                   subtotal, tax, total, status
            FROM sales
            ORDER BY id DESC
            LIMIT 20
            """
        ),
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------

elif page == "Menu":

    with st.form("menu_form"):

        name = st.text_input("Item name")
        category = st.text_input("Category")
        price = st.number_input("Selling price", min_value=0.0)
        cost = st.number_input("Cost", min_value=0.0)

        submitted = st.form_submit_button("Add menu item")

    if submitted and name:

        execute_sql(
            """
            INSERT INTO menu_items
            (company_id, name, category, price, cost)
            VALUES
            (:company_id, :name, :category, :price, :cost)
            """,
            {
                "company_id": company["id"],
                "name": name,
                "category": category,
                "price": price,
                "cost": cost
            }
        )

        st.success("Menu item added")
        st.rerun()

    st.dataframe(
        read_sql(
            """
            SELECT id, name, category, price, cost, active
            FROM menu_items
            WHERE company_id = :company_id
            ORDER BY category, name
            """,
            {"company_id": company["id"]}
        ),
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# USER ADMINISTRATION
# ---------------------------------------------------------

elif page == "User Administration":

    if user["role"] != "admin":
        st.error("Administrator access required.")
        st.stop()

    with st.form("new_user_form"):

        username = st.text_input("Username")
        full_name = st.text_input("Full name")
        password = st.text_input("Temporary password", type="password")
        role = st.selectbox(
            "Role",
            ["employee", "manager", "admin"]
        )

        submitted = st.form_submit_button("Create employee account")

    if submitted and username and full_name and password:

        execute_sql(
            """
            INSERT INTO users
            (company_id, username, full_name, password_hash, role)
            VALUES
            (:company_id, :username, :full_name, :password_hash, :role)
            """,
            {
                "company_id": company["id"],
                "username": username,
                "full_name": full_name,
                "password_hash": hash_password(password),
                "role": role
            }
        )

        st.success("Employee account created")

    st.dataframe(
        read_sql(
            """
            SELECT id, username, full_name, role, active, created_at
            FROM users
            ORDER BY id
            """
        ),
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

elif page == "Settings":

    if user["role"] != "admin":
        st.error("Administrator access required.")
        st.stop()

    with st.form("settings_form"):

        name = st.text_input(
            "Restaurant name",
            company.get("name", "")
        )

        address = st.text_input(
            "Address",
            company.get("address", "")
        )

        phone = st.text_input(
            "Phone",
            company.get("phone", "")
        )

        zimra_tin = st.text_input(
            "ZIMRA TIN",
            company.get("zimra_tin", "")
        )

        vat_number = st.text_input(
            "VAT number",
            company.get("vat_number", "")
        )

        nssa_number = st.text_input(
            "NSSA number",
            company.get("nssa_number", "")
        )

        submitted = st.form_submit_button("Save settings")

    if submitted:

        execute_sql(
            """
            UPDATE companies
            SET name = :name,
                address = :address,
                phone = :phone,
                zimra_tin = :zimra_tin,
                vat_number = :vat_number,
                nssa_number = :nssa_number
            WHERE id = :company_id
            """,
            {
                "name": name,
                "address": address,
                "phone": phone,
                "zimra_tin": zimra_tin,
                "vat_number": vat_number,
                "nssa_number": nssa_number,
                "company_id": company["id"]
            }
        )

        st.success("Restaurant settings saved")
