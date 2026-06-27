"""
LoveMatch AI — Home Page
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.theme import inject_theme, ornamental_divider

st.set_page_config(
    page_title="LoveMatch AI — Indian Marriage Outcome Predictor",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()

# ── Hero — all text explicitly white via inline styles ────────────────────────
st.markdown("""
<div style="
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%);
  border-radius: 20px;
  text-align: center;
  padding: 64px 40px 56px;
  margin-bottom: 8px;
  box-shadow: 0 8px 28px rgba(201,68,106,0.28);
  position: relative;
  overflow: hidden;
">
  <div style="position:absolute; font-size:200px; opacity:0.05; top:-40px; right:-20px; line-height:1;">💍</div>

  <div style="font-size: 3em; margin-bottom: 12px; color: white;">💍</div>

  <div style="
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.4em;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 16px;
    color: white;
  ">LoveMatch AI</div>

  <div style="
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1em;
    color: rgba(255,255,255,0.90);
    max-width: 560px;
    margin: 0 auto 28px;
    line-height: 1.7;
  ">
    Machine learning meets matrimony. Predict marriage outcomes,
    understand what drives them, and discover what changes would
    make the biggest difference.
  </div>

  <div style="
    display: flex;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82em;
    color: rgba(255,255,255,0.80);
    text-transform: uppercase;
    letter-spacing: 1.2px;
  ">
    <span style="color:rgba(255,255,255,0.80);">📊 10,000 Records</span>
    <span style="color:rgba(255,255,255,0.80);">🤖 XGBoost Models</span>
    <span style="color:rgba(255,255,255,0.80);">🔍 SHAP Explainability</span>
    <span style="color:rgba(255,255,255,0.80);">🎯 Counterfactual AI</span>
  </div>
</div>
""", unsafe_allow_html=True)

ornamental_divider()

# ── Module cards ──────────────────────────────────────────────────────────────
st.markdown("""
<h2 style="text-align:center; font-family:'Cormorant Garamond',serif;
           color:#7B2D42; font-size:2em; margin-bottom:6px;">
  Three Modules. One Story.
</h2>
<p style="text-align:center; color:#999; font-size:0.95em; margin-bottom:28px;
          font-family:'DM Sans',sans-serif;">
  Each module tackles a different question about your marriage profile.
</p>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:32px 24px;">
      <div style="font-size:2.4em; margin-bottom:12px;">💕</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:1.5em;
                  font-weight:700; color:#7B2D42; margin-bottom:8px;">Love or Arranged?</div>
      <div style="font-size:0.88em; color:#666; line-height:1.7; margin-bottom:20px;
                  font-family:'DM Sans',sans-serif;">
        Enter your profile and find out whether your relationship reads more like a love story
        or an arranged match — with SHAP showing exactly why.
      </div>
      <span class="lm-badge lm-badge-red">Module 1</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Love_Marriage_Predictor.py", label="→ Open Love Predictor", use_container_width=True)

with c2:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:32px 24px;">
      <div style="font-size:2.4em; margin-bottom:12px;">✨</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:1.5em;
                  font-weight:700; color:#7B2D42; margin-bottom:8px;">Will It Last?</div>
      <div style="font-size:0.88em; color:#666; line-height:1.7; margin-bottom:20px;
                  font-family:'DM Sans',sans-serif;">
        Get a clear read on divorce risk, predicted marital satisfaction, and the factors
        driving both — visualised with feature importance charts.
      </div>
      <span class="lm-badge lm-badge-red">Module 2</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Marriage_Success_Predictor.py", label="→ Open Success Predictor", use_container_width=True)

with c3:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:32px 24px;">
      <div style="font-size:2.4em; margin-bottom:12px;">🎯</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:1.5em;
                  font-weight:700; color:#7B2D42; margin-bottom:8px;">What Can Change?</div>
      <div style="font-size:0.88em; color:#666; line-height:1.7; margin-bottom:20px;
                  font-family:'DM Sans',sans-serif;">
        Counterfactual AI shows you which specific changes — parental approval, income,
        education — would lift your success probability, and by exactly how much.
      </div>
      <span class="lm-badge lm-badge-red">Module 3</span>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Improve_My_Chances.py", label="→ Open Improvement Engine", use_container_width=True)

ornamental_divider()

# ── Compatibility flow ────────────────────────────────────────────────────────
st.markdown("""
<h2 style="text-align:center; font-family:'Cormorant Garamond',serif;
           color:#7B2D42; font-size:2em; margin-bottom:6px;">
  Or Try the Couple's Flow 💑
</h2>
<p style="text-align:center; color:#999; font-size:0.95em; margin-bottom:28px;
          font-family:'DM Sans',sans-serif;">
  Both partners fill in their profiles — and we give you a detailed compatibility breakdown.
</p>
""", unsafe_allow_html=True)

fl1, fl2, fl3 = st.columns(3, gap="medium")

with fl1:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:24px 20px;">
      <div style="font-size:2em; margin-bottom:8px;">👨</div>
      <div style="font-family:'Cormorant Garamond',serif; font-weight:700;
                  color:#7B2D42; font-size:1.2em; margin-bottom:6px;">His Profile</div>
      <div style="font-size:0.84em; color:#888; font-family:'DM Sans',sans-serif;">
        Age, education, income, values & preferences
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Boy_Profile.py", label="→ Start Here", use_container_width=True)

with fl2:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:24px 20px;">
      <div style="font-size:2em; margin-bottom:8px;">👩</div>
      <div style="font-family:'Cormorant Garamond',serif; font-weight:700;
                  color:#7B2D42; font-size:1.2em; margin-bottom:6px;">Her Profile</div>
      <div style="font-size:0.84em; color:#888; font-family:'DM Sans',sans-serif;">
        Same details from her perspective
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Girl_Profile.py", label="→ Step 2", use_container_width=True)

with fl3:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:24px 20px;">
      <div style="font-size:2em; margin-bottom:8px;">💫</div>
      <div style="font-family:'Cormorant Garamond',serif; font-weight:700;
                  color:#7B2D42; font-size:1.2em; margin-bottom:6px;">Your Score</div>
      <div style="font-size:0.84em; color:#888; font-family:'DM Sans',sans-serif;">
        Compatibility score + radar chart + recommendation
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Compatibility_Analysis.py", label="→ See Results", use_container_width=True)

ornamental_divider()

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<h2 style="text-align:center; font-family:'Cormorant Garamond',serif;
           color:#7B2D42; font-size:2em; margin-bottom:28px;">
  How It Works
</h2>
""", unsafe_allow_html=True)

h1, h2, h3, h4 = st.columns(4, gap="medium")
steps = [
    ("1", "Fill Your Profile", "Answer questions about demographics, family background, and relationship preferences."),
    ("2", "ML Model Predicts", "XGBoost classifiers trained on 10,000 real Indian marriage records process your inputs."),
    ("3", "SHAP Explains Why", "See exactly which features pushed the prediction in each direction, and how strongly."),
    ("4", "Act on Insights", "Counterfactual suggestions show the specific changes with the highest improvement potential."),
]
for col, (num, title, desc) in zip([h1, h2, h3, h4], steps):
    with col:
        st.markdown(f"""
        <div class="lm-card" style="text-align:center; padding:24px 18px;">
          <div style="width:40px; height:40px; border-radius:50%;
                      background:linear-gradient(135deg,#C9446A,#7B2D42);
                      color:white; font-weight:700; font-size:1.1em;
                      display:flex; align-items:center; justify-content:center;
                      margin:0 auto 12px; font-family:'DM Sans',sans-serif;">{num}</div>
          <div style="font-weight:600; color:#2E2E2E; margin-bottom:8px; font-size:0.95em;
                      font-family:'DM Sans',sans-serif;">{title}</div>
          <div style="font-size:0.82em; color:#888; line-height:1.6;
                      font-family:'DM Sans',sans-serif;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

ornamental_divider()

st.markdown("""
<div style="text-align:center; color:#bbb; font-size:0.82em; line-height:2; padding-bottom:12px;
            font-family:'DM Sans',sans-serif;">
  <strong style="color:#C9446A; font-family:'Cormorant Garamond',serif; font-size:1.15em;">
    LoveMatch AI
  </strong><br>
  Built with Python · XGBoost · SHAP · Streamlit &nbsp;·&nbsp; For educational purposes only<br>
  <em>Real relationships are built on communication, trust, and genuine effort — not just algorithms.</em>
</div>
""", unsafe_allow_html=True)
