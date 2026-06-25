"""
Module 2: Marriage Success Predictor
Predicts divorce risk and marital satisfaction levels using ML models.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    get_confidence_label
)
from src.explainer import (
    create_shap_explainer,
    plot_shap_bar_top_features,
    create_success_gauge,
    plot_satisfaction_distribution
)

# Import label encoder load function
def safe_label_encoder_load(encoder_name: str, display_name: str = None):
    """Safely load a label encoder."""
    from src.preprocess import load_label_encoder
    try:
        return load_label_encoder(encoder_name)
    except FileNotFoundError:
        st.error(f"❌ {display_name or encoder_name} not found!")
        st.info(f"Please ensure `{encoder_name}` exists in the `models/` folder.")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="Marriage Success Predictor - LoveMatch AI",
    page_icon="✨",
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
    
    .success-metric {
        background: linear-gradient(135deg, #27AE60 0%, #229954 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.2);
    }
    
    .risk-metric {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.2);
    }
    
    .satisfaction-metric {
        background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(243, 156, 18, 0.2);
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 800;
        margin: 12px 0;
    }
    
    .metric-label {
        font-size: 0.85em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .form-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Page title
st.title("✨ Marriage Success Predictor")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
Analyze divorce risk and predict marital satisfaction. Discover what factors influence marriage outcomes with data-driven insights.
</p>
""", unsafe_allow_html=True)

st.divider()

# Load all models and preprocessors
try:
    # Divorce prediction models
    divorce_model = safe_model_load('divorce_model.pkl', 'Divorce Prediction Model')
    divorce_preprocessor = safe_preprocessor_load('divorce_preprocessor.pkl', 'Divorce Preprocessor')
    divorce_feature_names = safe_feature_load('divorce_feature_names.pkl', 'Divorce Feature Names')
    divorce_feature_cols = safe_feature_load('divorce_feature_cols.pkl', 'Divorce Feature Columns')
    
    # Satisfaction prediction models
    satisfaction_model = safe_model_load(
        'satisfaction_model.pkl',
        'Satisfaction Model'
    )

    sat_preprocessor = safe_preprocessor_load(
        'sat_preprocessor.pkl',
        'Satisfaction Preprocessor'
    )

    sat_feature_names = safe_feature_load(
        'sat_feature_names.pkl',
        'Satisfaction Feature Names'
    )

    sat_feature_cols = safe_feature_load(
        'sat_feature_cols.pkl',
        'Satisfaction Feature Columns'
    )

    sat_label_encoder = safe_label_encoder_load(
        'sat_label_encoder.pkl',
        'Satisfaction Label Encoder'
    )
    
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Please ensure all model files are present in the `models/` folder.")
    st.stop()

# Create two-column layout
col1, col2 = st.columns([1.1, 1], gap="large")

# LEFT COLUMN: Input Form
with col1:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Your Profile")
        
        with st.form("success_predictor_form"):
            user_input = build_input_form_fields(sat_feature_cols)
            
            submit_button = st.form_submit_button(
                "🔮 Predict Marriage Success",
                use_container_width=True,
                type="primary"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: Results
with col2:
    st.markdown("### 📊 Analysis")
    
    if submit_button:
        try:
            # Validate input
            if any(v is None for v in user_input.values()):
                st.error("⚠️ Please fill in all fields!")
                st.stop()


            # Build separate inputs
            input_divorce = create_input_dataframe(
                user_input,
                divorce_feature_cols
            )

            input_sat = create_input_dataframe(
                user_input,
                sat_feature_cols
            )


            # Preprocess
            X_divorce = divorce_preprocessor.transform(
                input_divorce
            )

            X_satisfaction = sat_preprocessor.transform(
                input_sat
            )
                
            # Make predictions
            divorce_proba = divorce_model.predict_proba(X_divorce)
            divorce_prob = divorce_proba[0][1]  # Probability of divorce
            success_prob = 1 - divorce_prob  # Probability of no divorce
            
            satisfaction_proba = satisfaction_model.predict_proba(X_satisfaction)
            satisfaction_pred = satisfaction_model.predict(X_satisfaction)[0]
            satisfaction_label = sat_label_encoder.inverse_transform([satisfaction_pred])[0]
            
            # Display key metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.markdown(f"""
                <div class="success-metric">
                    <div class="metric-label">Marriage Success Probability</div>
                    <div class="metric-value">{format_probability(success_prob)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown(f"""
                <div class="risk-metric">
                    <div class="metric-label">Divorce Risk</div>
                    <div class="metric-value">{format_probability(divorce_prob)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_col3:
                satisfaction_color = {
                    'Low': '#e74c3c',
                    'Medium': '#f39c12',
                    'High': '#27ae60'
                }.get(satisfaction_label, '#95a5a6')
                
                st.markdown(f"""
                <div class="satisfaction-metric" style="background: linear-gradient(135deg, {satisfaction_color} 0%, {satisfaction_color}cc 100%);">
                    <div class="metric-label">Predicted Satisfaction</div>
                    <div class="metric-value" style="font-size: 1.8em;">{satisfaction_label}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display gauge chart
            fig_gauge = create_success_gauge(success_prob, divorce_prob)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Satisfaction distribution chart
            fig_satisfaction = plot_satisfaction_distribution(
                satisfaction_model,
                satisfaction_proba,
                sat_label_encoder
            )
            st.plotly_chart(fig_satisfaction, use_container_width=True)
            
            # Store results for SHAP visualization
            st.session_state.success_prediction = {
                'divorce_proba': divorce_proba,
                'X_divorce': X_divorce,
                'success_prob': success_prob,
                'divorce_prob': divorce_prob,
                'satisfaction_pred': satisfaction_pred,
                'satisfaction_label': satisfaction_label,
                'satisfaction_proba': satisfaction_proba,
                'user_input': user_input
            }
            
            # Display insights
            st.markdown("### 💡 Quick Insights")
            
            insight_col1, insight_col2 = st.columns(2)
            
            with insight_col1:
                if success_prob >= 0.8:
                    st.success("✅ High likelihood of marital success!")
                elif success_prob >= 0.6:
                    st.info("⚠️ Moderate success probability - attention to key factors recommended")
                else:
                    st.error("❌ Elevated divorce risk - significant interventions may be needed")
            
            with insight_col2:
                if satisfaction_label == "High":
                    st.success("😊 Expected marital satisfaction is high")
                elif satisfaction_label == "Medium":
                    st.info("😐 Expected marital satisfaction is moderate")
                else:
                    st.warning("😞 Expected marital satisfaction may be low")
            
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            st.info("Please check your inputs and try again.")

st.divider()

# SHAP Explainability Section
st.markdown("### 🔍 Feature Importance & Risk Factors")

if 'success_prediction' in st.session_state:
    try:
        X_divorce = st.session_state.success_prediction['X_divorce']
        
        # Create SHAP explainer for divorce model
        explainer = create_shap_explainer(divorce_model, X_divorce)
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs([
            "📊 Top Success Factors",
            "⚠️ Divorce Risk Drivers",
            "📈 Satisfaction Breakdown"
        ])
        
        with tab1:
            st.markdown("""
            **Top Features Driving Marriage Success:** 
            These features have the strongest positive influence on avoiding divorce.
            """)
            
            fig_success = plot_shap_bar_top_features(
                explainer,
                X_divorce,
                divorce_feature_names,
                top_n=10
            )
            st.plotly_chart(fig_success, use_container_width=True)
        
        with tab2:
            st.markdown("""
            **Top Divorce Risk Factors:**
            These features most strongly influence divorce probability in your profile.
            """)
            
            # Get SHAP values
            shap_values = explainer.shap_values(X_divorce)
            if isinstance(shap_values, list):
                shap_vals = shap_values[1][0]  # Divorce class
            else:
                shap_vals = shap_values[0]
            
            # Create risk factors DataFrame
            risk_df = pd.DataFrame({
                'Feature': divorce_feature_names,
                'Risk Impact': np.abs(shap_vals)
            }).sort_values('Risk Impact', ascending=True).tail(10)
            
            fig_risk = px.bar(
                risk_df,
                x='Risk Impact',
                y='Feature',
                orientation='h',
                title="Top 10 Divorce Risk Factors",
                labels={'Risk Impact': 'Impact Magnitude'},
                color='Risk Impact',
                color_continuous_scale='Reds'
            )
            
            fig_risk.update_layout(height=400, showlegend=False, template="plotly_white")
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with tab3:
            st.markdown("""
            **Satisfaction Level Probabilities:**
            Likelihood of each satisfaction level based on your profile.
            """)
            
            satisfaction_data = pd.DataFrame({
                'Satisfaction Level': sat_label_encoder.classes_,
                'Probability': st.session_state.success_prediction['satisfaction_proba'][0]
            })
            
            fig_sat_detail = px.bar(
                satisfaction_data,
                x='Satisfaction Level',
                y='Probability',
                title="Marital Satisfaction Distribution",
                color='Satisfaction Level',
                color_discrete_map={
                    'Low': '#e74c3c',
                    'Medium': '#f39c12',
                    'High': '#27ae60'
                }
            )
            
            fig_sat_detail.update_layout(
                height=300,
                showlegend=False,
                template="plotly_white",
                yaxis_title="Probability",
                xaxis_title="Satisfaction Level"
            )
            st.plotly_chart(fig_sat_detail, use_container_width=True)
        
    except Exception as e:
        st.warning(f"⚠️ Could not generate detailed analysis: {str(e)}")

else:
    st.info("👆 Fill the form and click 'Predict' to see detailed risk factor analysis.")

st.divider()

# Detailed insights section
with st.expander("📚 Understanding the Results"):
    st.markdown("""
    ### What These Metrics Mean
    
    **Marriage Success Probability:**
    - Probability that the marriage will NOT end in divorce based on input factors
    - Calculated from the divorce prediction model (1 - divorce probability)
    - Ranges from 0% to 100%
    
    **Divorce Risk:**
    - Probability of divorce given current relationship characteristics
    - Inverse of success probability
    - Higher values indicate elevated risk factors
    
    **Marital Satisfaction:**
    - Predicted satisfaction level: Low, Medium, or High
    - Based on demographic and relationship factors
    - Multiclass classification using XGBoost
    
    ### How to Use Feature Importance
    
    - **Red/Warm colors** = Higher risk contribution
    - **Features further right** = Stronger influence on prediction
    - Focus on modifiable factors (income, approval, working status)
    - Some factors (age, caste) are descriptive, not actionable
    """)

# Information section
with st.expander("ℹ️ About This Module"):
    st.markdown("""
    ### Model Architecture
    
    **Divorce Prediction Model:**
    - Algorithm: XGBoost Binary Classifier
    - Target: Divorce Status (Yes/No)
    - Prediction Type: Probability of divorce
    
    **Marital Satisfaction Model:**
    - Algorithm: XGBoost Multiclass Classifier
    - Target: Satisfaction Level (Low, Medium, High)
    - Output: Class probabilities and predicted class
    
    **Input Features (17 total):**
    - Demographics: Age at marriage, Gender, Education, Income
    - Family Background: Religion, Caste, Parental approval, Inter-caste/religion
    - Relationship: Marriage type, Urban/Rural, Dowry, Spouse working status
    - Outcome: Children count, Years since marriage
    
    ### Feature Importance Interpretation
    
    SHAP values show:
    - Which features push towards divorce risk
    - Which features protect against divorce
    - Relative importance of each feature
    """)

# Footer
st.markdown("""
---
**Important:** These predictions are based on statistical patterns and should not replace professional counseling or advice.
""")
