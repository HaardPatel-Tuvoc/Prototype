import streamlit as st
import pandas as pd
from datetime import datetime, date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Continente – Order Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme detection (Streamlit does not expose data-theme on DOM) ─────────────
IS_DARK = st.context.theme.type == "dark"

# ── Custom CSS ───────────────────────────────────────────────────────────────
_LIGHT_CSS = """
.block-container { padding-top: 1.5rem; }
div[data-testid="stMetric"] {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 12px 16px;
}
.profile-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
    color: white !important;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 1rem;
}
.profile-card h2 { margin: 0 0 4px 0; font-size: 1.6rem; color: white !important; }
.profile-card p  { margin: 2px 0; opacity: 0.85; font-size: 0.95rem; color: white !important; }
.profile-card strong { color: white !important; }
.notif-card {
    border-left: 4px solid #2d5986;
    background: #f8f9fa;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #212529;
}
.notif-card span { color: #212529; }
.notif-card.promo  { border-left-color: #e67e22; }
.notif-card.alert  { border-left-color: #e74c3c; }
.notif-card.ship   { border-left-color: #27ae60; }
.notif-card.news   { border-left-color: #8e44ad; }
.success-box {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 20px 24px;
    color: #155724;
}
.success-box h3, .success-box p { color: #155724; }
"""

_DARK_CSS = """
div[data-testid="stMetric"] {
    background: #262730 !important;
    border: 1px solid #464854 !important;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #fafafa !important;
}
.notif-card {
    background: #262730 !important;
    border: 1px solid #464854 !important;
    border-left-width: 4px !important;
    color: #fafafa !important;
}
.notif-card strong, .notif-card span { color: #fafafa !important; }
.notif-card.promo  { border-left-color: #e67e22 !important; }
.notif-card.alert  { border-left-color: #e74c3c !important; }
.notif-card.ship   { border-left-color: #27ae60 !important; }
.notif-card.news   { border-left-color: #8e44ad !important; }
.success-box {
    background: #1a3d2e !important;
    border: 1px solid #2d6a4f !important;
    color: #b7e4c7 !important;
}
.success-box h3, .success-box p { color: #b7e4c7 !important; }
"""

st.markdown(
    f"<style>{_LIGHT_CSS}{_DARK_CSS if IS_DARK else ''}</style>",
    unsafe_allow_html=True,
)

# ── Mock data ────────────────────────────────────────────────────────────────
CUSTOMER = {
    "name": "Continente",
    "code": "CUST-001",
    "salesperson": "João Silva",
    "payment_terms": "30 Days",
    "last_order_date": date(2026, 5, 20),
}

PRODUCTS = [
    {"product_code": "PEN-001", "product_name": "Uni-ball Signo 207", "color": "Black", "brand": "Mitsubishi Pencil", "pack_unit": "Box/12", "stock_status": "In Stock", "unit_price": 1.85},
    {"product_code": "PEN-002", "product_name": "Uni-ball Signo 207", "color": "Blue", "brand": "Mitsubishi Pencil", "pack_unit": "Box/12", "stock_status": "In Stock", "unit_price": 1.85},
    {"product_code": "PEN-003", "product_name": "Uni-ball Signo 207", "color": "Red", "brand": "Mitsubishi Pencil", "pack_unit": "Box/12", "stock_status": "Low Stock", "unit_price": 1.85},
    {"product_code": "PEN-004", "product_name": "Pilot G2 Gel Pen", "color": "Black", "brand": "Pilot", "pack_unit": "Box/12", "stock_status": "In Stock", "unit_price": 1.45},
    {"product_code": "PEN-005", "product_name": "Pilot G2 Gel Pen", "color": "Blue", "brand": "Pilot", "pack_unit": "Box/12", "stock_status": "In Stock", "unit_price": 1.45},
    {"product_code": "PEN-006", "product_name": "Pilot G2 Gel Pen", "color": "Green", "brand": "Pilot", "pack_unit": "Box/12", "stock_status": "Out of Stock", "unit_price": 1.45},
    {"product_code": "NBK-001", "product_name": "Rhodia Webnotebook A5", "color": "Orange", "brand": "Rhodia", "pack_unit": "Unit", "stock_status": "In Stock", "unit_price": 8.50},
    {"product_code": "NBK-002", "product_name": "Rhodia Webnotebook A5", "color": "Black", "brand": "Rhodia", "pack_unit": "Unit", "stock_status": "In Stock", "unit_price": 8.50},
    {"product_code": "MRK-001", "product_name": "Posca PC-5M Marker", "color": "White", "brand": "Posca", "pack_unit": "Box/6", "stock_status": "In Stock", "unit_price": 3.20},
    {"product_code": "MRK-002", "product_name": "Posca PC-5M Marker", "color": "Black", "brand": "Posca", "pack_unit": "Box/6", "stock_status": "In Stock", "unit_price": 3.20},
    {"product_code": "MRK-003", "product_name": "Posca PC-5M Marker", "color": "Red", "brand": "Posca", "pack_unit": "Box/6", "stock_status": "Low Stock", "unit_price": 3.20},
    {"product_code": "PCL-001", "product_name": "Uni Kuru Toga Mechanical Pencil", "color": "Silver", "brand": "Mitsubishi Pencil", "pack_unit": "Unit", "stock_status": "In Stock", "unit_price": 6.75},
    {"product_code": "PCL-002", "product_name": "Uni Kuru Toga Mechanical Pencil", "color": "Blue", "brand": "Mitsubishi Pencil", "pack_unit": "Unit", "stock_status": "In Stock", "unit_price": 6.75},
    {"product_code": "ERZ-001", "product_name": "Staedtler Mars Plastic Eraser", "color": "White", "brand": "Staedtler", "pack_unit": "Box/20", "stock_status": "In Stock", "unit_price": 0.65},
    {"product_code": "HGL-001", "product_name": "Stabilo Boss Highlighter", "color": "Yellow", "brand": "Stabilo", "pack_unit": "Box/10", "stock_status": "In Stock", "unit_price": 1.10},
    {"product_code": "HGL-002", "product_name": "Stabilo Boss Highlighter", "color": "Pink", "brand": "Stabilo", "pack_unit": "Box/10", "stock_status": "In Stock", "unit_price": 1.10},
]

CURRENT_ORDERS = [
    {"Order No": "ORD-2026-00042", "Date": "2026-05-18", "Status": "Processing", "Total Items": 240, "Shipped Items": 120, "Pending Items": 120, "Tracking Status": "Partial Shipment"},
    {"Order No": "ORD-2026-00038", "Date": "2026-05-10", "Status": "Confirmed", "Total Items": 500, "Shipped Items": 0, "Pending Items": 500, "Tracking Status": "Awaiting Dispatch"},
    {"Order No": "ORD-2026-00035", "Date": "2026-05-05", "Status": "Shipped", "Total Items": 144, "Shipped Items": 144, "Pending Items": 0, "Tracking Status": "In Transit"},
]

OLD_ORDERS = [
    {"Order No": "ORD-2026-00030", "Date": "2026-04-22", "Status": "Delivered", "Invoice No": "INV-2026-00891", "Total Amount": "€ 892.40"},
    {"Order No": "ORD-2026-00025", "Date": "2026-04-08", "Status": "Delivered", "Invoice No": "INV-2026-00754", "Total Amount": "€ 1,245.00"},
    {"Order No": "ORD-2026-00019", "Date": "2026-03-15", "Status": "Delivered", "Invoice No": "INV-2026-00612", "Total Amount": "€ 567.80"},
    {"Order No": "ORD-2026-00012", "Date": "2026-02-28", "Status": "Delivered", "Invoice No": "INV-2026-00498", "Total Amount": "€ 2,100.50"},
    {"Order No": "ORD-2026-00008", "Date": "2026-02-10", "Status": "Delivered", "Invoice No": "INV-2026-00387", "Total Amount": "€ 430.00"},
]

NOTIFICATIONS = [
    {"type": "news", "icon": "🆕", "title": "New Product Launch", "message": "Uni-ball One Gel Pen range now available – exclusive preview for Continente.", "date": "2026-05-25"},
    {"type": "promo", "icon": "⏰", "title": "Promotion Ending Soon", "message": "Mitsubishi Pencil brand promotion ends on 31 May 2026. Place your order now to benefit.", "date": "2026-05-24"},
    {"type": "ship", "icon": "🚚", "title": "Shipment Update", "message": "Order ORD-2026-00035 has been dispatched. Expected delivery: 28 May 2026.", "date": "2026-05-23"},
    {"type": "alert", "icon": "⚠️", "title": "Backorder Alert", "message": "Pilot G2 Gel Pen (Green) – PEN-006 is currently out of stock. Estimated restock: 10 Jun 2026.", "date": "2026-05-22"},
    {"type": "news", "icon": "📰", "title": "Exhibition / Company News", "message": "Visit us at Paperworld Frankfurt 2026 – Hall 4.1, Stand B22. Exclusive show offers available.", "date": "2026-05-20"},
]

DISCOUNT_RULES = [
    {"Rule": "Volume Discount – Tier 1", "Description": "3% discount on orders of 144 units or more", "Applies To": "All products"},
    {"Rule": "Volume Discount – Tier 2", "Description": "5% discount on orders of 500 units or more", "Applies To": "All products"},
    {"Rule": "Brand Promotion", "Description": "Additional 2% off all Mitsubishi Pencil products (cumulative with volume discount)", "Applies To": "Mitsubishi Pencil brand"},
    {"Rule": "Payment Terms", "Description": "Standard 30-day payment terms as per PHC agreement", "Applies To": "Account-wide"},
]

MITSUBISHI_BRAND = "Mitsubishi Pencil"
MITSUBISHI_EXTRA_DISCOUNT = 0.02


# ── Session state init ───────────────────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "order_submitted" not in st.session_state:
    st.session_state.order_submitted = False
if "submitted_order_no" not in st.session_state:
    st.session_state.submitted_order_no = ""


# ── Helpers ──────────────────────────────────────────────────────────────────
def calc_discount(total_qty: int) -> float:
    if total_qty >= 500:
        return 0.05
    if total_qty >= 144:
        return 0.03
    return 0.0


def stock_badge(status: str) -> str:
    colors = {"In Stock": "🟢", "Low Stock": "🟡", "Out of Stock": "🔴"}
    return f"{colors.get(status, '⚪')} {status}"


def filter_products(query: str) -> list:
    if not query.strip():
        return PRODUCTS
    q = query.lower()
    return [
        p for p in PRODUCTS
        if q in p["product_code"].lower()
        or q in p["product_name"].lower()
        or q in p["color"].lower()
        or q in p["brand"].lower()
    ]


def notif_card_html(notif: dict) -> str:
    border_colors = {
        "promo": "#e67e22",
        "alert": "#e74c3c",
        "ship": "#27ae60",
        "news": "#8e44ad",
    }
    left = border_colors.get(notif["type"], "#2d5986")
    if IS_DARK:
        box = f"background:#262730;border:1px solid #464854;border-left:4px solid {left};color:#fafafa;"
        text = "color:#fafafa;"
    else:
        box = f"background:#f8f9fa;border-left:4px solid {left};color:#212529;"
        text = "color:#212529;"
    return f"""
    <div class="notif-card {notif['type']}" style="border-radius:6px;padding:14px 18px;margin-bottom:10px;{box}">
        <strong style="{text}">{notif['icon']} {notif['title']}</strong>
        <span style="float:right;opacity:0.6;font-size:0.85rem;{text}">{notif['date']}</span><br>
        <span style="font-size:0.93rem;{text}">{notif['message']}</span>
    </div>
    """


def success_box_html(order_no: str) -> str:
    if IS_DARK:
        box = "background:#1a3d2e;border:1px solid #2d6a4f;"
        text = "color:#b7e4c7;"
    else:
        box = "background:#d4edda;border:1px solid #c3e6cb;"
        text = "color:#155724;"
    return f"""
    <div class="success-box" style="border-radius:8px;padding:20px 24px;{box}{text}">
        <h3 style="margin:0 0 8px 0;{text}">✅ Order Submitted Successfully</h3>
        <p style="margin:4px 0;{text}"><strong>Order No:</strong> {order_no}</p>
        <p style="margin:4px 0;{text}"><strong>PHC Sync Status:</strong> Pending Sync</p>
    </div>
    """


def build_cart_summary(cart: dict) -> pd.DataFrame:
    rows = []
    for code, qty in cart.items():
        if qty <= 0:
            continue
        prod = next(p for p in PRODUCTS if p["product_code"] == code)
        line_total = prod["unit_price"] * qty
        rows.append({
            "Code": code,
            "Product": prod["product_name"],
            "Color": prod["color"],
            "Brand": prod["brand"],
            "Unit Price": f"€ {prod['unit_price']:.2f}",
            "Qty": qty,
            "Line Total": line_total,
        })
    return pd.DataFrame(rows)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="profile-card">
        <h2>📦 {CUSTOMER['name']} – B2B Order Portal</h2>
        <p>Customer Code: <strong>{CUSTOMER['code']}</strong> &nbsp;|&nbsp;
           Salesperson: <strong>{CUSTOMER['salesperson']}</strong> &nbsp;|&nbsp;
           Payment Terms: <strong>{CUSTOMER['payment_terms']}</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_dash, tab_new, tab_current, tab_old, tab_notif, tab_disc = st.tabs([
    "🏠 Dashboard",
    "🛒 New Order",
    "📋 Current Orders",
    "📁 Old Orders",
    "🔔 Notifications",
    "🏷️ Discounts",
])

# ── 1. Dashboard ─────────────────────────────────────────────────────────────
with tab_dash:
    st.subheader("Customer Profile")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customer Name", CUSTOMER["name"])
    c2.metric("Customer Code", CUSTOMER["code"])
    c3.metric("Salesperson", CUSTOMER["salesperson"])
    c4.metric("Payment Terms", CUSTOMER["payment_terms"])

    st.divider()

    active_orders = len(CURRENT_ORDERS)
    pending_items = sum(o["Pending Items"] for o in CURRENT_ORDERS)
    promotions = len([n for n in NOTIFICATIONS if n["type"] == "promo"])
    last_order = CUSTOMER["last_order_date"].strftime("%d %b %Y")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Orders", active_orders)
    m2.metric("Pending Items", pending_items)
    m3.metric("Available Promotions", promotions)
    m4.metric("Last Order Date", last_order)

    st.divider()
    st.subheader("Recent Activity")
    recent = pd.DataFrame(CURRENT_ORDERS[:2])[["Order No", "Date", "Status", "Tracking Status"]]
    st.dataframe(recent, use_container_width=True, hide_index=True)

# ── 2. New Order ─────────────────────────────────────────────────────────────
with tab_new:
    st.subheader("Place a New Order")

    if st.session_state.order_submitted:
        st.markdown(success_box_html(st.session_state.submitted_order_no), unsafe_allow_html=True)
        if st.button("Place Another Order"):
            st.session_state.order_submitted = False
            st.session_state.cart = {}
            st.rerun()
    else:
        search = st.text_input("🔍 Search products", placeholder="Search by code, name, color, or brand…")

        filtered = filter_products(search)
        st.caption(f"{len(filtered)} product(s) found")

        if filtered:
            header_cols = st.columns([0.5, 1.2, 2.5, 1, 1.5, 1, 1.2, 1])
            headers = ["Select", "Code", "Product Name", "Color", "Brand", "Pack", "Stock", "Unit Price"]
            for col, h in zip(header_cols, headers):
                col.markdown(f"**{h}**")

            st.divider()

            for prod in filtered:
                code = prod["product_code"]
                row_cols = st.columns([0.5, 1.2, 2.5, 1, 1.5, 1, 1.2, 1])
                selected = row_cols[0].checkbox("", key=f"sel_{code}", label_visibility="collapsed")
                row_cols[1].write(code)
                row_cols[2].write(prod["product_name"])
                row_cols[3].write(prod["color"])
                row_cols[4].write(prod["brand"])
                row_cols[5].write(prod["pack_unit"])
                row_cols[6].write(stock_badge(prod["stock_status"]))
                row_cols[7].write(f"€ {prod['unit_price']:.2f}")

                if selected:
                    qty = st.number_input(
                        f"Quantity for {code}",
                        min_value=1,
                        value=st.session_state.cart.get(code, 1),
                        step=1,
                        key=f"qty_{code}",
                    )
                    st.session_state.cart[code] = qty
                elif code in st.session_state.cart:
                    del st.session_state.cart[code]

        st.divider()
        st.subheader("Cart Summary")

        cart_df = build_cart_summary(st.session_state.cart)

        if cart_df.empty:
            st.info("No products selected. Search and select products above to build your order.")
        else:
            display_df = cart_df.copy()
            display_df["Line Total"] = display_df["Line Total"].apply(lambda x: f"€ {x:.2f}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            subtotal = cart_df["Line Total"].sum()
            total_qty = int(cart_df["Qty"].sum())
            vol_discount_pct = calc_discount(total_qty)
            vol_discount_amt = subtotal * vol_discount_pct

            mitsu_lines = cart_df[cart_df["Brand"] == MITSUBISHI_BRAND]["Line Total"].sum()
            mitsu_discount_amt = mitsu_lines * MITSUBISHI_EXTRA_DISCOUNT if mitsu_lines > 0 else 0

            total_discount = vol_discount_amt + mitsu_discount_amt
            grand_total = subtotal - total_discount

            s1, s2, s3 = st.columns(3)
            s1.metric("Subtotal", f"€ {subtotal:.2f}")
            s2.metric("Total Quantity", total_qty)
            s3.metric("Grand Total", f"€ {grand_total:.2f}")

            st.markdown("**Discount Breakdown**")
            disc_cols = st.columns(3)
            disc_cols[0].write(f"Volume discount ({vol_discount_pct * 100:.0f}%): **€ {vol_discount_amt:.2f}**")
            if mitsu_discount_amt > 0:
                disc_cols[1].write(f"Mitsubishi Pencil promo (2%): **€ {mitsu_discount_amt:.2f}**")
            disc_cols[2].write(f"Total discount: **€ {total_discount:.2f}**")

            if vol_discount_pct == 0 and total_qty < 144:
                st.caption(f"💡 Order {144 - total_qty} more units to unlock a 3% volume discount.")
            elif vol_discount_pct == 0.03 and total_qty < 500:
                st.caption(f"💡 Order {500 - total_qty} more units to unlock a 5% volume discount.")

            st.divider()
            if st.button("✅ Submit Order", type="primary", use_container_width=True):
                st.session_state.order_submitted = True
                st.session_state.submitted_order_no = "ORD-2026-00045"
                st.rerun()

# ── 3. Current Orders ────────────────────────────────────────────────────────
with tab_current:
    st.subheader("Current Orders")
    df_current = pd.DataFrame(CURRENT_ORDERS)

    status_colors = {
        "Processing": "🔄",
        "Confirmed": "✅",
        "Shipped": "🚚",
    }
    df_display = df_current.copy()
    df_display["Status"] = df_display["Status"].apply(lambda s: f"{status_colors.get(s, '📋')} {s}")

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Active Orders", len(CURRENT_ORDERS))
    c2.metric("Items Shipped", sum(o["Shipped Items"] for o in CURRENT_ORDERS))
    c3.metric("Items Pending", sum(o["Pending Items"] for o in CURRENT_ORDERS))

# ── 4. Old Orders ──────────────────────────────────────────────────────────────
with tab_old:
    st.subheader("Previous Orders")
    df_old = pd.DataFrame(OLD_ORDERS)
    st.dataframe(df_old, use_container_width=True, hide_index=True)

    total_spent = sum(float(o["Total Amount"].replace("€ ", "").replace(",", "")) for o in OLD_ORDERS)
    o1, o2 = st.columns(2)
    o1.metric("Total Delivered Orders", len(OLD_ORDERS))
    o2.metric("Total Spent (Delivered)", f"€ {total_spent:,.2f}")

# ── 5. Notifications ─────────────────────────────────────────────────────────
with tab_notif:
    st.subheader("Notifications")
    st.caption(f"{len(NOTIFICATIONS)} notification(s)")

    for notif in NOTIFICATIONS:
        st.markdown(notif_card_html(notif), unsafe_allow_html=True)

# ── 6. Discounts ───────────────────────────────────────────────────────────────
with tab_disc:
    st.subheader("Customer-Specific Discount Rules")
    st.caption("Terms are fetched from PHC in the real implementation.")

    df_disc = pd.DataFrame(DISCOUNT_RULES)
    st.dataframe(df_disc, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("#### How discounts are applied")
    st.markdown(
        """
        | Condition | Discount |
        |---|---|
        | Order quantity ≥ 144 units | **3%** off subtotal |
        | Order quantity ≥ 500 units | **5%** off subtotal |
        | Mitsubishi Pencil brand items | **Additional 2%** off line total |
        """
    )
    st.info("Volume and brand discounts are cumulative. Payment terms: **30 Days** as per PHC agreement.")

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(f"© {datetime.now().year} Reymon ERP · Portal for {CUSTOMER['name']} ({CUSTOMER['code']}) · Mock prototype – no backend connected")
