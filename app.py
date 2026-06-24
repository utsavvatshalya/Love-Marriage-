"""
LoveMatch AI - Couples Compatibility Analyzer
Two people, one future. Discover if you're relationship-ready.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LoveMatch AI - Couples Compatibility",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #FF6B6B;
        --primary-dark: #EE5A52;
        --secondary: #2C3E50;
        --accent: #FF8E8E;
        --success: #27AE60;
        --warning: #F39C12;
        --light-bg: #F8F9FA;
    }
    
    body {
        background: linear-gradient(135deg, #F8F9FA 0%, #E8EAED 100%);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 50%, #2C3E50 100%);
        padding: 80px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.2);
    }
    
    .hero-section h1 {
        font-size: 3.5em;
        margin-bottom: 15px;
        font-weight: 800;
    }
    
    .module-card {
        background: white;
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 5px solid #FF6B6B;
        transition: all 0.3s ease;
    }
    
    .module-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.15);
    }
    
    .module-card h3 {
        color: #FF6B6B;
        margin-top: 0;
    }
    
    .stats-box {
        background: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border-bottom: 4px solid #FF6B6B;
    }
    
    .stats-number {
        font-size: 2.5em;
        font-weight: 800;
        color: #FF6B6B;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>💕 LoveMatch AI</h1>
    <p style="font-size: 1.3em; margin: 15px 0;">Two hearts, one future</p>
    <p style="font-size: 1.1em; opacity: 0.95;">
    Discover your compatibility and make informed decisions about your relationship
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Main heading
st.markdown("## 🚀 How It Works")
st.markdown("**Step 1 → Step 2 → Step 3 → Decision**")

col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    st.markdown("""
    <div class="module-card">
        <h3>👨 Boy's Profile</h3>
        <p style="color: #666; line-height: 1.6;">
        Enter your background, lifestyle, and relationship goals in detail.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📝 Start", key="boy", use_container_width=True):
        st.switch_page("pages/1_Boy_Profile.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <h3>👩 Girl's Profile</h3>
        <p style="color: #666; line-height: 1.6;">
        Share your information, preferences, and what you're looking for.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📝 Start", key="girl", use_container_width=True):
        st.switch_page("pages/2_Girl_Profile.py")

with col3:
    st.markdown("""
    <div class="module-card">
        <h3>💫 Compare Profiles</h3>
        <p style="color: #666; line-height: 1.6;">
        See visual comparison of both profiles side-by-side.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Analyze", key="compare", use_container_width=True):
        st.switch_page("pages/3_Compatibility_Analysis.py")

with col4:
    st.markdown("""
    <div class="module-card">
        <h3>🎯 Get Recommendation</h3>
        <p style="color: #666; line-height: 1.6;">
        Marriage-ready or Keep Casual? Data-driven advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💡 Advice", key="advice", use_container_width=True):
        st.switch_page("pages/3_Compatibility_Analysis.py")

st.divider()

# Info section
st.markdown("### ℹ️ What We Analyze")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Personal Profile:**
    - Age, Education, Income Level
    - Caste, Religion, Location Preference
    
    **Lifestyle:**
    - Urban/Rural preference
    - Work status & career ambitions
    - Family values
    """)

with col2:
    st.markdown("""
    **Compatibility Factors:**
    - Age & life stage alignment
    - Educational/income match
    - Religious & caste compatibility
    - Family approval likelihood
    """)

st.divider()

st.markdown("### 📝 Privacy & Security")
st.markdown("""
✅ **Your data is private.** No information is stored or shared.  
✅ **Instant analysis.** Results generated in real-time.  
✅ **No registration.** Use anonymously.  
✅ **Fair & unbiased.** ML models trained on diverse data.  
""")

st.divider()

st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; margin-top: 40px;">
<p>💕 LoveMatch AI | Making relationship decisions easier</p>
</div>
""", unsafe_allow_html=True)
