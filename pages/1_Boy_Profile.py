"""
Module 1: Boy's Profile
Collect personal details of the boy for compatibility analysis.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.preprocess import build_input_form_fields

# Page config
st.set_page_config(
    page_title="Boy's Profile - LoveMatch AI",
    page_icon="👨",
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

st.title("👨 Boy's Profile")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
Enter your personal details, background, and relationship preferences.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="progress-bar">Step 1 of 3 - Boy Profile</div>', unsafe_allow_html=True)

# Feature columns for the form
feature_cols = [
    'Age_at_Marriage',
    'Gender',
    'Education_Level',
    'Income_Level',
    'Caste_Match',
    'Religion',
    'Parental_Approval',
    'Urban_Rural',
    'Dowry_Exchanged',
    'Children_Count',
    'Years_Since_Marriage',
    'Spouse_Working',
    'Inter-Caste',
    'Inter-Religion',
    'Marriage_Type'
]

with st.container():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    
    with st.form("boy_profile_form"):
        st.markdown("### 📋 Fill in Your Details")
        
        # Personal Details
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider("Your Age", 18, 60, 28, 1)
        with col2:
            education = st.selectbox("Education Level", 
                ["School", "Graduate", "Postgraduate", "PhD"], 
                key="boy_edu")
        with col3:
            income = st.selectbox("Income Level", 
                ["Low", "Middle", "High"], 
                key="boy_income")
        
        # Background
        col4, col5, col6 = st.columns(3)
        with col4:
            caste = st.selectbox("Caste Match with Partner",
                ["Same", "Different"],
                key="boy_caste")
        with col5:
            religion = st.selectbox("Religion",
                ["Hindu", "Muslim", "Sikh", "Christian", "Others"],
                key="boy_religion")
        with col6:
            parental = st.selectbox("Parental Approval Status",
                ["No", "Partial", "Yes"],
                key="boy_parental")
        
        # Lifestyle
        col7, col8, col9 = st.columns(3)
        with col7:
            location = st.selectbox("Location Preference",
                ["Urban", "Rural"],
                key="boy_location")
        with col8:
            dowry = st.selectbox("Dowry Status",
                ["Yes", "No", "Not Disclosed"],
                key="boy_dowry")
        with col9:
            children = st.slider("Desired Children Count", 0, 10, 2, 1)
        
        # Relationship
        col10, col11, col12 = st.columns(3)
        with col10:
            spouse_work = st.selectbox("Preference: Partner Working",
                ["Yes", "No"],
                key="boy_spouse_work")
        with col11:
            intercaste = st.selectbox("Open to Inter-Caste Marriage",
                ["Yes", "No"],
                key="boy_intercaste")
        with col12:
            interreligion = st.selectbox("Open to Inter-Religion Marriage",
                ["Yes", "No"],
                key="boy_interreligion")
        
        # Relationship Type
        st.markdown("#### What kind of marriage are you looking for?")
        marriage_type = st.radio("", ["Love Marriage", "Arranged Marriage"],
            horizontal=True, key="boy_marriage_type")
        marriage_value = "Love" if marriage_type == "Love Marriage" else "Arranged"
        
        submit_button = st.form_submit_button(
            "✅ Save My Profile & Continue to Girl's Profile",
            use_container_width=True,
            type="primary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    # Save boy's profile to session state
    boy_profile = {
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
        'Years_Since_Marriage': 0,  # Not applicable yet
        'Spouse_Working': spouse_work,
        'Inter-Caste': intercaste,
        'Inter-Religion': interreligion,
        'Marriage_Type': marriage_value
    }
    
    st.session_state['boy_profile'] = boy_profile
    st.success("✅ Your profile saved!")
    st.info("Proceeding to Girl's Profile →")
    st.switch_page("pages/2_Girl_Profile.py")
