import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IDFC Credit Card App", layout="centered")

# ---------------- Brand CSS ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    .phone-frame {
        width: 390px;
        margin: auto;
        border: 2px solid #ddd;
        border-radius: 30px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.2);
        background: #FFFFFF;
        overflow: hidden;
    }

    .header {
        background: linear-gradient(135deg, #AD0020, #820018);
        color: white;
        padding: 20px;
        text-align: center;
        font-weight: 600;
        font-size: 20px;
    }

    .credit-card {
        background: #AD0020;
        color: white;
        border-radius: 16px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    .credit-card h3 {
        margin: 0;
        font-size: 18px;
    }

    .metric-box {
        border-radius: 12px;
        background: #FFCC00;
        padding: 15px;
        margin: 10px;
        text-align: center;
        font-weight: 600;
    }

    .decline-bubble {
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        max-width: 80%;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    }

    .decline-red {
        background: #ffe5e8;
        border-left: 6px solid #AD0020;
    }

    .decline-yellow {
        background: #fff7cc;
        border-left: 6px solid #FFCC00;
    }

    .stButton>button {
        background-color: #AD0020;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
        margin-top: 6px;
    }

    .stButton>button:hover {
        background-color: #820018;
        color: #FFFFFF;
    }

    .nav-bar {
        display: flex;
        justify-content: space-around;
        background: #f7f7f7;
        padding: 12px;
        border-top: 2px solid #ddd;
    }

    .nav-item {
        text-align: center;
        font-size: 14px;
    }

    .active {
        color: #AD0020;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- App Wrapper ----------------
st.markdown("<div class='phone-frame'>", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<div class='header'>IDFC FIRST Credit Card</div>", unsafe_allow_html=True)

# ---------------- Bottom Navigation ----------------
menu = st.radio(
    "Navigation",
    ["🏠 Home", "⚠️ Declines", "💳 Controls", "📊 EMI", "👤 Profile"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------------- Mock Data ----------------
declines = [
    {"merchant": "Swiggy", "amount": 2450, "reason": "Insufficient Balance", "code": "INSUFFICIENT_LIMIT"},
    {"merchant": "Amazon", "amount": 1299, "reason": "Online usage disabled", "code": "CARD_CONTROL"},
    {"merchant": "Zomato", "amount": 560, "reason": "Incorrect PIN entered", "code": "PIN_ERROR"},
]

# ---------------- Home ----------------
if menu == "🏠 Home":
    st.markdown("""
        <div class='credit-card'>
            <h3>Rahul Sharma</h3>
            <p>**** **** **** 2345</p>
            <h3>Available Limit: ₹75,500</h3>
            <p>Due: ₹24,500 (12 days left)</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='metric-box'>⭐ Rewards: 12,540 Points</div>", unsafe_allow_html=True)
    st.info("💡 Pay ₹10,000 today to increase your available limit instantly.")

# ---------------- Declines ----------------
elif menu == "⚠️ Declines":
    st.markdown("### Recent Declines")
    for d in declines:
        bubble_class = "decline-red" if d["code"] != "CARD_CONTROL" else "decline-yellow"
        st.markdown(
            f"""
            <div class="decline-bubble {bubble_class}">
                <b>{d['merchant']}</b> – ₹{d['amount']} <br>
                <small>{d['reason']} | {datetime.now().strftime("%H:%M:%S")}</small>
            </div>
            """, unsafe_allow_html=True
        )
        if d["code"] == "INSUFFICIENT_LIMIT":
            st.button("💰 Pay Now", key=d['merchant']+"_pay")
        elif d["code"] == "CARD_CONTROL":
            st.button("⚙️ Update Card Settings", key=d['merchant']+"_settings")
        elif d["code"] == "PIN_ERROR":
            st.button("🔒 Reset PIN", key=d['merchant']+"_reset")

# ---------------- Controls ----------------
elif menu == "💳 Controls":
    st.markdown("### Card Controls")
    st.toggle("Enable Online Transactions", value=True)
    st.toggle("Enable International Transactions", value=False)
    st.toggle("Enable Contactless Payments", value=True)
    st.toggle("Enable ATM Withdrawals", value=True)
    st.success("✅ Preferences saved")

# ---------------- EMI ----------------
elif menu == "📊 EMI":
    st.markdown("### Convert to EMI")
    st.write("Amazon – ₹12,000")
    st.radio("Select Tenure", ["3 months (₹4,200)", "6 months (₹2,150)", "12 months (₹1,100)"])
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
st.markdown("<div class='nav-bar'><div class='nav-item'>🏠</div><div class='nav-item'>⚠️</div><div class='nav-item'>💳</div><div class='nav-item'>📊</div><div class='nav-item'>👤</div></div>", unsafe_allow_html=True)

# ---------------- Close Wrapper ----------------
st.markdown("</div>", unsafe_allow_html=True)




