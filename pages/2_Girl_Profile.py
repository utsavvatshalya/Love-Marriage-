"""
Module 2: Girl's Profile
Collect personal details of the girl for compatibility analysis.
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# Page config
st.set_page_config(
    page_title="Girl's Profile - LoveMatch AI",
    page_icon="👩",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .form-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .progress-bar {
        background: #FF6B6B;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("👩 Girl's Profile")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
Share your personal details, background, and relationship expectations.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="progress-bar">Step 2 of 3 - Girl Profile</div>', unsafe_allow_html=True)

# Check if boy's profile exists
if 'boy_profile' not in st.session_state:
    st.warning("⚠️ Please complete Boy's Profile first!")
    if st.button("← Go Back to Boy Profile"):
        st.switch_page("pages/1_Boy_Profile.py")
    st.stop()

with st.container():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    
    with st.form("girl_profile_form"):
        st.markdown("### 📋 Fill in Your Details")
        
        # Personal Details
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider("Your Age", 18, 60, 26, 1)
        with col2:
            education = st.selectbox("Education Level", 
                ["School", "Graduate", "Postgraduate", "PhD"], 
                key="girl_edu")
        with col3:
            income = st.selectbox("Income Level", 
                ["Low", "Middle", "High"], 
                key="girl_income")
        
        # Background
        col4, col5, col6 = st.columns(3)
        with col4:
            caste = st.selectbox("Caste Match with Partner",
                ["Same", "Different"],
                key="girl_caste")
        with col5:
            religion = st.selectbox("Religion",
                ["Hindu", "Muslim", "Sikh", "Christian", "Others"],
                key="girl_religion")
        with col6:
            parental = st.selectbox("Parental Approval Status",
                ["No", "Partial", "Yes"],
                key="girl_parental")
        
        # Lifestyle
        col7, col8, col9 = st.columns(3)
        with col7:
            location = st.selectbox("Location Preference",
                ["Urban", "Rural"],
                key="girl_location")
        with col8:
            dowry = st.selectbox("Dowry Status",
                ["Yes", "No", "Not Disclosed"],
                key="girl_dowry")
        with col9:
            children = st.slider("Desired Children Count", 0, 10, 2, 1)
        
        # Relationship
        col10, col11, col12 = st.columns(3)
        with col10:
            work_preference = st.selectbox("Your Work Status",
                ["Yes", "No"],
                key="girl_work")
        with col11:
            intercaste = st.selectbox("Open to Inter-Caste Marriage",
                ["Yes", "No"],
                key="girl_intercaste")
        with col12:
            interreligion = st.selectbox("Open to Inter-Religion Marriage",
                ["Yes", "No"],
                key="girl_interreligion")
        
        # Relationship Type
        st.markdown("#### What kind of marriage are you looking for?")
        marriage_type = st.radio("", ["Love Marriage", "Arranged Marriage"],
            horizontal=True, key="girl_marriage_type")
        marriage_value = "Love" if marriage_type == "Love Marriage" else "Arranged"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            back_button = st.form_submit_button(
                "← Back to Boy's Profile",
                use_container_width=True
            )
        with col_btn2:
            submit_button = st.form_submit_button(
                "✅ Save & Analyze Compatibility",
                use_container_width=True,
                type="primary"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

if back_button:
    st.switch_page("pages/1_Boy_Profile.py")

if submit_button:
    # Save girl's profile to session state
    girl_profile = {
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
        'Spouse_Working': work_preference,
        'Inter-Caste': intercaste,
        'Inter-Religion': interreligion,
        'Marriage_Type': marriage_value
    }
    
    st.session_state['girl_profile'] = girl_profile
    st.success("✅ Your profile saved!")
    st.info("Analyzing compatibility →")
    st.switch_page("pages/3_Compatibility_Analysis.py")
