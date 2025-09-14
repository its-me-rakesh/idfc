# idfc_reco_app.py
import streamlit as st
from datetime import datetime

# ---------------- Page config ----------------
st.set_page_config(page_title="IDFC - Smart Settings Recommender", layout="centered")

# ---------------- Brand CSS ----------------
BRAND_RED = "#AD0020"
BRAND_YELLOW = "#FFCC00"
BG_WHITE = "#FFFFFF"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    * {{ font-family: 'Inter', sans-serif !important; color: #000; }}

    .phone-frame {{
        width: 390px;
        margin: 18px auto;
        border: 1px solid #e6e6e6;
        border-radius: 28px;
        box-shadow: 0px 8px 30px rgba(0,0,0,0.12);
        background: {BG_WHITE};
        overflow: hidden;
        padding-bottom: 12px;
    }}

    .header {{
        background: linear-gradient(135deg, {BRAND_RED}, #820018);
        color: white;
        padding: 16px;
        text-align: left;
        font-weight: 600;
        font-size: 18px;
        border-radius: 0 0 18px 18px;
    }}

    .card {{
        background: {BG_WHITE};
        border-radius: 14px;
        padding: 14px;
        margin: 14px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
    }}

    .big-amount {{
        font-size: 22px;
        font-weight: 700;
        color: #000;
    }}

    .apply-btn .stButton>button {{
        background-color: {BRAND_RED};
        color: #FFFFFF;
        border-radius: 12px;
        padding: 9px 16px;
        font-weight: 700;
        border: none;
    }}
    .apply-btn .stButton>button:hover {{
        background-color: #820018;
        color: #fff;
    }}

    .small-btn .stButton>button {{
        background-color: {BRAND_YELLOW};
        color: #000;
        border-radius: 10px;
        padding: 6px 10px;
        font-weight: 600;
        border: none;
    }}

    .toggle-row {{
        display:flex; justify-content:space-between; align-items:center; padding:10px 0;
    }}
    .muted {{ color: #666; font-size: 13px; }}
    .section-title {{ font-weight:700; margin-top:8px; margin-bottom:6px; }}
    </style>
""", unsafe_allow_html=True)

# ---------------- Session state defaults ----------------
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "applied_settings" not in st.session_state:
    # default simulated settings
    st.session_state.applied_settings = {
        "online_enabled": True,
        "international_enabled": False,
        "contactless_enabled": True,
        "nfc_enabled": True,
        "virtual_card_enabled": False,
        "auto_emi": False,
        "monthly_limit_suggestion": 75000,
        "notifications": True
    }
if "last_class" not in st.session_state:
    st.session_state.last_class = None
if "last_reco" not in st.session_state:
    st.session_state.last_reco = {}

# ---------------- Utility functions ----------------
def classify_user(a: dict):
    """
    Simple rule-based classifier. Returns a tuple (class_name, reasons)
    """
    reasons = []
    # Scores for each persona
    scores = {
        "Frequent Traveler": 0,
        "Online Shopper": 0,
        "Security-Conscious": 0,
        "New-to-Credit": 0,
        "High Spender": 0,
        "Minimal User": 0
    }

    # Heuristics
    # Travel behavior
    if a.get("travels_internationally") == "Yes":
        scores["Frequent Traveler"] += 2
        scores["High Spender"] += 1
        reasons.append("Travels internationally")

    # Shopping & subscriptions
    if a.get("online_spend") == "High":
        scores["Online Shopper"] += 2
        scores["High Spender"] += 1
        reasons.append("High online spend")
    elif a.get("online_spend") == "Medium":
        scores["Online Shopper"] += 1
        reasons.append("Moderate online spend")

    # NFC / contactless preference
    if a.get("prefers_contactless") == "Yes":
        scores["High Spender"] += 1
        scores["Frequent Traveler"] += 1
        reasons.append("Uses contactless frequently")

    # EMI preference
    if a.get("uses_emi") == "Often":
        scores["High Spender"] += 2
        scores["Online Shopper"] += 1
        reasons.append("Often converts to EMI")

    # Security preferences
    if a.get("security_first") == "Yes":
        scores["Security-Conscious"] += 2
        reasons.append("Prioritizes security over convenience")

    # Credit familiarity
    if a.get("new_to_credit") == "Yes":
        scores["New-to-Credit"] += 2
        reasons.append("New to credit / thin file")
    else:
        # experienced users lean to minimal user or spender
        scores["Minimal User"] += 1

    # Card usage frequency & monthly spend
    monthly = a.get("monthly_spend", 0)
    if monthly >= 100000:
        scores["High Spender"] += 3
        reasons.append("Monthly spend very high")
    elif monthly >= 30000:
        scores["High Spender"] += 1
    elif monthly <= 5000:
        scores["Minimal User"] += 2
        reasons.append("Low monthly spend")

    # Preferred transaction mode
    mode = a.get("preferred_mode")
    if mode == "In-store (POS/Contactless)":
        scores["Frequent Traveler"] += 1
        scores["Minimal User"] += 0
    elif mode == "Online (web/app)":
        scores["Online Shopper"] += 2
    elif mode == "Mostly EMI":
        scores["High Spender"] += 2

    # pick top scoring class
    cls = max(scores.items(), key=lambda x: x[1])[0]
    return cls, reasons

def get_recommendations_for_class(cls_name: str):
    """
    Return recommended settings dict for a class
    """
    base = {
        "online_enabled": True,
        "international_enabled": False,
        "contactless_enabled": True,
        "nfc_enabled": True,
        "virtual_card_enabled": False,
        "auto_emi": False,
        "monthly_limit_suggestion": 50000,
        "notifications": True,
        "notes": ""
    }

    if cls_name == "Frequent Traveler":
        base.update({
            "international_enabled": True,
            "contactless_enabled": True,
            "nfc_enabled": True,
            "virtual_card_enabled": False,
            "auto_emi": False,
            "monthly_limit_suggestion": 150000,
            "notes": "Enable international & contactless for seamless travel. Keep alerts on for unusual foreign transactions."
        })
    elif cls_name == "Online Shopper":
        base.update({
            "online_enabled": True,
            "virtual_card_enabled": True,
            "contactless_enabled": False,
            "auto_emi": True,
            "monthly_limit_suggestion": 80000,
            "notes": "Enable virtual single-use cards for safer online checkout. Auto-EMI useful for big purchases."
        })
    elif cls_name == "Security-Conscious":
        base.update({
            "online_enabled": False,
            "virtual_card_enabled": True,
            "contactless_enabled": False,
            "nfc_enabled": False,
            "auto_emi": False,
            "monthly_limit_suggestion": 30000,
            "notes": "Keep online/contactless off. Use virtual cards for trusted merchants only."
        })
    elif cls_name == "New-to-Credit":
        base.update({
            "online_enabled": True,
            "virtual_card_enabled": False,
            "contactless_enabled": False,
            "auto_emi": False,
            "monthly_limit_suggestion": 20000,
            "notes": "Start with conservative limits; consider secured card if needed."
        })
    elif cls_name == "High Spender":
        base.update({
            "online_enabled": True,
            "virtual_card_enabled": True,
            "contactless_enabled": True,
            "nfc_enabled": True,
            "auto_emi": True,
            "monthly_limit_suggestion": 250000,
            "notes": "Higher monthly limit with auto-EMI for big purchases and travel perks enabled."
        })
    elif cls_name == "Minimal User":
        base.update({
            "online_enabled": True,
            "virtual_card_enabled": False,
            "contactless_enabled": False,
            "nfc_enabled": False,
            "auto_emi": False,
            "monthly_limit_suggestion": 15000,
            "notes": "Keep conservative limits and notifications to avoid surprises."
        })
    else:
        base["notes"] = "Default recommendation."

    return base

# ---------------- UI: phone frame and navigation ----------------
st.markdown("<div class='phone-frame'>", unsafe_allow_html=True)
st.markdown("<div class='header'>💳 IDFC Smart Settings Recommender</div>", unsafe_allow_html=True)

select = st.sidebar.selectbox("Quick Nav (dev)", ["Questionnaire", "Review Recommendation", "Applied Settings", "Reset"])

# If user uses sidebar nav, sync with main flow; otherwise use default flow via main nav
main_nav = st.radio("", ["📝 Questionnaire", "🔎 Recommendation", "⚙️ Apply", "📋 Applied Settings"], index=0, horizontal=True, label_visibility="collapsed")

page = None
# allow sidebar override (for testing)
if select:
    if select == "Questionnaire":
        page = "Questionnaire"
    elif select == "Review Recommendation":
        page = "Recommendation"
    elif select == "Applied Settings":
        page = "Applied Settings"
    elif select == "Reset":
        # reset answers
        st.session_state.answers = {}
        st.session_state.last_class = None
        st.session_state.last_reco = {}
        st.warning("Session reset. Please re-run questionnaire.")
        page = "Questionnaire"

# If sidebar not used, use main nav
if not page:
    if main_nav == "📝 Questionnaire":
        page = "Questionnaire"
    elif main_nav == "🔎 Recommendation":
        page = "Recommendation"
    elif main_nav == "⚙️ Apply":
        page = "Apply"
    else:
        page = "Applied Settings"

# ---------------- Page: Questionnaire ----------------
if page == "Questionnaire":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Tell us about your card usage</div>", unsafe_allow_html=True)

    # Basic info
    name = st.text_input("Your name", value=st.session_state.answers.get("name", ""))
    st.session_state.answers["name"] = name

    monthly_spend = st.number_input("Approx. monthly card spend (₹)", min_value=0, step=1000, value=int(st.session_state.answers.get("monthly_spend", 30000)))
    st.session_state.answers["monthly_spend"] = monthly_spend

    # Modes of transaction
    st.markdown("<div style='margin-top:8px;'><b>Preferred transaction mode</b></div>", unsafe_allow_html=True)
    preferred_mode = st.selectbox("Where do you use your card most?", ["Online (web/app)", "In-store (POS/Contactless)", "Mostly EMI", "Mixed"], index=0)
    st.session_state.answers["preferred_mode"] = preferred_mode

    # Online spend level
    online_spend = st.radio("Online spend level", ["Low", "Medium", "High"], index=1, horizontal=True)
    st.session_state.answers["online_spend"] = online_spend

    # Travel
    travels_internationally = st.selectbox("Do you travel internationally?", ["No", "Yes"], index=0)
    st.session_state.answers["travels_internationally"] = travels_internationally

    # NFC / contactless
    prefers_contactless = st.selectbox("Do you often use contactless / tap-to-pay?", ["No", "Yes"], index=1)
    st.session_state.answers["prefers_contactless"] = prefers_contactless

    # EMI usage
    uses_emi = st.selectbox("How often do you convert purchases to EMI?", ["Never", "Occasionally", "Often"], index=1)
    st.session_state.answers["uses_emi"] = uses_emi

    # Security preference
    security_first = st.selectbox("Do you prefer stricter security (disable online/contactless) over convenience?", ["No", "Yes"], index=0)
    st.session_state.answers["security_first"] = security_first

    # New to credit
    new_to_credit = st.selectbox("Are you new to credit / thin-file?", ["No", "Yes"], index=0)
    st.session_state.answers["new_to_credit"] = new_to_credit

    # Notifications
    notifications = st.checkbox("Receive real-time decline & suspicious activity alerts", value=True)
    st.session_state.answers["notifications"] = notifications

    # Quick summary & action
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f"**Summary so far:** {st.session_state.answers.get('name','(no name)')} — monthly ₹{st.session_state.answers.get('monthly_spend',0)}")
    if st.button("➡️ Get recommendation"):
        cls, reasons = classify_user(st.session_state.answers)
        st.session_state.last_class = cls
        reco = get_recommendations_for_class(cls)
        st.session_state.last_reco = reco
        st.success(f"Recommended profile: **{cls}**")
        if reasons:
            st.info("Reasoning: " + "; ".join(reasons))
        # navigate to recommendation
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Page: Recommendation (Review) ----------------
elif page == "Recommendation":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if not st.session_state.last_class:
        st.warning("No recommendation yet. Please complete the questionnaire first.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='section-title'>Recommended Profile: {st.session_state.last_class}</div>", unsafe_allow_html=True)
        st.markdown(f"_{datetime.now().strftime('%d %b %Y, %H:%M')}_", unsafe_allow_html=True)

        reco = st.session_state.last_reco or get_recommendations_for_class(st.session_state.last_class)
        st.markdown("<div style='margin-top:6px;'><b>Suggested Settings</b></div>", unsafe_allow_html=True)

        # Show toggles (preview, not applied yet)
        online = st.checkbox("Enable Online Transactions", value=reco["online_enabled"], key="preview_online")
        international = st.checkbox("Enable International Transactions", value=reco["international_enabled"], key="preview_intl")
        contactless = st.checkbox("Enable Contactless / POS", value=reco["contactless_enabled"], key="preview_contactless")
        nfc = st.checkbox("Enable NFC / Tap & Pay", value=reco["nfc_enabled"], key="preview_nfc")
        virtual_card = st.checkbox("Enable Virtual Single-use Cards for Online", value=reco["virtual_card_enabled"], key="preview_virtual")
        auto_emi = st.checkbox("Suggest Auto-EMI for big purchases", value=reco["auto_emi"], key="preview_emi")
        notifications_preview = st.checkbox("Receive real-time alerts", value=reco["notifications"], key="preview_notify")

        st.markdown(f"<div class='muted'>Suggested monthly limit: ₹{reco['monthly_limit_suggestion']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:10px;'><b>Notes:</b> {reco.get('notes','')}</div>", unsafe_allow_html=True)

        # Buttons: Apply or Edit
        c1, c2 = st.columns([1,1])
        with c1:
            if st.button("✅ Apply these settings", key="apply_reco", help="Simulate applying the recommended settings"):
                # apply (simulate)
                st.session_state.applied_settings.update({
                    "online_enabled": online,
                    "international_enabled": international,
                    "contactless_enabled": contactless,
                    "nfc_enabled": nfc,
                    "virtual_card_enabled": virtual_card,
                    "auto_emi": auto_emi,
                    "monthly_limit_suggestion": reco["monthly_limit_suggestion"],
                    "notifications": notifications_preview
                })
                st.success("✅ Settings applied to your profile (simulated). Go to 'Applied Settings' to review.")
                st.experimental_rerun()
        with c2:
            if st.button("✏️ Edit settings before apply", key="edit_reco"):
                st.info("You can edit the toggles above to tweak recommendations, then press Apply.")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Page: Apply (direct apply flow) ----------------
elif page == "Apply":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Quick apply last recommendation</div>", unsafe_allow_html=True)
    if not st.session_state.last_class:
        st.warning("No recommendation found. Run questionnaire first.")
    else:
        st.write(f"Last recommended profile: **{st.session_state.last_class}**")
        if st.button("Apply recommendation now"):
            reco = st.session_state.last_reco or get_recommendations_for_class(st.session_state.last_class)
            st.session_state.applied_settings.update(reco)
            st.success("Applied recommended settings (simulated).")
            st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Page: Applied Settings ----------------
elif page == "Applied Settings":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Your Current Settings (simulated)</div>", unsafe_allow_html=True)

    S = st.session_state.applied_settings
    st.markdown(f"<div><b>Online Transactions:</b> {'Enabled' if S['online_enabled'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>International:</b> {'Enabled' if S['international_enabled'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>Contactless / POS:</b> {'Enabled' if S['contactless_enabled'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>NFC / Tap & Pay:</b> {'Enabled' if S['nfc_enabled'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>Virtual Card:</b> {'Enabled' if S['virtual_card_enabled'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>Auto-EMI:</b> {'Enabled' if S['auto_emi'] else 'Disabled'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><b>Monthly limit (suggested):</b> ₹{S['monthly_limit_suggestion']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='muted'>Last recommended profile: {st.session_state.last_class or '—'}</div>", unsafe_allow_html=True)

    if st.button("🔁 Reset applied settings to defaults"):
        st.session_state.applied_settings = {
            "online_enabled": True,
            "international_enabled": False,
            "contactless_enabled": True,
            "nfc_enabled": True,
            "virtual_card_enabled": False,
            "auto_emi": False,
            "monthly_limit_suggestion": 75000,
            "notifications": True
        }
        st.success("Settings reset.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Close phone frame ----------------
st.markdown("</div>", unsafe_allow_html=True)





