"""
LoveMatch AI - Streamlit Home Page
Multi-page ML application for predicting Indian marriage outcomes.
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="LoveMatch AI - Indian Marriage Outcome Predictor",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
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
        --white: #FFFFFF;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #F8F9FA 0%, #E8EAED 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background-color: transparent;
    }
    
    /* Hero Section */
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
        letter-spacing: -1px;
    }
    
    .hero-section p {
        font-size: 1.2em;
        margin: 12px 0;
        opacity: 0.98;
        font-weight: 300;
    }
    
    /* Module Cards */
    .module-card {
        background: white;
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 5px solid #FF6B6B;
        margin-bottom: 25px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .module-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF6B6B, #FF8E8E);
    }
    
    .module-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.15);
        border-top: 5px solid #FF8E8E;
    }
    
    .module-card h3 {
        color: #2C3E50;
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.6em;
        font-weight: 700;
    }
    
    .module-card p {
        color: #555;
        line-height: 1.6;
        margin: 10px 0;
    }
    
    .module-card ul {
        list-style: none;
        padding: 15px 0;
    }
    
    .module-card li {
        color: #666;
        padding: 8px 0;
        padding-left: 25px;
        position: relative;
    }
    
    .module-card li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #FF6B6B;
        font-weight: bold;
    }
    
    /* Stats Boxes */
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
    
    .stats-label {
        font-size: 0.85em;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* How It Works */
    .how-it-works {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 40px 0;
    }
    
    .how-it-works h2 {
        color: #2C3E50;
        margin-bottom: 30px;
        font-size: 2em;
        font-weight: 700;
    }
    
    .step {
        display: flex;
        margin-bottom: 30px;
        align-items: flex-start;
    }
    
    .step-number {
        background: linear-gradient(135deg, #FF6B6B, #EE5A52);
        color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 25px;
        flex-shrink: 0;
        font-size: 1.3em;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .step-content h4 {
        margin-top: 0;
        color: #2C3E50;
        font-size: 1.2em;
        font-weight: 600;
    }
    
    .step-content p {
        color: #666;
        line-height: 1.6;
        margin-top: 8px;
    }
    
    /* Sidebar */
    section[data-testid="sidebar"] {
        background: linear-gradient(180deg, #2C3E50 0%, #1A252F 100%);
    }
    
    section[data-testid="sidebar"] .stButton > button {
        background: #FF6B6B !important;
        width: 100% !important;
        margin: 8px 0 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        padding: 30px 20px;
        margin-top: 60px;
        border-top: 1px solid #EEE;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>💕 LoveMatch AI</h1>
    <p>Predict Indian Marriage Outcomes with ML & Explainability</p>
    <p style="font-size: 1em; opacity: 0.9;">
        Data-driven insights powered by XGBoost, SHAP, and 10,000+ marriage records
    </p>
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown("## Welcome to LoveMatch AI")
st.markdown("""
This intelligent system analyzes factors influencing Indian marriage outcomes — whether a marriage is 
born from love or arranged, likelihood of success, and actionable recommendations to strengthen your bond.

**Powered by machine learning, explainable with SHAP and counterfactuals via DiCE.**
""")

st.divider()

# Stats Section
st.markdown("### 📊 Platform Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-label">Training Data</div>
        <div class="stats-number">10,000+</div>
        <div class="stats-label">Records Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-label">Models Trained</div>
        <div class="stats-number">3</div>
        <div class="stats-label">Prediction Modules</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-label">Input Features</div>
        <div class="stats-number">17</div>
        <div class="stats-label">Variables Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stats-box">
        <div class="stats-label">Interpretability</div>
        <div class="stats-number">🟢</div>
        <div class="stats-label">SHAP Explainable</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Modules Section
st.markdown("### 📍 Explore Our Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="module-card">
        <h3>💕 Love Marriage Predictor</h3>
        <p>
            Determine whether a marriage is based on love or arranged marriage using ML classification.
            Get probability scores and understand key driving factors via SHAP analysis.
        </p>
        <p><strong>What you get:</strong></p>
        <ul>
            <li>Love Marriage Probability Gauge</li>
            <li>Confidence Level Assessment</li>
            <li>SHAP Feature Importance Chart</li>
            <li>Top Contributing Factors</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Go to Love Marriage Predictor", key="module1", use_container_width=True):
        st.switch_page("pages/1_Love_Marriage_Predictor.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <h3>✨ Marriage Success Predictor</h3>
        <p>
            Analyze divorce risk and predict marital satisfaction levels.
            Comprehensive risk assessment with SHAP-based feature analysis.
        </p>
        <p><strong>What you get:</strong></p>
        <ul>
            <li>Success Probability Gauge</li>
            <li>Divorce Risk Assessment</li>
            <li>Satisfaction Level Prediction</li>
            <li>Risk Factor Breakdown</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Go to Marriage Success Predictor", key="module2", use_container_width=True):
        st.switch_page("pages/2_Marriage_Success_Predictor.py")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="module-card">
        <h3>🎯 Improve My Chances</h3>
        <p>
            Get personalized counterfactual recommendations to improve your marriage outcome.
            Discover what changes would have the biggest positive impact.
        </p>
        <p><strong>What you get:</strong></p>
        <ul>
            <li>Actionable Improvement Suggestions</li>
            <li>Before/After Comparisons</li>
            <li>Impact Quantification</li>
            <li>Priority-Ranked Recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Go to Improve My Chances", key="module3", use_container_width=True):
        st.switch_page("pages/3_Improve_My_Chances.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <h3>ℹ️ About This Project</h3>
        <p>
            Learn about the dataset, model architecture, and technical implementation.
            Understand the science behind LoveMatch AI predictions.
        </p>
        <p><strong>What you'll find:</strong></p>
        <ul>
            <li>Dataset Overview</li>
            <li>Model Architecture Details</li>
            <li>Tech Stack Information</li>
            <li>Feature Descriptions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Go to About", key="module4", use_container_width=True):
        st.switch_page("pages/4_About.py")

st.divider()

# How It Works Section
st.markdown("""
<div class="how-it-works">
    <h2>🔍 How It Works</h2>
    
    <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
            <h4>Fill Your Profile</h4>
            <p>Enter marriage details including demographics, family background, and relationship factors across 17 input features.</p>
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">2</div>
        <div class="step-content">
            <h4>Run ML Models</h4>
            <p>Three XGBoost models process your data to predict marriage type (love/arranged), divorce risk, and satisfaction level.</p>
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">3</div>
        <div class="step-content">
            <h4>Get Explanations</h4>
            <p>SHAP values break down each prediction, showing exactly which factors influenced the outcome.</p>
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">4</div>
        <div class="step-content">
            <h4>Receive Recommendations</h4>
            <p>Get actionable counterfactual suggestions to improve outcomes, ranked by impact.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Tech Stack Section
st.markdown("### 🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **ML/AI Models:**
    - XGBoost (Gradient Boosting)
    - SHAP (Feature Importance)
    - DiCE (Counterfactuals)
    """)

with col2:
    st.markdown("""
    **Data Processing:**
    - Pandas & NumPy
    - Scikit-learn (Preprocessing)
    - Joblib (Model Serialization)
    """)

with col3:
    st.markdown("""
    **Frontend & Deployment:**
    - Streamlit (Web Framework)
    - Plotly (Interactive Charts)
    - Streamlit Cloud (Hosting)
    """)

st.divider()

# Footer with usage tips
st.markdown("### 💡 Usage Tips")

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    st.info("""
    **📋 Input Requirements**
    
    All 17 features must be filled to generate predictions. Use realistic values for best results.
    """)

with tip_col2:
    st.info("""
    **📊 Understanding Outputs**
    
    SHAP charts show feature importance. Red = increases probability, Blue = decreases.
    """)

with tip_col3:
    st.info("""
    **🎯 Counterfactuals**
    
    "Improve My Chances" generates 3 top suggestions ranked by impact on outcome.
    """)

st.divider()

# Sidebar information
with st.sidebar:
    st.markdown("### 🔗 Quick Links")
    
    if st.button("📍 Love Marriage Predictor"):
        st.switch_page("pages/1_Love_Marriage_Predictor.py")
    
    if st.button("✨ Marriage Success Predictor"):
        st.switch_page("pages/2_Marriage_Success_Predictor.py")
    
    if st.button("🎯 Improve My Chances"):
        st.switch_page("pages/3_Improve_My_Chances.py")
    
    if st.button("ℹ️ About"):
        st.switch_page("pages/4_About.py")
    
    st.divider()
    
    st.markdown("### 📚 About")
    st.info("""
    **LoveMatch AI v1.0**
    
    A machine learning platform for predicting Indian marriage outcomes using XGBoost, SHAP, and counterfactual explanations.
    
    Trained on 10,000+ real marriage records with 17 input features.
    """)
    
    st.markdown("### 🌐 Social & Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[GitHub](https://github.com)")
    with col2:
        st.markdown("[Kaggle](https://kaggle.com)")
    with col3:
        st.markdown("[LinkedIn](https://linkedin.com)")

# Bottom note
st.markdown("""
---
**Disclaimer:** This tool is for educational and entertainment purposes. Predictions are probabilistic and should not be used as a sole basis for major life decisions. Always consult with professionals for relationship or life advice.
""")
