"""
Module: Compatibility Analysis
Compare both profiles and show compatibility score with visualisations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.theme import inject_theme, page_header, ornamental_divider

st.set_page_config(
    page_title="Compatibility Analysis — LoveMatch AI",
    page_icon="💫",
    layout="wide"
)

inject_theme()

page_header(
    "💫",
    "Compatibility Analysis",
    "Here's how you two align — across values, lifestyle, and life goals."
)

st.markdown('<div class="lm-step-badge">Step 3 of 3 — Your Results</div>', unsafe_allow_html=True)

# Guard
if 'boy_profile' not in st.session_state or 'girl_profile' not in st.session_state:
    st.markdown("""
    <div class="lm-card" style="text-align:center; padding:40px; color:#aaa;">
      <div style="font-size:2em; margin-bottom:10px;">⚠️</div>
      <div>Please complete both profiles before viewing the analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Boy's Profile", use_container_width=True):
            st.switch_page("pages/1_Boy_Profile.py")
    with c2:
        if st.button("← Girl's Profile", use_container_width=True):
            st.switch_page("pages/2_Girl_Profile.py")
    st.stop()

boy  = st.session_state['boy_profile']
girl = st.session_state['girl_profile']

# ── Compatibility calculation ─────────────────────────────────────────────────
def calculate_compatibility(boy, girl):
    matches = {
        'Education Match':    boy['Education_Level'] == girl['Education_Level'],
        'Income Level':       boy['Income_Level']    == girl['Income_Level'],
        'Caste Match':        boy['Caste_Match']     == girl['Caste_Match'],
        'Religion':           boy['Religion']         == girl['Religion'],
        'Parental Approval':  boy['Parental_Approval'] == 'Yes' and girl['Parental_Approval'] == 'Yes',
        'Location':           boy['Urban_Rural']      == girl['Urban_Rural'],
        'Marriage Type':      boy['Marriage_Type']    == girl['Marriage_Type'],
        'Inter-Caste Open':   boy['Inter-Caste']      == girl['Inter-Caste'] and boy['Inter-Caste'] == 'Yes',
        'Inter-Religion Open':boy['Inter-Religion']   == girl['Inter-Religion'] and boy['Inter-Religion'] == 'Yes',
        'Children Goals':     boy['Children_Count']   == girl['Children_Count'],
    }
    age_diff = abs(boy['Age_at_Marriage'] - girl['Age_at_Marriage'])
    matches['Age Compatibility'] = 2 <= age_diff <= 5
    score = sum(matches.values()) / len(matches) * 100
    return matches, score, age_diff

matches, score, age_diff = calculate_compatibility(boy, girl)

# ── Compatibility hero card ───────────────────────────────────────────────────
if score >= 75:
    tagline = "💚 Marriage-Ready — you align on what matters most."
elif score >= 50:
    tagline = "🟡 Good potential — worth exploring further together."
else:
    tagline = "🔴 Significant differences — approach thoughtfully."

st.markdown(f"""
<div class="lm-compatibility-hero petal-bg">
  <div style="font-size:0.8em; text-transform:uppercase; letter-spacing:1.4px; opacity:0.8;">Your Compatibility Score</div>
  <div class="score">{score:.0f}%</div>
  <div class="tagline">{tagline}</div>
</div>
""", unsafe_allow_html=True)

ornamental_divider()

# ── Recommendation ────────────────────────────────────────────────────────────
st.markdown("### 💌 What This Means for You")

if score >= 75:
    border = "#6B8F71"
    match_count = sum(matches.values())
    total_count = len(matches)
    rec_body = f"""
<p>You align strongly on <strong>{match_count} out of {total_count}</strong> key factors. The data suggests a solid foundation — shared values, compatible goals, and family support all point in the right direction.</p>
<p><strong>Good next steps:</strong></p>
<ul>
  <li>Have deeper conversations about long-term life goals</li>
  <li>Discuss family planning expectations openly</li>
  <li>Involve parents if you're both comfortable</li>
</ul>
"""
elif score >= 50:
    border = "#E8972A"
    match_count = sum(matches.values())
    total_count = len(matches)
    rec_body = f"""
<p>You share common ground on <strong>{match_count} out of {total_count}</strong> factors, with some meaningful differences. These aren't dealbreakers — but they're worth exploring before making a big commitment.</p>
<p><strong>Good next steps:</strong></p>
<ul>
  <li>Have honest conversations about the mismatches below</li>
  <li>Understand each other's non-negotiables</li>
  <li>Give yourselves time before deciding on marriage</li>
</ul>
"""
else:
    border = "#C9446A"
    match_count = sum(matches.values())
    total_count = len(matches)
    rec_body = f"""
<p>You match on only <strong>{match_count} out of {total_count}</strong> factors. Significant gaps exist in core areas. That doesn't mean it can't work — but it means both of you would need to consciously bridge those gaps.</p>
<p><strong>Good next steps:</strong></p>
<ul>
  <li>Identify which differences are truly dealbreakers</li>
  <li>Consider whether you're both flexible enough on key areas</li>
  <li>A relationship counsellor can help navigate this constructively</li>
</ul>
"""

st.markdown(f"""
<div class="lm-recommendation" style="border-left-color:{border};">
  {rec_body}
</div>
""", unsafe_allow_html=True)

ornamental_divider()

# ── Side-by-side profiles ─────────────────────────────────────────────────────
st.markdown("### 👥 Profile Comparison")

cb, cg = st.columns(2)

def profile_row(label, value):
    return f"<p><strong>{label}:</strong> {value}</p>"

with cb:
    st.markdown("#### 👨 His Profile")
    st.markdown(f"""
    <div class="lm-profile-box">
      {profile_row('Age', str(boy['Age_at_Marriage']) + ' yrs')}
      {profile_row('Education', boy['Education_Level'])}
      {profile_row('Income', boy['Income_Level'])}
      {profile_row('Religion', boy['Religion'])}
      {profile_row('Caste Match', boy['Caste_Match'])}
      {profile_row('Location', boy['Urban_Rural'])}
      {profile_row('Marriage Type', boy['Marriage_Type'])}
      {profile_row('Children Desired', str(boy['Children_Count']))}
      {profile_row('Parental Approval', boy['Parental_Approval'])}
    </div>
    """, unsafe_allow_html=True)

with cg:
    st.markdown("#### 👩 Her Profile")
    st.markdown(f"""
    <div class="lm-profile-box">
      {profile_row('Age', str(girl['Age_at_Marriage']) + ' yrs')}
      {profile_row('Education', girl['Education_Level'])}
      {profile_row('Income', girl['Income_Level'])}
      {profile_row('Religion', girl['Religion'])}
      {profile_row('Caste Match', girl['Caste_Match'])}
      {profile_row('Location', girl['Urban_Rural'])}
      {profile_row('Marriage Type', girl['Marriage_Type'])}
      {profile_row('Children Desired', str(girl['Children_Count']))}
      {profile_row('Parental Approval', girl['Parental_Approval'])}
    </div>
    """, unsafe_allow_html=True)

ornamental_divider()

# ── Match factors chart ───────────────────────────────────────────────────────
st.markdown("### ✅ Matching Factors at a Glance")

match_df = pd.DataFrame([
    {'Factor': k, 'Match': 1 if v else 0} for k, v in matches.items()
])

colors = ['#6B8F71' if v == 1 else '#F2B5C8' for v in match_df['Match']]
texts  = ['✓ Match' if v == 1 else '✗ Mismatch' for v in match_df['Match']]

fig_match = go.Figure(go.Bar(
    x=match_df['Match'], y=match_df['Factor'], orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=texts, textposition='auto',
    hovertemplate='%{y}<br>%{text}<extra></extra>'
))
fig_match.update_layout(
    height=380, showlegend=False,
    xaxis=dict(range=[0, 1.3], showticklabels=False, showgrid=False),
    yaxis=dict(showgrid=False),
    margin=dict(l=180, r=20, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', size=13)
)
st.plotly_chart(fig_match, use_container_width=True)

ornamental_divider()

# ── Radar chart ───────────────────────────────────────────────────────────────
st.markdown("### 📊 Radar — Compatibility Dimensions")

categories = ['Education', 'Income', 'Religion', 'Location', 'Values', 'Age Gap', 'Goals']

def radar_score(profile, other, field, good_vals=None):
    if good_vals:
        return 80 if profile.get(field) in good_vals else 50
    return 80 if profile.get(field) == other.get(field) else 45

boy_scores  = [
    radar_score(boy, girl, 'Education_Level', ['Postgraduate', 'PhD']),
    radar_score(boy, girl, 'Income_Level', ['High']),
    80 if boy['Religion'] == girl['Religion'] else 45,
    80 if boy['Urban_Rural'] == girl['Urban_Rural'] else 45,
    80 if boy['Marriage_Type'] == girl['Marriage_Type'] else 45,
    80 if 2 <= age_diff <= 5 else 45,
    80 if boy['Children_Count'] == girl['Children_Count'] else 50,
]
girl_scores = [
    radar_score(girl, boy, 'Education_Level', ['Postgraduate', 'PhD']),
    radar_score(girl, boy, 'Income_Level', ['High']),
    80 if girl['Religion'] == boy['Religion'] else 45,
    80 if girl['Urban_Rural'] == boy['Urban_Rural'] else 45,
    80 if girl['Marriage_Type'] == boy['Marriage_Type'] else 45,
    80 if 2 <= age_diff <= 5 else 45,
    80 if girl['Children_Count'] == boy['Children_Count'] else 50,
]

fig_radar = go.Figure(data=[
    go.Scatterpolar(r=boy_scores,  theta=categories, fill='toself', name='Him',
                    marker_color='rgba(201,68,106,0.5)', line_color='#C9446A'),
    go.Scatterpolar(r=girl_scores, theta=categories, fill='toself', name='Her',
                    marker_color='rgba(107,143,113,0.5)', line_color='#6B8F71'),
])
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10))),
    showlegend=True, height=460,
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans'),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)
st.plotly_chart(fig_radar, use_container_width=True)

ornamental_divider()

# ── Action buttons ────────────────────────────────────────────────────────────
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("← Edit His Profile", use_container_width=True):
        st.switch_page("pages/1_Boy_Profile.py")
with b2:
    if st.button("← Edit Her Profile", use_container_width=True):
        st.switch_page("pages/2_Girl_Profile.py")
with b3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#bbb; font-size:0.85em; line-height:1.8;">
  💕 Love is important — but shared values and open communication build lasting marriages.<br>
  This analysis highlights statistical patterns, not personal truth. Your connection is what matters most.
</div>
""", unsafe_allow_html=True)
