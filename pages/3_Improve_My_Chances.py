"""
Module 3: Improve My Chances
Generates personalised counterfactual recommendations to improve marriage outcomes.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider
from src.preprocess import (
    safe_model_load, safe_preprocessor_load, safe_feature_load,
    build_input_form_fields, create_input_dataframe, format_probability
)
from src.explainer import (
    CounterfactualExplainer, display_counterfactual_suggestions, create_comparison_dataframe
)

st.set_page_config(
    page_title="Improve My Chances — LoveMatch AI",
    page_icon="🎯",
    layout="wide"
)

inject_theme()

page_header(
    "🎯",
    "Improve My Chances",
    "See exactly which changes would move the needle on your success probability — ranked by impact so you know where to focus first."
)

# ── Load models ──────────────────────────────────────────────────────────────
try:
    divorce_model         = safe_model_load('divorce_model.pkl', 'Divorce Model')
    divorce_preprocessor  = safe_preprocessor_load('divorce_preprocessor.pkl', 'Divorce Preprocessor')
    divorce_feature_names = safe_feature_load('divorce_feature_names.pkl', 'Divorce Feature Names')
    divorce_feature_cols  = safe_feature_load('divorce_feature_cols.pkl', 'Divorce Feature Columns')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Place all `.pkl` files inside the `models/` folder and reload.")
    st.stop()

# ── Counterfactual explainer ──────────────────────────────────────────────────
continuous_features  = ['Age_at_Marriage', 'Children_Count', 'Years_Since_Marriage']
categorical_features = [c for c in divorce_feature_cols if c not in continuous_features]

counterfactual = CounterfactualExplainer(
    model=divorce_model,
    feature_names=divorce_feature_names,
    feature_cols=divorce_feature_cols,
    continuous_features=continuous_features,
    categorical_features=categorical_features
)

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.1, 1], gap="large")

# ── LEFT: Form ────────────────────────────────────────────────────────────────
with col1:
    st.markdown('<div class="lm-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Your Current Profile")
    with st.form("improve_chances_form"):
        user_input = build_input_form_fields(divorce_feature_cols)
        submit_button = st.form_submit_button(
            "🔍 Generate Recommendations",
            use_container_width=True,
            type="primary"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Recommendations ────────────────────────────────────────────────────
with col2:
    st.markdown("### 💡 Personalised Recommendations")

    if submit_button:
        try:
            if not all(user_input.values()):
                st.error("⚠️ Please fill in all fields!")
                st.stop()

            input_df       = create_input_dataframe(user_input, divorce_feature_cols)
            X_current      = divorce_preprocessor.transform(input_df)
            current_proba  = divorce_model.predict_proba(X_current)
            current_success= 1 - current_proba[0][1]

            # ── Current status card ───────────────────────────────────────
            status_cls  = "lm-card-sage" if current_success >= 0.8 else \
                          "lm-card-gold" if current_success >= 0.6 else "lm-card-rose"
            status_text = "Strong position 💚" if current_success >= 0.8 else \
                          "Room to grow 🟡" if current_success >= 0.6 else "Needs attention 🔴"

            st.markdown(f"""
            <div class="{status_cls} petal-bg" style="text-align:center; padding:28px 20px; margin-bottom:20px;">
              <div class="lm-metric-label">Current Success Probability</div>
              <div class="lm-metric-val">{format_probability(current_success)}</div>
              <span class="lm-badge lm-badge-rose">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Generate suggestions ──────────────────────────────────────
            suggestions = counterfactual.generate_counterfactuals_simple(
                current_success, user_input, divorce_preprocessor
            )

            if suggestions:
                suggestions = sorted(suggestions, key=lambda x: x['improvement'], reverse=True)

                impact_map = {
                    'high':   ('lm-suggestion high',   '🔥', '#6B8F71'),
                    'medium': ('lm-suggestion medium',  '⬆️', '#E8972A'),
                    'low':    ('lm-suggestion low',     '📈', '#C9446A'),
                }

                for i, sug in enumerate(suggestions, 1):
                    imp    = sug['improvement']
                    tier   = 'high' if imp >= 10 else 'medium' if imp >= 5 else 'low'
                    cls, icon, color = impact_map[tier]

                    st.markdown(f"""
                    <div class="{cls}">
                      <div style="font-size:0.72em; text-transform:uppercase; letter-spacing:1px; color:#aaa; margin-bottom:4px;">Recommendation #{i}</div>
                      <div style="font-weight:600; font-size:1em; color:#2E2E2E; margin-bottom:12px;">{icon} {sug['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="lm-before-after">
                      <div>
                        <div class="lbl">Current</div>
                        <div class="val">{format_probability(sug['old_value'])}</div>
                      </div>
                      <div class="arrow">→</div>
                      <div>
                        <div class="lbl">Projected</div>
                        <div class="val" style="color:{color};">{format_probability(sug['new_value'])}</div>
                      </div>
                    </div>
                    <div style="text-align:center; margin-bottom:20px;">
                      <span style="background:{color}; color:white; padding:7px 20px; border-radius:20px;
                                   font-size:0.82em; font-weight:600; font-family:'DM Sans',sans-serif;">
                        +{imp:.1f}% improvement
                      </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Your profile is already well-positioned. No urgent changes needed!")

            st.session_state.improvement_data = {
                'current_success': current_success,
                'suggestions': suggestions,
                'user_input': user_input
            }

        except Exception as e:
            st.error(f"❌ Failed to generate recommendations: {str(e)}")

ornamental_divider()

# ── Comparison Table ──────────────────────────────────────────────────────────
if 'improvement_data' in st.session_state:
    st.markdown("### 📋 Full Comparison Table")

    suggestions     = st.session_state.improvement_data['suggestions']
    current_success = st.session_state.improvement_data['current_success']

    if suggestions:
        rows = [{'Scenario': '📍 Current Status',
                 'Success Probability': format_probability(current_success),
                 'Divorce Risk': format_probability(1 - current_success),
                 'Change': '—'}]

        for i, sug in enumerate(suggestions, 1):
            rows.append({
                'Scenario': f"#{i}: {sug['description']}",
                'Success Probability': format_probability(sug['new_value']),
                'Divorce Risk': format_probability(1 - sug['new_value']),
                'Change': f"+{sug['improvement']:.1f}%"
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Recommendations as CSV",
            data=csv,
            file_name="lovematch_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

    ornamental_divider()

with st.expander("🔬 How counterfactuals work"):
    st.markdown("""
    A **counterfactual** answers: *"What's the minimum I'd need to change to get a better outcome?"*

    For each actionable feature (parental approval, income, education, spousal working status), we:
    1. Swap the value to the next best option
    2. Re-run the preprocessor and model
    3. Record the probability change
    4. Rank by improvement and return the top suggestions

    Features like age, caste, and religion are intentionally excluded — they're either fixed or ethically off-limits to "optimise."
    """)

with st.expander("💡 How to act on these recommendations"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        | Recommendation | Realistic Path | Timeline |
        |---|---|---|
        | Parental approval | Open conversation, family counselling | 3–6 months |
        | Income level | Career growth, side income | 1–2 years |
        | Education level | Certifications, part-time degrees | 1–4 years |
        """)
    with col2:
        st.markdown("""
        **Remember:**
        - Start with the #1 recommendation (highest impact)
        - These are statistical signals — not guarantees
        - Real relationships need genuine effort on both sides
        - A counsellor can help with the human side of things
        """)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#bbb; font-size:0.8em;">LoveMatch AI · Statistical predictions only · Please seek professional guidance for major life decisions</div>', unsafe_allow_html=True)
