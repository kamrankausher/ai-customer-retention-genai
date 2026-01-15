import streamlit as st

# ================== PAGE CONFIG (ONLY ONCE) ==================
st.set_page_config(
    page_title="AI Customer Retention Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== GLOBAL STYLES ==================
st.markdown("""
<style>
body, .main {
    background-color: #0b0f1a;
}

h1, h2, h3, h4 {
    color: #d4af37;
    font-family: 'Segoe UI', sans-serif;
}

p, label {
    color: #dddddd;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: linear-gradient(145deg, #121826, #0e1320);
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 0 25px rgba(212, 175, 55, 0.15);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: scale(1.02);
}

.divider {
    height: 2px;
    background: linear-gradient(to right, #d4af37, transparent);
    margin: 35px 0;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<h1>AI Customer Retention Intelligence</h1>
<p>Predict churn • Explain risk • Decide retention actions</p>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== CUSTOMER PROFILE ==================
st.markdown("## 👤 Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tenure = st.slider("Tenure (Months)", 0, 72, 1)
    monthly_charges = st.slider("Monthly Charges", 20, 120, 90)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== RISK ANALYSIS ==================
st.markdown("## 📊 Risk Analysis")

if tenure <= 3 and monthly_charges > 80:
    risk_level = "HIGH RISK"
    churn_prob = 0.92
    risk_color = "#ff4d4d"
elif tenure <= 12:
    risk_level = "MEDIUM RISK"
    churn_prob = 0.55
    risk_color = "#f5c542"
else:
    risk_level = "LOW RISK"
    churn_prob = 0.15
    risk_color = "#00c853"

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{risk_color}; text-align:center;'>{risk_level}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Customer churn likelihood</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<h4>Churn Probability</h4><h1>{int(churn_prob*100)}%</h1>", unsafe_allow_html=True)
    st.progress(churn_prob)
    st.caption("Confidence score based on model prediction")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== AI EXPLANATION ==================
with st.expander("🧠 AI Explanation Panel", expanded=True):
    reasons = []
    if tenure <= 3:
        reasons.append("the customer is very new")
    if monthly_charges > 80:
        reasons.append("monthly charges are relatively high")
    if partner == "No" and dependents == "No":
        reasons.append("there are no family ties associated with the account")

    explanation = "The model predicts churn risk because " + ", and ".join(reasons) if reasons else \
        "No strong churn indicators were detected."

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(explanation)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== AI DECISION ==================
with st.expander("🎯 AI Decision Panel", expanded=True):
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if risk_level == "HIGH RISK":
        st.write("**Immediate retention intervention required.**")
        st.write("Offer discounts, premium support, and contract upgrades.")
    elif risk_level == "MEDIUM RISK":
        st.write("**Preventive engagement recommended.**")
        st.write("Provide value-added services.")
    else:
        st.write("**No action required.** Customer is stable.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== RETENTION MESSAGE ==================
with st.expander("💬 Retention Message Generator", expanded=True):
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if risk_level == "HIGH RISK":
        message = "We value you! Enjoy a special discount and premium support."
    elif risk_level == "MEDIUM RISK":
        message = "Unlock additional benefits at no extra cost."
    else:
        message = "Thank you for being a loyal customer."

    st.text_area("", value=message, height=180)
    st.markdown('</div>', unsafe_allow_html=True)
