"""
About LoveMatch AI — project info, dataset, models, tech stack.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider

st.set_page_config(
    page_title="About — LoveMatch AI",
    page_icon="ℹ️",
    layout="wide"
)

inject_theme()

page_header(
    "ℹ️",
    "About LoveMatch AI",
    "An end-to-end machine learning project — from raw marriage data to explainable, actionable predictions."
)

ornamental_divider()

# ── Overview ──────────────────────────────────────────────────────────────────
st.markdown("### 🎯 What This Project Does")
st.markdown("""
**LoveMatch AI** uses XGBoost models trained on 10,000 Indian marriage records to deliver three things:

1. **Marriage Type Classification** — is this profile more consistent with a love or arranged marriage?
2. **Success Analysis** — what's the divorce risk and predicted satisfaction level?
3. **Counterfactual Recommendations** — exactly which changes would improve the outcome, and by how much?

Every prediction comes with SHAP-powered explanations so you can see *why* the model decided what it did.
""")

ornamental_divider()

# ── Dataset stats ─────────────────────────────────────────────────────────────
st.markdown("### 📊 Dataset at a Glance")

c1, c2, c3, c4 = st.columns(4)
for col, val, label in zip(
    [c1, c2, c3, c4],
    ["10,000", "17", "3", "India"],
    ["Records", "Input Features", "Target Variables", "Focus Region"]
):
    col.metric(label, val)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Feature categories**")
    st.markdown("""
    - **Numeric:** Age at Marriage, Children Count, Years Since Marriage
    - **Ordinal:** Education Level, Income Level, Parental Approval
    - **Nominal:** Gender, Religion, Caste Match, Urban/Rural, Dowry, Spouse Working, Inter-Caste, Inter-Religion
    """)
with col_b:
    st.markdown("**Target variables**")
    targets = pd.DataFrame({
        'Module': ['Love Marriage Predictor', 'Success Predictor', 'Satisfaction Predictor'],
        'Target': ['Marriage_Type', 'Divorce_Status', 'Marital_Satisfaction'],
        'Type': ['Binary', 'Binary', 'Multiclass (3)']
    })
    st.dataframe(targets, hide_index=True, use_container_width=True)

ornamental_divider()

# ── Models ────────────────────────────────────────────────────────────────────
st.markdown("### 🤖 Model Architecture")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="lm-model-card" style="background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%);">
      <div style="font-size:1.3em; font-weight:700; margin-bottom:16px; font-family:'Cormorant Garamond',serif;">💕 Love Predictor</div>
      <div class="lm-model-row"><span class="k">Algorithm</span><span class="v">XGBoost</span></div>
      <div class="lm-model-row"><span class="k">Task</span><span class="v">Binary classification</span></div>
      <div class="lm-model-row"><span class="k">Explainer</span><span class="v">SHAP TreeExplainer</span></div>
      <div class="lm-model-row"><span class="k">Imbalance</span><span class="v">SMOTE</span></div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="lm-model-card" style="background: linear-gradient(135deg, #6B8F71 0%, #4e6e54 100%);">
      <div style="font-size:1.3em; font-weight:700; margin-bottom:16px; font-family:'Cormorant Garamond',serif;">✨ Success Predictor</div>
      <div class="lm-model-row"><span class="k">Algorithm</span><span class="v">XGBoost</span></div>
      <div class="lm-model-row"><span class="k">Task</span><span class="v">Binary classification</span></div>
      <div class="lm-model-row"><span class="k">Explainer</span><span class="v">SHAP TreeExplainer</span></div>
      <div class="lm-model-row"><span class="k">Imbalance</span><span class="v">SMOTE (~10% divorce rate)</span></div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="lm-model-card" style="background: linear-gradient(135deg, #E8972A 0%, #c67d1a 100%);">
      <div style="font-size:1.3em; font-weight:700; margin-bottom:16px; font-family:'Cormorant Garamond',serif;">🎯 Counterfactuals</div>
      <div class="lm-model-row"><span class="k">Approach</span><span class="v">Iterative search</span></div>
      <div class="lm-model-row"><span class="k">Base model</span><span class="v">Divorce predictor</span></div>
      <div class="lm-model-row"><span class="k">Output</span><span class="v">Top 3 suggestions</span></div>
      <div class="lm-model-row"><span class="k">Ranked by</span><span class="v">Improvement %</span></div>
    </div>
    """, unsafe_allow_html=True)

ornamental_divider()

# ── Tech stack ────────────────────────────────────────────────────────────────
st.markdown("### 🛠️ Technology Stack")

tech_groups = {
    "ML & AI": ["XGBoost", "Scikit-learn", "SHAP", "imbalanced-learn", "NumPy", "Pandas"],
    "Web & Visualisation": ["Streamlit", "Plotly", "Plotly Express"],
    "Infrastructure": ["Joblib", "Python 3.10+", "Streamlit Cloud"],
}

for group, techs in tech_groups.items():
    st.markdown(f"**{group}**")
    pills = "".join([f'<span class="lm-tech-pill">{t}</span>' for t in techs])
    st.markdown(f'<div style="margin-bottom:16px;">{pills}</div>', unsafe_allow_html=True)

ornamental_divider()

# ── Explainability ────────────────────────────────────────────────────────────
st.markdown("### 🔍 Explainability Methods")

e1, e2 = st.columns(2)
with e1:
    st.markdown("""
    <div class="lm-card">
      <div style="font-size:1.1em; font-weight:700; color:#C9446A; margin-bottom:10px;">SHAP</div>
      <p style="font-size:0.92em; color:#555; line-height:1.7;">
        SHapley Additive exPlanations assign each feature a contribution value for a specific prediction.
        We use <code>TreeExplainer</code> for fast, exact SHAP values on XGBoost models.
        Waterfall charts show per-prediction breakdowns; bar charts rank by mean absolute impact.
      </p>
    </div>
    """, unsafe_allow_html=True)

with e2:
    st.markdown("""
    <div class="lm-card">
      <div style="font-size:1.1em; font-weight:700; color:#C9446A; margin-bottom:10px;">Counterfactuals</div>
      <p style="font-size:0.92em; color:#555; line-height:1.7;">
        Inspired by DiCE, our approach iterates over actionable features, swaps each value to the
        next-best option, re-runs the preprocessor and model, and records the probability change.
        Features like age, caste, and religion are excluded for ethical reasons.
      </p>
    </div>
    """, unsafe_allow_html=True)

ornamental_divider()

# ── Disclaimers ───────────────────────────────────────────────────────────────
st.markdown("### ⚠️ Important Disclaimers")

st.warning("""
**This project is built for educational and portfolio purposes.**

- Predictions are probabilistic — not guarantees.
- The dataset reflects historical patterns, which may embed cultural biases.
- Correlation in the model ≠ causation in real relationships.
- Real marriages are shaped by communication, commitment, and countless unmeasured factors.
- **Do not use these predictions as a substitute for personal judgement or professional counselling.**
""")

ornamental_divider()

st.markdown("""
<div style="text-align:center; color:#bbb; font-size:0.85em; line-height:2;">
  <strong style="color:#C9446A; font-family:'Cormorant Garamond',serif; font-size:1.2em;">LoveMatch AI</strong><br>
  Built with Python · XGBoost · SHAP · Streamlit<br>
  Deployed on Streamlit Community Cloud · <em>Made with ❤️</em>
</div>
""", unsafe_allow_html=True)
