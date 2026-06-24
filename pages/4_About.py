"""
Module 4: About LoveMatch AI
Project information, dataset details, model architecture, and tech stack.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About - LoveMatch AI",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .section-header {
        color: #FF6B6B;
        font-size: 1.6em;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 3px solid #FF6B6B;
        padding-bottom: 12px;
    }
    
    .feature-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 12px 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .model-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.2);
    }
    
    .model-card h3 {
        margin-top: 0;
        font-size: 1.3em;
    }
    
    .tech-item {
        background: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #2c3e50;
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .stat-label {
        font-weight: 600;
        color: #2c3e50;
    }
    
    .stat-value {
        color: #FF6B6B;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Page title
st.title("ℹ️ About LoveMatch AI")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
A machine learning platform leveraging XGBoost and SHAP for predicting Indian marriage outcomes with explainable AI insights.
</p>
""", unsafe_allow_html=True)

st.divider()

# Overview section
st.markdown("""
### 🎯 Project Overview

**LoveMatch AI** is an intelligent platform that leverages machine learning to predict and analyze 
Indian marriage outcomes. Using data from 10,000+ real marriage records and advanced explainable AI 
techniques, the system provides:

1. **Marriage Type Classification** - Predict if a marriage is love-based or arranged
2. **Success Analysis** - Assess divorce risk and marital satisfaction
3. **Actionable Insights** - Get counterfactual recommendations to improve outcomes
4. **Explainability** - Understand WHY the model made each prediction using SHAP values
""")

st.divider()

# Dataset Section
st.markdown("<div class='section-header'>📊 Dataset Information</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", "10,000+")
with col2:
    st.metric("Input Features", "17")
with col3:
    st.metric("Geographic Focus", "India")
with col4:
    st.metric("Target Variables", "3")

st.markdown("### Dataset Characteristics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Data Domains:**
    - Demographic information
    - Family background
    - Relationship dynamics
    - Social factors
    - Economic indicators
    """)

with col2:
    st.markdown("""
    **Collection Method:**
    - Real marriage records
    - Indian marriage surveys
    - Diverse regions & communities
    - Multiple socioeconomic levels
    - Various age groups
    """)

st.markdown("### Input Features (17 Total)")

features_data = {
    "Category": [
        "Numeric", "Numeric", "Numeric",
        "Categorical", "Categorical", "Categorical", "Categorical", "Categorical",
        "Categorical", "Categorical", "Categorical", "Categorical", "Categorical", "Categorical",
        "Numeric", "Numeric", "Categorical"
    ],
    "Feature": [
        "Age at Marriage", "Children Count", "Years Since Marriage",
        "Gender", "Marriage Type", "Education Level", "Income Level", "Caste Match",
        "Religion", "Parental Approval", "Urban/Rural", "Dowry Exchanged", "Spouse Working", "Inter-Caste",
        "Age at Marriage (scaled)", "Years Since Marriage (scaled)", "Inter-Religion"
    ],
    "Description": [
        "Age when married (18-60)", "Number of children (0-10)", "Marriage duration in years (0-50)",
        "Male/Female", "Love/Arranged", "School/Graduate/Postgraduate/PhD", "Low/Middle/High", "Same/Different",
        "Hindu/Muslim/Sikh/Christian/Others", "No/Partial/Yes", "Urban/Rural", "Yes/No/Not Disclosed", "Yes/No", "Yes/No",
        "Standardized age feature", "Standardized duration feature", "Yes/No"
    ]
}

features_df = pd.DataFrame(features_data)

# Display features by category
st.markdown("**Numeric Features (Continuous):**")
numeric_features = features_df[features_df["Category"] == "Numeric"]
for _, row in numeric_features.iterrows():
    st.markdown(f"""
    <div class="feature-box">
        <strong>{row['Feature']}</strong><br>
        {row['Description']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Categorical Features (Discrete):**")
categorical_features = features_df[features_df["Category"] == "Categorical"]
for _, row in categorical_features.iterrows():
    st.markdown(f"""
    <div class="feature-box">
        <strong>{row['Feature']}</strong><br>
        {row['Description']}
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Target Variables")

target_data = {
    "Module": [
        "Love Marriage Predictor",
        "Marriage Success Predictor",
        "Marital Satisfaction"
    ],
    "Target Variable": [
        "Marriage Type",
        "Divorce Status",
        "Marital Satisfaction"
    ],
    "Classes": [
        "Love (1) / Arranged (0)",
        "Divorced (1) / Together (0)",
        "Low / Medium / High"
    ],
    "Type": [
        "Binary Classification",
        "Binary Classification",
        "Multiclass Classification"
    ]
}

import pandas as pd
target_df = pd.DataFrame(target_data)
st.dataframe(target_df, use_container_width=True, hide_index=True)

st.divider()

# Model Architecture Section
st.markdown("<div class='section-header'>🤖 Model Architecture</div>", unsafe_allow_html=True)

st.markdown("""
### Training Pipeline

**Step 1: Data Preprocessing**
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Numeric Features:**
    - StandardScaler normalization
    - Features: Age, Children Count, Years Since Marriage
    - Range: [0, 1] after scaling
    """)

with col2:
    st.markdown("""
    **Ordinal Features:**
    - OrdinalEncoder
    - Education Level, Income, Parental Approval
    - Respects order: Low → High
    """)

st.markdown("""
**Categorical Features:**
- OneHotEncoder
- Gender, Religion, Caste, Urban/Rural, Dowry, Working Status, etc.
- Binary columns per category
""")

st.markdown("### Three Specialized Models")

# Model 1
st.markdown("""
<div class="model-card">
    <h3>💕 Module 1: Love Marriage Predictor</h3>
    <div class="stat-row">
        <span class="stat-label">Algorithm:</span>
        <span class="stat-value">XGBoost Binary Classifier</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Target:</span>
        <span class="stat-value">Marriage Type (Love=1, Arranged=0)</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Input Features:</span>
        <span class="stat-value">All 17 features</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Output:</span>
        <span class="stat-value">Probability [0-1] of being Love Marriage</span>
    </div>
    <div class="stat-row">
        <span class="stat-label">Explainability:</span>
        <span class="stat-value">SHAP TreeExplainer</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Model 2
st.markdown("""
<div class="model-card" style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);">
    <h3>✨ Module 2: Marriage Success Predictor</h3>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Algorithm:</span>
        <span class="stat-value">XGBoost Binary Classifier</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Target 1:</span>
        <span class="stat-value">Divorce Status (Yes=1, No=0)</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Target 2:</span>
        <span class="stat-value">Satisfaction (Low/Medium/High)</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Input Features:</span>
        <span class="stat-value">All 17 features</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Explainability:</span>
        <span class="stat-value">SHAP for feature importance</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Model 3
st.markdown("""
<div class="model-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%);">
    <h3>🎯 Module 3: Counterfactual Recommender</h3>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Approach:</span>
        <span class="stat-value">DiCE-inspired Iterative Search</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Technique:</span>
        <span class="stat-value">Feature modification + re-prediction</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Output:</span>
        <span class="stat-value">Top 3 actionable suggestions</span>
    </div>
    <div class="stat-row" style="border-bottom-color: rgba(255,255,255,0.2);">
        <span class="stat-label">Ranking:</span>
        <span class="stat-value">By improvement percentage</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Explainability Methods")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **SHAP (SHapley Additive exPlanations):**
    - Model-agnostic feature importance
    - Waterfall plots for individual predictions
    - Feature contribution quantification
    - Cumulative model impact visualization
    """)

with col2:
    st.markdown("""
    **DiCE (Diverse Counterfactual Explanations):**
    - "What-if" scenario generation
    - Minimal change suggestions
    - Actionable recommendations
    - Before/after comparisons
    """)

st.divider()

# Tech Stack Section
st.markdown("<div class='section-header'>🛠️ Technology Stack</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ML/AI Libraries")
    st.markdown("""
    <div class="tech-item">
        <strong>XGBoost</strong><br>
        Gradient Boosting for all predictions
    </div>
    <div class="tech-item">
        <strong>SHAP</strong><br>
        Feature importance & explainability
    </div>
    <div class="tech-item">
        <strong>Scikit-learn</strong><br>
        Data preprocessing & pipelines
    </div>
    <div class="tech-item">
        <strong>NumPy & Pandas</strong><br>
        Numerical & data manipulation
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Web & Visualization")
    st.markdown("""
    <div class="tech-item">
        <strong>Streamlit</strong><br>
        Web app framework
    </div>
    <div class="tech-item">
        <strong>Plotly</strong><br>
        Interactive charts
    </div>
    <div class="tech-item">
        <strong>Plotly Express</strong><br>
        High-level plotting API
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### Infrastructure & Tools")
    st.markdown("""
    <div class="tech-item">
        <strong>Streamlit Cloud</strong><br>
        FREE hosting & deployment
    </div>
    <div class="tech-item">
        <strong>Joblib</strong><br>
        Model serialization
    </div>
    <div class="tech-item">
        <strong>Python 3.10+</strong><br>
        Core language
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Model Performance Section
st.markdown("<div class='section-header'>📈 Model Performance Overview</div>", unsafe_allow_html=True)

st.markdown("""
All models use **XGBoost with hyperparameter tuning** to balance:
- ✅ **Accuracy** - Correct predictions
- ✅ **Interpretability** - SHAP explainability
- ✅ **Generalization** - Performance on unseen data
- ✅ **Speed** - Fast inference (<100ms per prediction)

**Note:** Detailed performance metrics (precision, recall, F1, ROC-AUC) are available 
in the model training documentation.
""")

st.divider()

# Features & Capabilities Section
st.markdown("<div class='section-header'>✨ Key Features</div>", unsafe_allow_html=True)

features = [
    ("🔮 Probabilistic Predictions", "Get confidence scores for each prediction"),
    ("📊 SHAP Explainability", "Understand which factors drive each outcome"),
    ("🎯 Counterfactual Recommendations", "Get actionable suggestions for improvement"),
    ("📈 Interactive Visualizations", "Gauge charts, waterfall plots, bar charts"),
    ("⚡ Fast Inference", "Predictions in milliseconds"),
    ("🔒 Privacy-Focused", "No data storage or tracking"),
    ("📱 Responsive Design", "Works on mobile and desktop"),
    ("🌐 Free Deployment", "Streamlit Community Cloud hosting")
]

for title, desc in features:
    st.markdown(f"**{title}**  \n{desc}\n")

st.divider()

# Limitations & Disclaimers
st.markdown("<div class='section-header'>⚠️ Limitations & Disclaimers</div>", unsafe_allow_html=True)

st.warning("""
### Important Disclaimers

1. **Educational Purpose:** This system is designed for educational and entertainment purposes only.

2. **Not Medical/Legal Advice:** Predictions should NOT replace professional counseling or advice.

3. **Probabilistic:** Predictions are based on statistical patterns in historical data, not certainties.

4. **Correlation ≠ Causation:** ML models identify correlations, not causal relationships.

5. **Data Limitations:** 
   - Based on 10,000 Indian marriage records
   - May not represent all communities or demographics
   - Cultural factors change over time

6. **Unmeasured Factors:** Real relationships involve emotional, psychological, and social factors 
   not captured in this dataset.

7. **Use Responsibly:** Always consult with real professionals for major life decisions.

### What The Models CAN Do
- Identify patterns in marriage outcomes
- Highlight key statistical factors
- Provide probabilistic estimates
- Suggest areas for improvement

### What The Models CANNOT Do
- Guarantee specific outcomes
- Predict individual love or compatibility
- Account for human factors (communication, commitment, growth)
- Predict future major life events
- Replace human judgment or professional advice
""")

st.divider()

# Development & Attribution
st.markdown("<div class='section-header'>👨‍💻 Development</div>", unsafe_allow_html=True)

st.markdown("""
### Technology & Methodology

- **ML Framework:** XGBoost (Gradient Boosting)
- **Explainability:** SHAP (SHapley Additive exPlanations)
- **Recommendations:** DiCE-inspired counterfactual approach
- **Data Science:** Full pipeline from preprocessing to deployment
- **Web Framework:** Streamlit with Plotly visualizations

### Open Source Libraries Used

This project leverages excellent open-source libraries:
- [XGBoost](https://xgboost.readthedocs.io/) - Gradient boosting library
- [SHAP](https://shap.readthedocs.io/) - Model explainability
- [Streamlit](https://streamlit.io/) - Web app framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Scikit-learn](https://scikit-learn.org/) - ML utilities

### Contact & Feedback

Have questions or suggestions? Feel free to reach out:
- **GitHub:** [Repository Link]
- **Email:** [Contact Email]
- **LinkedIn:** [Profile Link]
""")

st.divider()

# Footer
st.markdown("""
---
**LoveMatch AI v1.0** | An Explainable ML Project for Marriage Outcome Prediction

Built with ❤️ using Python, XGBoost, SHAP, and Streamlit  
Deployed on Streamlit Community Cloud

*Remember: Real relationships thrive on communication, commitment, and genuine effort.*
""")
