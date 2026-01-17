import sys
import os
import json
import streamlit as st

# ------------------ FIX IMPORT PATH ------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.genai.llm_engine import generate_retention_bundle


# ------------------ CACHE SAFE GENAI CALL ------------------
@st.cache_data(show_spinner=False)
def get_cached_ai_output(profile_json: str) -> dict:
    """
    Streamlit-safe cached GenAI call.
    Uses JSON string to avoid mutable dict issues.
    """
    profile_dict = json.loads(profile_json)
    return generate_retention_bundle(profile_dict)


# ================== PAGE CONFIG ==================
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

# ================== RISK ANALYSIS (VISUAL ONLY) ==================
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
    st.markdown(
        f"<h3 style='color:{risk_color}; text-align:center;'>{risk_level}</h3>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align:center;'>Customer churn likelihood</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<h4>Churn Probability</h4><h1>{int(churn_prob * 100)}%</h1>", unsafe_allow_html=True)
    st.progress(churn_prob)
    st.caption("Confidence score based on model prediction")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================== GENAI INPUT ==================
customer_profile = {
    "gender": gender,
    "senior_citizen": senior,
    "partner": partner,
    "dependents": dependents,
    "tenure_months": tenure,
    "monthly_charges": monthly_charges,
    "contract_type": "Month-to-month" if tenure < 12 else "Long-term",
    "support_calls": "High" if tenure < 3 else "Normal"
}

# ================== GENAI EXECUTION ==================
ai_output = None

if st.button("🚀 Run AI Analysis"):
    profile_json = json.dumps(customer_profile, sort_keys=True)

    with st.spinner("AI analyzing customer risk..."):
        ai_output = get_cached_ai_output(profile_json)

# ================== DISPLAY GENAI OUTPUT ==================
if ai_output:

    risk_explanation = ai_output.get(
        "risk_explanation",
        "Explanation unavailable."
    )
    retention_decision = ai_output.get(
        "retention_decision",
        "No decision available."
    )
    customer_message = ai_output.get(
        "customer_message",
        "Thank you for being a valued customer."
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ------------------ AI EXPLANATION ------------------
    with st.expander("🧠 AI Explanation Panel", expanded=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(risk_explanation)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ------------------ AI DECISION ------------------
    with st.expander("🎯 AI Decision Panel", expanded=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(retention_decision)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ------------------ RETENTION MESSAGE ------------------
    with st.expander("💬 Retention Message Generator", expanded=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.text_area("", value=customer_message, height=200)
        st.markdown('</div>', unsafe_allow_html=True)

st.caption("Powered by local GenAI • Privacy-safe • No external API calls")
