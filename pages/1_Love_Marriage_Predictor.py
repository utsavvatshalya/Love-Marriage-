"""
Module 1: Love Marriage Predictor
Predicts whether a marriage is based on Love or Arranged using ML classification.
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
    build_input_form_fields, create_input_dataframe,
    format_probability, get_confidence_label, preprocess_input
)
from src.explainer import (
    create_shap_explainer, plot_shap_waterfall, plot_shap_bar_top_features
)

st.set_page_config(
    page_title="Love Marriage Predictor — LoveMatch AI",
    page_icon="💕",
    layout="wide"
)

inject_theme()

page_header(
    "💕",
    "Love Marriage Predictor",
    "Tell us about your relationship and we'll reveal whether your match reads as a love story — or an arrangement — along with the key forces shaping that outcome."
)

# ── Load models ─────────────────────────────────────────────────────────────
try:
    model         = safe_model_load('love_marriage_model.pkl', 'Love Marriage Model')
    preprocessor  = safe_preprocessor_load('love_preprocessor.pkl', 'Love Marriage Preprocessor')
    feature_names = safe_feature_load('love_feature_names.pkl', 'Feature Names')
    feature_cols  = safe_feature_load('love_feature_cols.pkl', 'Feature Columns')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Place all `.pkl` files inside the `models/` folder and reload.")
    st.stop()

# ── Layout ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.1, 1], gap="large")

# ── LEFT: Input Form ─────────────────────────────────────────────────────────
with col1:
    st.markdown('<div class="lm-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Your Profile")

    with st.form("love_marriage_form"):
        user_input = build_input_form_fields(feature_cols)
        submit_button = st.form_submit_button(
            "✨ Reveal My Marriage Type",
            use_container_width=True,
            type="primary"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Results ────────────────────────────────────────────────────────────
with col2:
    st.markdown("### 🔮 Prediction")

    if submit_button:
        try:
            input_df    = create_input_dataframe(user_input, feature_cols)
            X_processed = preprocessor.transform(input_df)
            proba       = model.predict_proba(X_processed)
            love_prob   = proba[0][1]
            arr_prob    = proba[0][0]

            is_love = love_prob > 0.5
            label   = "💕 Love Marriage" if is_love else "👨‍👩‍👧‍👦 Arranged Marriage"
            conf    = get_confidence_label(max(love_prob, arr_prob))

            # Hero result card
            st.markdown(f"""
            <div class="lm-card-rose petal-bg" style="text-align:center; padding:36px 28px;">
              <div style="font-size:0.78em; text-transform:uppercase; letter-spacing:1.4px; opacity:0.85; margin-bottom:6px;">Predicted Classification</div>
              <div style="font-family:'Cormorant Garamond',serif; font-size:2.2em; font-weight:700; margin:10px 0 14px;">{label}</div>
              <span class="lm-badge lm-badge-rose">{conf}</span>
            </div>
            """, unsafe_allow_html=True)

            # Probability pills
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            with m1:
                st.metric("💕 Love Marriage", format_probability(love_prob),
                          delta=f"{(love_prob-0.5)*100:.1f}%" if love_prob > 0.5 else None)
            with m2:
                st.metric("👨‍👩‍👧‍👦 Arranged Marriage", format_probability(arr_prob),
                          delta=f"{(arr_prob-0.5)*100:.1f}%" if arr_prob > 0.5 else None)

            # Gauge chart — rose/wine palette
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(love_prob * 100, 1),
                number={'suffix': '%', 'font': {'family': 'Cormorant Garamond', 'size': 42, 'color': '#7B2D42'}},
                title={'text': "Love Marriage Score", 'font': {'family': 'DM Sans', 'size': 14, 'color': '#888'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#ccc', 'tickfont': {'size': 11}},
                    'bar': {'color': "#C9446A", 'thickness': 0.28},
                    'bgcolor': '#FDF6F0',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 30],  'color': '#F7EFF4'},
                        {'range': [30, 60], 'color': '#F2B5C8'},
                        {'range': [60, 100],'color': '#e8849e'},
                    ],
                    'threshold': {
                        'line': {'color': '#7B2D42', 'width': 3},
                        'thickness': 0.8,
                        'value': love_prob * 100
                    }
                }
            ))
            fig_gauge.update_layout(
                height=240,
                margin=dict(t=40, b=10, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.session_state.love_prediction = {
                'proba': proba, 'X_processed': X_processed,
                'love_prob': love_prob, 'user_input': user_input
            }

        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")

ornamental_divider()

# ── SHAP Section ──────────────────────────────────────────────────────────────
st.markdown("### 🔍 What's Driving This Prediction?")

if 'love_prediction' in st.session_state:
    try:
        X_processed = st.session_state.love_prediction['X_processed']
        explainer   = create_shap_explainer(model, X_processed)

        tab1, tab2 = st.tabs(["📊 Waterfall Breakdown", "📈 Top Features"])

        with tab1:
            st.caption("Each bar shows how a feature pushes the prediction toward Love (rose) or Arranged (muted).")
            fig_wf = plot_shap_waterfall(explainer, X_processed, feature_names, expected_value_idx=1)
            st.plotly_chart(fig_wf, use_container_width=True)

        with tab2:
            st.caption("The 10 features with the biggest absolute influence on this prediction.")
            fig_bar = plot_shap_bar_top_features(explainer, X_processed, feature_names, top_n=10)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Top-3 insight cards
        st.markdown("#### 💡 Three Most Influential Factors")
        shap_values = explainer.shap_values(X_processed)
        shap_vals   = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]
        top_idx     = np.argsort(np.abs(shap_vals))[-3:][::-1]

        c1, c2, c3 = st.columns(3)
        for i, (col, idx) in enumerate(zip([c1, c2, c3], top_idx)):
            fname  = feature_names[idx]
            sval   = shap_vals[idx]
            toward = "Love Marriage" if sval > 0 else "Arranged Marriage"
            color  = "#C9446A" if sval > 0 else "#6B8F71"
            with col:
                st.markdown(f"""
                <div class="lm-card" style="text-align:center; padding:20px 16px;">
                  <div style="font-size:0.7em; text-transform:uppercase; letter-spacing:1px; color:#aaa; margin-bottom:6px;">Factor #{i+1}</div>
                  <div style="font-weight:600; font-size:0.95em; color:#2E2E2E; margin-bottom:8px;">{fname}</div>
                  <div style="font-family:'Cormorant Garamond',serif; font-size:1.5em; font-weight:700; color:{color};">{abs(sval):.3f}</div>
                  <div style="font-size:0.78em; color:{color}; margin-top:4px;">→ {toward}</div>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"⚠️ SHAP explanations unavailable: {str(e)}")
else:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:40px; color:#aaa;">
      <div style="font-size:2em; margin-bottom:10px;">📊</div>
      <div>Fill in your profile and hit <strong>Reveal</strong> to see what's shaping the prediction.</div>
    </div>
    """, unsafe_allow_html=True)

ornamental_divider()

with st.expander("ℹ️ How this module works"):
    st.markdown("""
    **Model:** XGBoost Binary Classifier trained on 10,000 Indian marriage records.

    **Features used:** 14 demographic and relationship factors — age, education, income, caste, religion, parental approval, location, dowry, children, spousal working status, inter-caste and inter-religion openness.

    **Explainability:** SHAP TreeExplainer quantifies each feature's contribution to the final probability. Waterfall charts show cumulative impact; bar charts rank by absolute influence.

    **Note:** Predictions are probabilistic, not deterministic. Treat them as one lens among many.
    """)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#bbb; font-size:0.8em;">LoveMatch AI · For educational purposes only · Not a substitute for personal guidance</div>', unsafe_allow_html=True)
