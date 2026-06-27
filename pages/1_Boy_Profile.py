"""
Module: Boy's Profile
Collect personal details of the boy for compatibility analysis.
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider

st.set_page_config(
    page_title="Boy's Profile — LoveMatch AI",
    page_icon="👨",
    layout="wide"
)

inject_theme()

page_header(
    "👨",
    "Boy's Profile",
    "Enter your personal details, background, and relationship preferences — this forms the foundation of your compatibility analysis."
)

st.markdown('<div class="lm-step-badge">Step 1 of 3 — Boy\'s Profile</div>', unsafe_allow_html=True)

st.markdown('<div class="lm-card">', unsafe_allow_html=True)
st.markdown("### 📋 Fill in Your Details")

with st.form("boy_profile_form"):

    st.markdown("#### 👤 Personal")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Your Age", 18, 60, 28)
    with col2:
        education = st.selectbox("Education Level",
            ["School", "Graduate", "Postgraduate", "PhD"], key="boy_edu")
    with col3:
        income = st.selectbox("Income Level",
            ["Low", "Middle", "High"], key="boy_income")

    st.markdown("#### 🏛️ Background")
    col4, col5, col6 = st.columns(3)
    with col4:
        caste = st.selectbox("Caste Match with Partner",
            ["Same", "Different"], key="boy_caste")
    with col5:
        religion = st.selectbox("Religion",
            ["Hindu", "Muslim", "Sikh", "Christian", "Others"], key="boy_religion")
    with col6:
        parental = st.selectbox("Parental Approval",
            ["No", "Partial", "Yes"], key="boy_parental")

    st.markdown("#### 🏡 Lifestyle")
    col7, col8, col9 = st.columns(3)
    with col7:
        location = st.selectbox("Location", ["Urban", "Rural"], key="boy_location")
    with col8:
        dowry = st.selectbox("Dowry Status",
            ["Yes", "No", "Not Disclosed"], key="boy_dowry")
    with col9:
        children = st.slider("Desired Children", 0, 10, 2)

    st.markdown("#### 💞 Relationship")
    col10, col11, col12 = st.columns(3)
    with col10:
        spouse_work = st.selectbox("Preference: Partner Working",
            ["Yes", "No"], key="boy_spouse_work")
    with col11:
        intercaste = st.selectbox("Open to Inter-Caste",
            ["Yes", "No"], key="boy_intercaste")
    with col12:
        interreligion = st.selectbox("Open to Inter-Religion",
            ["Yes", "No"], key="boy_interreligion")

    st.markdown("#### 💍 Marriage Type")
    marriage_type = st.radio("", ["Love Marriage", "Arranged Marriage"],
        horizontal=True, key="boy_marriage_type")
    marriage_value = "Love" if marriage_type == "Love Marriage" else "Arranged"

    submit_button = st.form_submit_button(
        "✅ Save Profile & Continue →",
        use_container_width=True,
        type="primary"
    )

st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    st.session_state['boy_profile'] = {
        'Age_at_Marriage': age,
        'Gender': 'Male',
        'Education_Level': education,
        'Income_Level': income,
        'Caste_Match': caste,
        'Religion': religion,
        'Parental_Approval': parental,
        'Urban_Rural': location,
        'Dowry_Exchanged': dowry,
        'Children_Count': children,
        'Years_Since_Marriage': 0,
        'Spouse_Working': spouse_work,
        'Inter-Caste': intercaste,
        'Inter-Religion': interreligion,
        'Marriage_Type': marriage_value
    }
    st.success("✅ Profile saved!")
    st.switch_page("pages/2_Girl_Profile.py")

ornamental_divider()
st.markdown('<div style="text-align:center; color:#bbb; font-size:0.8em;">LoveMatch AI · Your data stays in this session only</div>', unsafe_allow_html=True)
