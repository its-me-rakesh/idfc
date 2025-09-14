import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IDFC Credit Card - Decline Assist", layout="centered")

# ---- Mock Data ----
declines = [
    {
        "merchant": "Swiggy",
        "amount": 2450,
        "reason": "Insufficient Balance",
        "code": "INSUFFICIENT_LIMIT",
        "time": datetime.now().strftime("%H:%M:%S")
    },
    {
        "merchant": "Amazon",
        "amount": 1299,
        "reason": "Online usage disabled",
        "code": "CARD_CONTROL",
        "time": datetime.now().strftime("%H:%M:%S")
    },
    {
        "merchant": "Zomato",
        "amount": 560,
        "reason": "Incorrect PIN entered",
        "code": "PIN_ERROR",
        "time": datetime.now().strftime("%H:%M:%S")
    },
    {
        "merchant": "Netflix",
        "amount": 499,
        "reason": "Invalid CVV",
        "code": "INVALID_CREDENTIALS",
        "time": datetime.now().strftime("%H:%M:%S")
    }
]

# ---- Title ----
st.markdown("<h2 style='text-align: center;'>💳 IDFC Credit Card – Decline Assist</h2>", unsafe_allow_html=True)
st.write("Smart, real-time help for declined transactions.\n---")

# ---- Tabs for Decline Categories ----
tab1, tab2, tab3, tab4 = st.tabs(
    ["⚠️ Insufficient Balance", "🔒 Card Controls", "🔑 PIN Issues", "🆘 Invalid Credentials"]
)

# ---- Tab 1: Insufficient Balance ----
with tab1:
    for d in [x for x in declines if x["code"] == "INSUFFICIENT_LIMIT"]:
        st.markdown(
            f"""
            <div style="border-radius:15px; padding:15px; background-color:#ffe8e8; margin-bottom:15px;">
                <h4>❌ Payment Declined at {d['merchant']}</h4>
                <p><b>Amount:</b> ₹{d['amount']} | <b>Time:</b> {d['time']}</p>
                <p><b>Reason:</b> {d['reason']}</p>
            </div>
            """, unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        if col1.button(f"💰 Pay ₹{d['amount']} now", key=d['merchant']+"_pay"):
            st.success("✅ Payment successful. Limit updated.")
        if col2.button("🔄 Retry Transaction", key=d['merchant']+"_retry"):
            st.info("🔁 Retrying transaction...")

# ---- Tab 2: Card Controls ----
with tab2:
    for d in [x for x in declines if x["code"] == "CARD_CONTROL"]:
        st.markdown(
            f"""
            <div style="border-radius:15px; padding:15px; background-color:#fff4e6; margin-bottom:15px;">
                <h4>❌ Payment Declined at {d['merchant']}</h4>
                <p><b>Amount:</b> ₹{d['amount']} | <b>Time:</b> {d['time']}</p>
                <p><b>Reason:</b> {d['reason']}</p>
            </div>
            """, unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        if col1.button("✅ Allow Once", key=d['merchant']+"_once"):
            st.success("✔️ Online usage enabled for this transaction.")
        if col2.button("⚙️ Update Settings", key=d['merchant']+"_settings"):
            st.info("⚙️ Opening card control settings...")

# ---- Tab 3: PIN Errors ----
with tab3:
    for d in [x for x in declines if x["code"] == "PIN_ERROR"]:
        st.markdown(
            f"""
            <div style="border-radius:15px; padding:15px; background-color:#e6f3ff; margin-bottom:15px;">
                <h4>❌ Payment Declined at {d['merchant']}</h4>
                <p><b>Amount:</b> ₹{d['amount']} | <b>Time:</b> {d['time']}</p>
                <p><b>Reason:</b> {d['reason']}</p>
            </div>
            """, unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        if col1.button("🔁 Retry PIN", key=d['merchant']+"_retry_pin"):
            st.info("Please re-enter your PIN securely.")
        if col2.button("🔒 Reset PIN", key=d['merchant']+"_reset_pin"):
            st.success("🔑 PIN reset successfully!")

# ---- Tab 4: Invalid Credentials ----
with tab4:
    for d in [x for x in declines if x["code"] == "INVALID_CREDENTIALS"]:
        st.markdown(
            f"""
            <div style="border-radius:15px; padding:15px; background-color:#f3e6ff; margin-bottom:15px;">
                <h4>❌ Payment Declined at {d['merchant']}</h4>
                <p><b>Amount:</b> ₹{d['amount']} | <b>Time:</b> {d['time']}</p>
                <p><b>Reason:</b> {d['reason']}</p>
            </div>
            """, unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        if col1.button("🔑 View Card Details", key=d['merchant']+"_view"):
            st.info("🔍 Secure card details displayed.")
        if col2.button("🆕 Generate Virtual Card", key=d['merchant']+"_virtual"):
            st.success("💳 Virtual card created successfully.")

