"""
Module: Girl's Profile
Collect personal details of the girl for compatibility analysis.
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider

st.set_page_config(
    page_title="Girl's Profile — LoveMatch AI",
    page_icon="👩",
    layout="wide"
)

inject_theme()

page_header(
    "👩",
    "Girl's Profile",
    "Share your personal details, background, and relationship expectations to complete the compatibility picture."
)

st.markdown('<div class="lm-step-badge">Step 2 of 3 — Girl\'s Profile</div>', unsafe_allow_html=True)

# Guard: need boy's profile first
if 'boy_profile' not in st.session_state:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:40px; color:#aaa;">
      <div style="font-size:2em; margin-bottom:10px;">⚠️</div>
      <div>Please complete the <strong>Boy's Profile</strong> first before continuing here.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("← Go to Boy's Profile"):
        st.switch_page("pages/1_Boy_Profile.py")
    st.stop()

st.markdown('<div class="lm-card">', unsafe_allow_html=True)
st.markdown("### 📋 Fill in Your Details")

with st.form("girl_profile_form"):

    st.markdown("#### 👤 Personal")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Your Age", 18, 60, 26)
    with col2:
        education = st.selectbox("Education Level",
            ["School", "Graduate", "Postgraduate", "PhD"], key="girl_edu")
    with col3:
        income = st.selectbox("Income Level",
            ["Low", "Middle", "High"], key="girl_income")

    st.markdown("#### 🏛️ Background")
    col4, col5, col6 = st.columns(3)
    with col4:
        caste = st.selectbox("Caste Match with Partner",
            ["Same", "Different"], key="girl_caste")
    with col5:
        religion = st.selectbox("Religion",
            ["Hindu", "Muslim", "Sikh", "Christian", "Others"], key="girl_religion")
    with col6:
        parental = st.selectbox("Parental Approval",
            ["No", "Partial", "Yes"], key="girl_parental")

    st.markdown("#### 🏡 Lifestyle")
    col7, col8, col9 = st.columns(3)
    with col7:
        location = st.selectbox("Location", ["Urban", "Rural"], key="girl_location")
    with col8:
        dowry = st.selectbox("Dowry Status",
            ["Yes", "No", "Not Disclosed"], key="girl_dowry")
    with col9:
        children = st.slider("Desired Children", 0, 10, 2)

    st.markdown("#### 💞 Relationship")
    col10, col11, col12 = st.columns(3)
    with col10:
        work = st.selectbox("Your Work Status", ["Yes", "No"], key="girl_work")
    with col11:
        intercaste = st.selectbox("Open to Inter-Caste",
            ["Yes", "No"], key="girl_intercaste")
    with col12:
        interreligion = st.selectbox("Open to Inter-Religion",
            ["Yes", "No"], key="girl_interreligion")

    st.markdown("#### 💍 Marriage Type")
    marriage_type = st.radio("", ["Love Marriage", "Arranged Marriage"],
        horizontal=True, key="girl_marriage_type")
    marriage_value = "Love" if marriage_type == "Love Marriage" else "Arranged"

    col_b, col_s = st.columns(2)
    with col_b:
        back_button = st.form_submit_button("← Back to Boy's Profile", use_container_width=True)
    with col_s:
        submit_button = st.form_submit_button(
            "✅ Save & Analyse Compatibility →",
            use_container_width=True,
            type="primary"
        )

st.markdown('</div>', unsafe_allow_html=True)

if back_button:
    st.switch_page("pages/1_Boy_Profile.py")

if submit_button:
    st.session_state['girl_profile'] = {
        'Age_at_Marriage': age,
        'Gender': 'Female',
        'Education_Level': education,
        'Income_Level': income,
        'Caste_Match': caste,
        'Religion': religion,
        'Parental_Approval': parental,
        'Urban_Rural': location,
        'Dowry_Exchanged': dowry,
        'Children_Count': children,
        'Years_Since_Marriage': 0,
        'Spouse_Working': work,
        'Inter-Caste': intercaste,
        'Inter-Religion': interreligion,
        'Marriage_Type': marriage_value
    }
    st.success("✅ Profile saved!")
    st.switch_page("pages/3_Compatibility_Analysis.py")

ornamental_divider()
st.markdown('<div style="text-align:center; color:#bbb; font-size:0.8em;">LoveMatch AI · Your data stays in this session only</div>', unsafe_allow_html=True)
