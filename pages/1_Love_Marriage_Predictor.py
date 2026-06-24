"""
Module 1: Love Marriage Predictor
Predicts whether a marriage is based on Love or Arranged using ML classification.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Import helper functions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.preprocess import (
    safe_model_load,
    safe_preprocessor_load,
    safe_feature_load,
    build_input_form_fields,
    create_input_dataframe,
    format_probability,
    get_confidence_label,
    preprocess_input
)
from src.explainer import (
    create_shap_explainer,
    plot_shap_waterfall,
    plot_shap_bar_top_features
)

# Page configuration
st.set_page_config(
    page_title="Love Marriage Predictor - LoveMatch AI",
    page_icon="💕",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #FF6B6B;
        --secondary: #2C3E50;
    }
    
    .main {
        background: linear-gradient(135deg, #F8F9FA 0%, #E8EAED 100%);
    }
    
    .prediction-result {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.2);
    }
    
    .prediction-result h2 {
        margin-top: 0;
        font-size: 2.2em;
        font-weight: 800;
    }
    
    .prediction-result p {
        font-size: 1.1em;
        margin: 10px 0;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 12px 25px;
        background: rgba(255,255,255,0.25);
        border-radius: 25px;
        margin: 15px 0;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    .form-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .form-section h3 {
        color: #2C3E50;
        margin-bottom: 20px;
        font-size: 1.4em;
        font-weight: 700;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-bottom: 4px solid #FF6B6B;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
    }
    
    .shap-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Page title
st.title("💕 Love Marriage Predictor")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
Determine whether a marriage is based on <strong>Love</strong> or <strong>Arranged</strong>. Get detailed predictions with SHAP-powered explainability.
</p>
""", unsafe_allow_html=True)

st.divider()

# Load models and preprocessors with error handling
try:
    model = safe_model_load('love_marriage_model.pkl', 'Love Marriage Model')
    preprocessor = safe_preprocessor_load('love_preprocessor.pkl', 'Love Marriage Preprocessor')
    feature_names = safe_feature_load('love_feature_names.pkl', 'Feature Names')
    feature_cols = safe_feature_load('love_feature_cols.pkl', 'Feature Columns')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Please ensure all model files are present in the `models/` folder.")
    st.stop()

# Create two-column layout: inputs on left, results on right
col1, col2 = st.columns([1.1, 1], gap="large")

# LEFT COLUMN: Input Form
with col1:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Your Profile")
        
        with st.form("love_marriage_form"):
            user_input = build_input_form_fields(feature_cols)
            
            submit_button = st.form_submit_button(
                "🔮 Predict Marriage Type",
                use_container_width=True,
                type="primary"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: Results
with col2:
    st.markdown("### 📊 Results")
    
    if submit_button:
        try:
            # Validate input
            if not all(user_input.values()):
                st.error("⚠️ Please fill in all fields!")
                st.stop()
            
            # Create DataFrame and preprocess
            input_df = create_input_dataframe(user_input, feature_cols)
            X_processed = preprocessor.transform(input_df)
            
            # Make prediction
            prediction_proba = model.predict_proba(X_processed)
            love_prob = prediction_proba[0][1]  # Probability of Love Marriage
            arranged_prob = prediction_proba[0][0]  # Probability of Arranged Marriage
            
            # Display main prediction
            prediction_label = "💕 Love Marriage" if love_prob > 0.5 else "👨‍👩‍👧‍👦 Arranged Marriage"
            
            st.markdown(f"""
            <div class="prediction-result">
                <h2>{prediction_label}</h2>
                <p>Predicted Classification</p>
                <div class="confidence-badge">{get_confidence_label(max(love_prob, arranged_prob))}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Probability display
            col_prob1, col_prob2 = st.columns(2)
            
            with col_prob1:
                st.metric(
                    label="💕 Love Marriage",
                    value=format_probability(love_prob),
                    delta=f"{(love_prob - 0.5) * 100:.1f}%" if love_prob > 0.5 else None
                )
            
            with col_prob2:
                st.metric(
                    label="👨‍👩‍👧‍👦 Arranged Marriage Probability",
                    value=format_probability(arranged_prob),
                    delta=f"{(arranged_prob - 0.5) * 100:.1f}%" if arranged_prob > 0.5 else None
                )
            
            # Probability gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=love_prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Love Marriage Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#e74c3c"},
                    'steps': [
                        {'range': [0, 25], 'color': "#ecf0f1"},
                        {'range': [25, 50], 'color': "#bdc3c7"},
                        {'range': [50, 75], 'color': "#3498db"},
                        {'range': [75, 100], 'color': "#e74c3c"}
                    ],
                    'threshold': {
                        'line': {'color': "darkred", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Store results in session state for SHAP visualization
            st.session_state.love_prediction = {
                'proba': prediction_proba,
                'X_processed': X_processed,
                'love_prob': love_prob,
                'user_input': user_input
            }
            
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            st.info("Please check your inputs and try again.")

st.divider()

# SHAP Explainability Section
st.markdown("### 🔍 Feature Importance & Explainability")

if 'love_prediction' in st.session_state:
    try:
        X_processed = st.session_state.love_prediction['X_processed']
        
        # Create SHAP explainer
        explainer = create_shap_explainer(model, X_processed)
        
        # Create tabs for different visualizations
        tab1, tab2 = st.tabs(["📊 SHAP Waterfall", "📈 Feature Importance"])
        
        with tab1:
            st.markdown("""
            **SHAP Waterfall Chart:** Shows how each feature contributes to pushing the prediction 
            towards Love Marriage (red, positive) or Arranged Marriage (blue, negative).
            """)
            
            fig_waterfall = plot_shap_waterfall(
                explainer,
                X_processed,
                feature_names,
                expected_value_idx=1
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            st.markdown("""
            **How to read this chart:**
            - 📊 Longer red bars = stronger influence towards Love Marriage
            - 📊 Longer blue bars = stronger influence towards Arranged Marriage
            - The base value is the model's baseline prediction before considering any features
            """)
        
        with tab2:
            st.markdown("""
            **Feature Importance:** Top 10 features by absolute impact on this prediction.
            """)
            
            fig_importance = plot_shap_bar_top_features(
                explainer,
                X_processed,
                feature_names,
                top_n=10
            )
            st.plotly_chart(fig_importance, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        
        # Get SHAP values for interpretation
        shap_values = explainer.shap_values(X_processed)
        if isinstance(shap_values, list):
            shap_vals = shap_values[1][0]
        else:
            shap_vals = shap_values[0]
        
        # Find top features
        top_indices = np.argsort(np.abs(shap_vals))[-3:][::-1]
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        for i, idx in enumerate(top_indices):
            if i == 0:
                col = insight_col1
            elif i == 1:
                col = insight_col2
            else:
                col = insight_col3
            
            with col:
                feature_name = feature_names[idx]
                shap_value = shap_vals[idx]
                direction = "→ Love Marriage" if shap_value > 0 else "→ Arranged Marriage"
                color = "#e74c3c" if shap_value > 0 else "#3498db"
                
                st.markdown(f"""
                **Top Feature #{i+1}**
                
                {feature_name}  
                Impact: {abs(shap_value):.3f}  
                <span style="color: {color};">{direction}</span>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"⚠️ Could not generate SHAP explanations: {str(e)}")
        st.info("This might be due to model compatibility. The main prediction is still available above.")

else:
    st.info("👆 Fill the form and click 'Predict' to see detailed feature importance analysis.")

st.divider()

# Information section
with st.expander("ℹ️ About This Module"):
    st.markdown("""
    ### How It Works
    
    This module uses an **XGBoost classifier** trained on 10,000+ marriage records to predict 
    whether a marriage is based on love or arranged union.
    
    **Input Features:** 17 demographic and relationship factors
    - Marriage type indicators (Love/Arranged flag in training)
    - Demographics: Age, Gender, Education, Income
    - Family factors: Caste, Religion, Parental Approval
    - Relationship factors: Urban/Rural, Dowry, Working Status
    
    **Model Performance:**
    - Algorithm: XGBoost (Gradient Boosting)
    - Interpretability: SHAP TreeExplainer
    - Prediction Type: Binary Classification (Love vs Arranged)
    
    **Explainability:**
    - SHAP values quantify each feature's contribution
    - Waterfall charts show cumulative impact
    - Feature importance ranks by absolute influence
    """)

# Footer
st.markdown("""
---
**Note:** This prediction is probabilistic. Always consult with loved ones and professionals for life decisions.
""")
