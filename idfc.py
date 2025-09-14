import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IDFC Credit Card - Decline Assist", layout="centered")

# ---- Mock Data (Decline Cases) ----
declines = [
    {
        "merchant": "Swiggy",
        "amount": 2450,
        "reason": "Insufficient Balance",
        "code": "INSUFFICIENT_LIMIT",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "merchant": "Amazon",
        "amount": 1299,
        "reason": "Online usage disabled",
        "code": "CARD_CONTROL",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "merchant": "Zomato",
        "amount": 560,
        "reason": "Incorrect PIN entered",
        "code": "PIN_ERROR",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "merchant": "Netflix",
        "amount": 499,
        "reason": "Invalid CVV",
        "code": "INVALID_CREDENTIALS",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

st.title("💳 IDFC Credit Card – Decline Assist")
st.write("Smart, real-time help for declined transactions.")

# ---- Render Decline Cards ----
for d in declines:
    with st.container():
        st.subheader(f"❌ Payment Declined at {d['merchant']} (₹{d['amount']})")
        st.caption(f"Time: {d['time']}")
        st.write(f"**Reason:** {d['reason']}")

        if d["code"] == "INSUFFICIENT_LIMIT":
            st.warning("This transaction exceeds your available limit.")
            if st.button(f"💰 Pay ₹{d['amount']} to free up limit", key=d['merchant']+"_pay"):
                st.success("Payment made successfully. Limit updated. ✅")
            if st.button("🔄 Retry transaction", key=d['merchant']+"_retry"):
                st.info("Transaction retried. Awaiting confirmation.")

        elif d["code"] == "CARD_CONTROL":
            st.warning("Your card control settings blocked this transaction.")
            if st.button("✅ Allow once (secure)", key=d['merchant']+"_once"):
                st.success("Online usage enabled for this transaction.")
            if st.button("⚙️ Update card settings", key=d['merchant']+"_settings"):
                st.info("Redirecting to card control settings...")

        elif d["code"] == "PIN_ERROR":
            st.warning("Incorrect PIN entered.")
            if st.button("🔁 Retry with correct PIN", key=d['merchant']+"_retry_pin"):
                st.info("Please re-enter your PIN securely.")
            if st.button("🔒 Reset PIN", key=d['merchant']+"_reset"):
                st.success("PIN reset successfully. Use new PIN for next transaction.")

        elif d["code"] == "INVALID_CREDENTIALS":
            st.warning("Invalid card details entered.")
            if st.button("🔑 View card details", key=d['merchant']+"_view"):
                st.info("Card details (masked) displayed securely.")
            if st.button("🆕 Generate virtual card", key=d['merchant']+"_virtual"):
                st.success("New single-use virtual card generated.")

        st.markdown("---")
