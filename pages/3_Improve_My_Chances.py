"""
Module 3: Improve My Chances
Generates personalized counterfactual recommendations to improve marriage outcomes.
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
    format_probability
)
from src.explainer import (
    CounterfactualExplainer,
    display_counterfactual_suggestions,
    create_comparison_dataframe
)

# Page configuration
st.set_page_config(
    page_title="Improve My Chances - LoveMatch AI",
    page_icon="🎯",
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
    
    .suggestion-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #F39C12;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 15px 0;
    }
    
    .suggestion-card.high {
        border-left-color: #27AE60;
        background: linear-gradient(90deg, white 0%, rgba(39, 174, 96, 0.02) 100%);
    }
    
    .suggestion-card.medium {
        border-left-color: #F39C12;
        background: linear-gradient(90deg, white 0%, rgba(243, 156, 18, 0.02) 100%);
    }
    
    .improvement-badge {
        display: inline-block;
        padding: 10px 20px;
        background: #27AE60;
        color: white;
        border-radius: 20px;
        font-weight: 600;
        margin: 10px 0;
    }
    
    .before-after {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 15px 0;
        padding: 20px;
        background: #F8F9FA;
        border-radius: 10px;
    }
    
    .before-after-item {
        text-align: center;
    }
    
    .before-after-value {
        font-size: 1.8em;
        font-weight: 800;
        color: #2C3E50;
        margin: 10px 0;
    }
    
    .before-after-label {
        font-size: 0.9em;
        color: #7f8c8d;
        text-transform: uppercase;
    }
    
    .arrow {
        font-size: 2em;
        color: #27ae60;
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
st.title("🎯 Improve My Chances")
st.markdown("""
<p style="font-size: 1.1em; color: #666; line-height: 1.7; margin-bottom: 20px;">
Get personalized recommendations to improve your marriage success probability. See exactly how changes can positively impact your outcomes.
</p>
""", unsafe_allow_html=True)

st.divider()

# Load models and preprocessors
try:
    divorce_model = safe_model_load('divorce_model.pkl', 'Divorce Model')
    divorce_preprocessor = safe_preprocessor_load('divorce_preprocessor.pkl', 'Divorce Preprocessor')
    divorce_feature_names = safe_feature_load('divorce_feature_names.pkl', 'Divorce Feature Names')
    divorce_feature_cols = safe_feature_load('divorce_feature_cols.pkl', 'Divorce Feature Columns')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Please ensure all model files are present in the `models/` folder.")
    st.stop()

# Initialize counterfactual explainer
continuous_features = ['Age_at_Marriage', 'Children_Count', 'Years_Since_Marriage']
categorical_features = [col for col in divorce_feature_cols if col not in continuous_features]

counterfactual = CounterfactualExplainer(
    model=divorce_model,
    feature_names=divorce_feature_names,
    feature_cols=divorce_feature_cols,
    continuous_features=continuous_features,
    categorical_features=categorical_features
)

# Create layout
col1, col2 = st.columns([1.1, 1], gap="large")

# LEFT COLUMN: Input Form
with col1:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Your Profile")
        
        with st.form("improve_chances_form"):
            user_input = build_input_form_fields(divorce_feature_cols)
            
            submit_button = st.form_submit_button(
                "🔍 Generate Recommendations",
                use_container_width=True,
                type="primary"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: Results
with col2:
    st.subheader("💡 Personalized Recommendations")
    
    if submit_button:
        try:
            # Validate input
            if not all(user_input.values()):
                st.error("⚠️ Please fill in all fields!")
                st.stop()
            
            # Get current prediction
            input_df = create_input_dataframe(user_input, divorce_feature_cols)
            X_current = divorce_preprocessor.transform(input_df)
            current_proba = divorce_model.predict_proba(X_current)
            current_success = 1 - current_proba[0][1]
            
            # Display current status
            st.markdown("### 📊 Your Current Outlook")
            
            current_col1, current_col2 = st.columns(2)
            
            with current_col1:
                st.metric(
                    label="Current Success Probability",
                    value=format_probability(current_success),
                    delta=None
                )
            
            with current_col2:
                if current_success >= 0.8:
                    st.success("✅ Already strong position!")
                elif current_success >= 0.6:
                    st.info("⚠️ Moderate - room for improvement")
                else:
                    st.error("❌ Elevated risk - focus on changes below")
            
            st.divider()
            
            # Generate counterfactual suggestions
            st.markdown("### 🎯 Top Recommendations to Boost Success")
            
            suggestions = counterfactual.generate_counterfactuals_simple(
                current_success,
                user_input,
                divorce_preprocessor
            )
            
            if suggestions:
                # Sort by improvement (descending)
                suggestions = sorted(
                    suggestions,
                    key=lambda x: x['improvement'],
                    reverse=True
                )
                
                for i, suggestion in enumerate(suggestions, 1):
                    improvement = suggestion['improvement']
                    
                    # Determine card style
                    if improvement >= 10:
                        card_class = "high"
                        impact_icon = "🔥"
                    elif improvement >= 5:
                        card_class = "medium"
                        impact_icon = "⬆️"
                    else:
                        card_class = "low"
                        impact_icon = "📈"
                    
                    st.markdown(f"""
                    <div class="suggestion-card {card_class}">
                        <h3>Recommendation #{i} {impact_icon}</h3>
                        <p><strong>{suggestion['description']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Before/After visualization
                    st.markdown(f"""
                    <div class="before-after">
                        <div class="before-after-item">
                            <div class="before-after-label">Current Success</div>
                            <div class="before-after-value">{format_probability(suggestion['old_value'])}</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="before-after-item">
                            <div class="before-after-label">Projected Success</div>
                            <div class="before-after-value">{format_probability(suggestion['new_value'])}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Improvement badge
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <span class="improvement-badge">
                            Improvement: +{suggestion['improvement']:.1f}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.divider()
            else:
                st.success("✅ No immediate improvements needed! Your profile is already well-positioned.")
            
            # Store session state
            st.session_state.improvement_data = {
                'current_success': current_success,
                'suggestions': suggestions,
                'user_input': user_input
            }
        
        except Exception as e:
            st.error(f"❌ Failed to generate recommendations: {str(e)}")
            st.info("Please check your inputs and try again.")

st.divider()

# Comparison Table Section
if 'improvement_data' in st.session_state:
    st.markdown("### 📋 Comparison Table")
    
    suggestions = st.session_state.improvement_data['suggestions']
    current_success = st.session_state.improvement_data['current_success']
    
    if suggestions:
        # Create comparison data
        comparison_data = []
        comparison_data.append({
            'Scenario': '📍 Current Status',
            'Success Probability': format_probability(current_success),
            'Divorce Risk': format_probability(1 - current_success),
            'Changes Required': 'None'
        })
        
        for i, suggestion in enumerate(suggestions, 1):
            comparison_data.append({
                'Scenario': f'#{i}: {suggestion["description"]}',
                'Success Probability': format_probability(suggestion['new_value']),
                'Divorce Risk': format_probability(1 - suggestion['new_value']),
                'Improvement': f"+{suggestion['improvement']:.1f}%"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Export option
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Recommendations as CSV",
            data=csv,
            file_name="lovematch_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

st.divider()

# How Counterfactuals Work
with st.expander("🔬 How Counterfactuals Work"):
    st.markdown("""
    ### Understanding Counterfactual Explanations
    
    A **counterfactual explanation** answers: "What would I need to change to get a different outcome?"
    
    **Example:**
    - **Current:** Age 28, Income Level: Low, Parental Approval: Partial
    - **Prediction:** 60% success probability
    
    **Counterfactual Suggestion:**
    - **Change:** Income Level → High
    - **New Prediction:** 72% success probability
    - **Insight:** Improving income level would increase success probability by +12%
    
    ### How We Generate Recommendations
    
    1. **Get Current Prediction:** Calculate your current success probability
    2. **Test Changes:** For each actionable feature:
       - Modify the feature to a better value
       - Preprocess and re-predict
       - If improvement detected → save suggestion
    3. **Rank by Impact:** Sort suggestions by improvement percentage
    4. **Return Top 3:** Show most impactful recommendations
    
    ### Actionable Features
    
    We focus on features that are realistically changeable:
    - ✅ **Modifiable:** Parental approval, Spouse income/work, Education level
    - ✅ **Achievable:** Building financial stability, household harmony
    - ❌ **Not Modified:** Age, Gender, Religion, Caste (for ethical reasons)
    """)

# Implementation Tips
with st.expander("💡 Implementation Tips"):
    st.markdown("""
    ### How to Use These Recommendations
    
    1. **Prioritize:** Start with the #1 recommendation (highest improvement %)
    2. **Plan:** Consider which changes are realistic for your situation
    3. **Act:** Implement changes gradually and monitor outcomes
    4. **Reassess:** After changes, re-run predictions to see updated probabilities
    
    ### Common Actionable Recommendations
    
    | Recommendation | How to Achieve | Timeline |
    |---|---|---|
    | Increase Parental Approval | Family counseling, open communication | 3-6 months |
    | Improve Income Level | Career advancement, additional income streams | 1-2 years |
    | Increase Education Level | Formal education, certifications | 1-4 years |
    | Both Spouses Working | Job search, skill development | 0-6 months |
    | Better Caste/Religion Match | Pre-marriage counseling, acceptance building | Ongoing |
    
    ### What These Changes Don't Guarantee
    
    - Counterfactuals show statistical likelihood, not certainty
    - Real relationships involve emotional, social, and personal factors
    - Professional relationship counseling is always recommended
    - Success requires mutual effort and commitment from both partners
    """)

# Information section
with st.expander("ℹ️ About This Module"):
    st.markdown("""
    ### Counterfactual ML Technique
    
    **What is it?**
    - Generates hypothetical "what-if" scenarios
    - Shows minimal changes needed to flip predictions
    - Reveals actionable insights from ML models
    
    **Why use it?**
    - More actionable than feature importance alone
    - Shows concrete paths to improvement
    - Helps users understand model behavior
    
    **Limitations:**
    - Based on historical data patterns
    - Cannot account for unmeasured factors
    - Statistical correlation ≠ causation
    - Real-world changes may have different effects
    
    ### Model Details
    
    - **Base Model:** XGBoost Divorce Predictor
    - **Recommendation Method:** Iterative feature modification + re-prediction
    - **Features Considered:** 17 input features across demographics and relationships
    - **Output Format:** Top 3 suggestions with before/after probabilities
    """)

# Footer
st.markdown("""
---
**Remember:** These are statistical predictions based on patterns in data. Real relationships are complex and 
require genuine effort, communication, and often professional guidance. Use these insights as one input among many 
in your decision-making.
""")
