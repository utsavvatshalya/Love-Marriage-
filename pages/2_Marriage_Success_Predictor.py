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
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider
from src.preprocess import (
    safe_model_load, safe_preprocessor_load, safe_feature_load,
    build_input_form_fields, create_input_dataframe,
    format_probability, get_confidence_label
)
from src.explainer import (
    create_shap_explainer, plot_shap_bar_top_features,
    create_success_gauge, plot_satisfaction_distribution
)

def safe_label_encoder_load(encoder_name, display_name=None):
    from src.preprocess import load_label_encoder
    try:
        return load_label_encoder(encoder_name)
    except FileNotFoundError:
        st.error(f"❌ {display_name or encoder_name} not found!")
        st.stop()

st.set_page_config(
    page_title="Marriage Success Predictor — LoveMatch AI",
    page_icon="✨",
    layout="wide"
)

inject_theme()

page_header(
    "✨",
    "Marriage Success Predictor",
    "Understand the health of your union — get a clear read on divorce risk, predicted satisfaction, and the factors that matter most to lasting happiness."
)

# ── Load models ──────────────────────────────────────────────────────────────
try:
    divorce_model        = safe_model_load('divorce_model.pkl', 'Divorce Prediction Model')
    divorce_preprocessor = safe_preprocessor_load('divorce_preprocessor.pkl', 'Divorce Preprocessor')
    divorce_feature_names= safe_feature_load('divorce_feature_names.pkl', 'Divorce Feature Names')
    divorce_feature_cols = safe_feature_load('divorce_feature_cols.pkl', 'Divorce Feature Columns')
    satisfaction_model   = safe_model_load('satisfaction_model.pkl', 'Satisfaction Model')
    sat_preprocessor     = safe_preprocessor_load('sat_preprocessor.pkl', 'Satisfaction Preprocessor')
    sat_feature_names    = safe_feature_load('sat_feature_names.pkl', 'Satisfaction Feature Names')
    sat_feature_cols     = safe_feature_load('sat_feature_cols.pkl', 'Satisfaction Feature Columns')
    sat_label_encoder    = safe_label_encoder_load('sat_label_encoder.pkl', 'Satisfaction Label Encoder')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.info("Place all `.pkl` files inside the `models/` folder and reload.")
    st.stop()

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.1, 1], gap="large")

# ── LEFT: Input Form ──────────────────────────────────────────────────────────
with col1:
    st.markdown('<div class="lm-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Your Profile")
    with st.form("success_predictor_form"):
        user_input = build_input_form_fields(sat_feature_cols)
        submit_button = st.form_submit_button(
            "💍 Predict Marriage Success",
            use_container_width=True,
            type="primary"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Results ────────────────────────────────────────────────────────────
with col2:
    st.markdown("### 📊 Analysis")

    if submit_button:
        try:
            if any(v is None for v in user_input.values()):
                st.error("⚠️ Please fill in all fields!")
                st.stop()

            input_divorce = create_input_dataframe(user_input, divorce_feature_cols)
            input_sat     = create_input_dataframe(user_input, sat_feature_cols)
            X_divorce     = divorce_preprocessor.transform(input_divorce)
            X_satisfaction= sat_preprocessor.transform(input_sat)

            divorce_proba     = divorce_model.predict_proba(X_divorce)
            divorce_prob      = divorce_proba[0][1]
            success_prob      = 1 - divorce_prob

            satisfaction_proba= satisfaction_model.predict_proba(X_satisfaction)
            satisfaction_pred = satisfaction_model.predict(X_satisfaction)[0]
            satisfaction_label= sat_label_encoder.inverse_transform([satisfaction_pred])[0]

            # ── Three metric cards ────────────────────────────────────────
            sat_colors = {'Low': 'lm-card-rose', 'Medium': 'lm-card-gold', 'High': 'lm-card-sage'}
            sat_icons  = {'Low': '😔', 'Medium': '😊', 'High': '🥰'}
            sat_cls    = sat_colors.get(satisfaction_label, 'lm-card-rose')
            sat_icon   = sat_icons.get(satisfaction_label, '💍')

            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="lm-card-sage" style="text-align:center; padding:24px 16px;">
                  <div class="lm-metric-label">Success Probability</div>
                  <div class="lm-metric-val">{format_probability(success_prob)}</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="lm-card-rose" style="text-align:center; padding:24px 16px;">
                  <div class="lm-metric-label">Divorce Risk</div>
                  <div class="lm-metric-val">{format_probability(divorce_prob)}</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="{sat_cls}" style="text-align:center; padding:24px 16px;">
                  <div class="lm-metric-label">Predicted Satisfaction</div>
                  <div class="lm-metric-val">{sat_icon}</div>
                  <div style="font-family:'DM Sans',sans-serif; font-weight:600; font-size:1.05em;">{satisfaction_label}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            # ── Gauge chart ───────────────────────────────────────────────
            fig_gauge = create_success_gauge(success_prob, divorce_prob)
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=250,
                margin=dict(t=40, b=10, l=20, r=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # ── Satisfaction bar ──────────────────────────────────────────
            fig_sat = plot_satisfaction_distribution(satisfaction_model, satisfaction_proba, sat_label_encoder)
            fig_sat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=220
            )
            st.plotly_chart(fig_sat, use_container_width=True)

            # ── Quick insight pills ───────────────────────────────────────
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if success_prob >= 0.8:
                st.success("✅ Strong foundation — your profile shows a high likelihood of lasting together.")
            elif success_prob >= 0.6:
                st.info("⚠️ Moderate outlook — a few key factors could make a real difference.")
            else:
                st.error("❌ Elevated risk — consider the suggestions in *Improve My Chances*.")

            if satisfaction_label == "High":
                st.success("🥰 High satisfaction predicted — the signs point to a fulfilling marriage.")
            elif satisfaction_label == "Medium":
                st.info("😊 Moderate satisfaction — there's clear room to grow together.")
            else:
                st.warning("😔 Low satisfaction signals — worth exploring what drives this.")

            # Store for SHAP section
            st.session_state.success_prediction = {
                'divorce_proba': divorce_proba, 'X_divorce': X_divorce,
                'success_prob': success_prob, 'divorce_prob': divorce_prob,
                'satisfaction_pred': satisfaction_pred,
                'satisfaction_label': satisfaction_label,
                'satisfaction_proba': satisfaction_proba,
                'user_input': user_input
            }

        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")

ornamental_divider()

# ── SHAP Section ──────────────────────────────────────────────────────────────
st.markdown("### 🔍 Risk Factors & Feature Importance")

if 'success_prediction' in st.session_state:
    try:
        X_divorce  = st.session_state.success_prediction['X_divorce']
        explainer  = create_shap_explainer(divorce_model, X_divorce)

        tab1, tab2, tab3 = st.tabs([
            "💚 Success Drivers", "⚠️ Risk Factors", "📈 Satisfaction Breakdown"
        ])

        with tab1:
            st.caption("Features with the strongest positive influence on a lasting marriage.")
            fig_success = plot_shap_bar_top_features(explainer, X_divorce, divorce_feature_names, top_n=10)
            fig_success.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_success, use_container_width=True)

        with tab2:
            st.caption("Features most strongly associated with elevated divorce risk in your profile.")
            shap_values = explainer.shap_values(X_divorce)
            shap_vals   = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

            risk_df = pd.DataFrame({
                'Feature': divorce_feature_names,
                'Risk Impact': np.abs(shap_vals)
            }).sort_values('Risk Impact', ascending=True).tail(10)

            fig_risk = px.bar(
                risk_df, x='Risk Impact', y='Feature', orientation='h',
                labels={'Risk Impact': 'Impact Magnitude'},
                color='Risk Impact',
                color_continuous_scale=[[0, '#F2B5C8'], [1, '#7B2D42']]
            )
            fig_risk.update_layout(
                height=360, showlegend=False, template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False,
                font=dict(family='DM Sans')
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        with tab3:
            st.caption("Probability of each satisfaction level given your profile.")
            satisfaction_data = pd.DataFrame({
                'Satisfaction Level': sat_label_encoder.classes_,
                'Probability': st.session_state.success_prediction['satisfaction_proba'][0]
            })
            fig_sat = px.bar(
                satisfaction_data, x='Satisfaction Level', y='Probability',
                color='Satisfaction Level',
                color_discrete_map={'Low': '#C9446A', 'Medium': '#E8972A', 'High': '#6B8F71'}
            )
            fig_sat.update_layout(
                height=280, showlegend=False, template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='DM Sans')
            )
            st.plotly_chart(fig_sat, use_container_width=True)

    except Exception as e:
        st.warning(f"⚠️ Could not generate detailed analysis: {str(e)}")

else:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:44px; color:#aaa;">
      <div style="font-size:2em; margin-bottom:10px;">🔍</div>
      <div>Fill in your profile and click <strong>Predict Marriage Success</strong> to see the full risk analysis.</div>
    </div>
    """, unsafe_allow_html=True)

ornamental_divider()

with st.expander("📚 Understanding the Results"):
    st.markdown("""
    **Success Probability** — the model's estimate that this marriage will not end in divorce, based on your inputs.

    **Divorce Risk** — the inverse: how strongly the profile aligns with patterns seen in divorces in the training data.

    **Marital Satisfaction** — a separate multiclass prediction (Low / Medium / High) trained independently to avoid leakage.

    **SHAP values** show direction and magnitude — warm colours push toward risk, cool colours toward stability. Longer bars mean stronger influence.

    Focus your attention on *modifiable* features (income, parental approval, spousal work status). Features like caste or religion are descriptive, not prescriptive.
    """)

with st.expander("ℹ️ Model architecture"):
    st.markdown("""
    - **Divorce model:** XGBoost Binary Classifier · Target: `Divorce_Status` (No = success)
    - **Satisfaction model:** XGBoost Multiclass · Target: `Marital_Satisfaction` (Low / Medium / High)
    - **Explainability:** SHAP TreeExplainer on the divorce model
    - **Imbalance handling:** SMOTE oversampling during training (~10% divorce rate in data)
    """)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#bbb; font-size:0.8em;">LoveMatch AI · For educational purposes only · Not a substitute for professional counselling</div>', unsafe_allow_html=True)
