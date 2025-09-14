import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IDFC Credit Card Prototype", layout="centered")

# ---------------- Brand Styling ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    .app-container {
        width: 380px;
        margin: auto;
        border: 2px solid #ddd;
        border-radius: 30px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.2);
        background: #FFFFFF;
        padding: 15px;
    }

    .header {
        background-color: #AD0020;
        color: white;
        padding: 15px;
        border-radius: 20px;
        text-align: center;
        font-weight: 600;
        font-size: 20px;
    }

    .decline-card {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        border-left: 6px solid #AD0020;
        background: #fff8f8;
    }

    .stButton>button {
        background-color: #AD0020;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background-color: #820018;
        color: #FFFFFF;
    }

    .metric-box {
        border-radius: 12px;
        background: #FFCC00;
        padding: 12px;
        text-align: center;
        font-weight: 600;
    }

    .nav-bar {
        display: flex;
        justify-content: space-around;
        background: #f7f7f7;
        padding: 10px;
        border-top: 2px solid #AD0020;
        border-radius: 0 0 20px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- App Wrapper ----------------
st.markdown("<div class='app-container'>", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<div class='header'>💳 IDFC FIRST Credit Card</div>", unsafe_allow_html=True)

# ---------------- Navigation ----------------
menu = st.radio(
    "Navigation",
    ["🏠 Home", "⚠️ Declines", "💳 Card Controls", "📊 EMI Options", "👤 Profile"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------------- Mock Data ----------------
declines = [
    {"merchant": "Swiggy", "amount": 2450, "reason": "Insufficient Balance", "code": "INSUFFICIENT_LIMIT"},
    {"merchant": "Amazon", "amount": 1299, "reason": "Online usage disabled", "code": "CARD_CONTROL"},
    {"merchant": "Zomato", "amount": 560, "reason": "Incorrect PIN entered", "code": "PIN_ERROR"},
    {"merchant": "Netflix", "amount": 499, "reason": "Invalid CVV", "code": "INVALID_CREDENTIALS"}
]

# ---------------- Home ----------------
if menu == "🏠 Home":
    st.markdown("### Dashboard")
    st.markdown("<div class='metric-box'>Available Limit: ₹75,500</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-box'>Current Due: ₹24,500 (Due in 12 days)</div>", unsafe_allow_html=True)
    st.progress(0.65)
    st.info("💡 Pay ₹10,000 today to increase your available limit instantly.")

# ---------------- Declines ----------------
elif menu == "⚠️ Declines":
    st.markdown("### Recent Declines")
    for d in declines:
        st.markdown(
            f"""
            <div class="decline-card">
                <h4>{d['merchant']} – ₹{d['amount']}</h4>
                <p><b>Reason:</b> {d['reason']}</p>
                <p><b>Time:</b> {datetime.now().strftime("%H:%M:%S")}</p>
            </div>
            """, unsafe_allow_html=True
        )

        if d["code"] == "INSUFFICIENT_LIMIT":
            st.button("💰 Pay Now", key=d['merchant']+"_pay")
        elif d["code"] == "CARD_CONTROL":
            st.button("⚙️ Update Card Settings", key=d['merchant']+"_settings")
        elif d["code"] == "PIN_ERROR":
            st.button("🔒 Reset PIN", key=d['merchant']+"_reset")
        elif d["code"] == "INVALID_CREDENTIALS":
            st.button("🆕 Generate Virtual Card", key=d['merchant']+"_virtual")

# ---------------- Card Controls ----------------
elif menu == "💳 Card Controls":
    st.markdown("### Manage Your Card")
    st.toggle("Enable Online Transactions", value=True)
    st.toggle("Enable International Transactions", value=False)
    st.toggle("Enable Contactless Payments", value=True)
    st.toggle("Enable ATM Withdrawals", value=True)
    st.success("✅ Preferences saved successfully.")

# ---------------- EMI Options ----------------
elif menu == "📊 EMI Options":
    st.markdown("### Convert Purchases to EMI")
    purchase = st.selectbox("Select Transaction", ["Amazon – ₹12,000", "Flipkart – ₹18,500", "Myntra – ₹6,500"])
    tenure = st.radio("Choose Tenure", ["3 months", "6 months", "12 months"], horizontal=True)
    st.button("📌 Convert to EMI")

# ---------------- Profile ----------------
elif menu == "👤 Profile":
    st.markdown("### My Profile")
    st.write("**Name:** Rahul Sharma")
    st.write("**Card:** IDFC FIRST Classic Credit Card")
    st.write("**Member Since:** 2022")
    st.write("**Rewards Points:** 12,540")
    st.button("🚪 Logout")

# ---------------- Footer ----------------
st.markdown("<div class='nav-bar'>🏠 | ⚠️ | 💳 | 📊 | 👤</div>", unsafe_allow_html=True)

# ---------------- Close App Wrapper ----------------
st.markdown("</div>", unsafe_allow_html=True)



