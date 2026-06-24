"""
Module 3: Compatibility Analysis
Compare profiles and provide compatibility score with visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# Page config
st.set_page_config(
    page_title="Compatibility Analysis - LoveMatch AI",
    page_icon="💫",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .compatibility-score {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .score-number {
        font-size: 3.5em;
        font-weight: 800;
        margin: 20px 0;
    }
    .score-label {
        font-size: 1.3em;
        opacity: 0.95;
    }
    .recommendation {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 20px 0;
        border-left: 5px solid #FF6B6B;
    }
    .profile-box {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.06);
    }
    .match-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #eee;
    }
    .match-label {
        font-weight: 600;
        color: #333;
    }
    .match-status {
        font-weight: 700;
    }
    .match-yes {
        color: #27AE60;
    }
    .match-no {
        color: #E74C3C;
    }
    .match-partial {
        color: #F39C12;
    }
</style>
""", unsafe_allow_html=True)

st.title("💫 Compatibility Analysis")
st.markdown('<div style="background: #FF6B6B; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; font-weight: 600;">Step 3 of 3 - Compatibility Results</div>', unsafe_allow_html=True)

# Check if both profiles exist
if 'boy_profile' not in st.session_state or 'girl_profile' not in st.session_state:
    st.warning("⚠️ Please complete both profiles first!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Boy Profile", use_container_width=True):
            st.switch_page("pages/1_Boy_Profile.py")
    with col2:
        if st.button("← Girl Profile", use_container_width=True):
            st.switch_page("pages/2_Girl_Profile.py")
    st.stop()

boy = st.session_state['boy_profile']
girl = st.session_state['girl_profile']

# Calculate compatibility scores
def calculate_compatibility(boy, girl):
    """Calculate detailed compatibility metrics"""
    
    matches = {
        'Education Match': boy['Education_Level'] == girl['Education_Level'],
        'Income Level Match': boy['Income_Level'] == girl['Income_Level'],
        'Caste Match': boy['Caste_Match'] == girl['Caste_Match'],
        'Religion Match': boy['Religion'] == girl['Religion'],
        'Parental Approval': boy['Parental_Approval'] == 'Yes' and girl['Parental_Approval'] == 'Yes',
        'Location Preference': boy['Urban_Rural'] == girl['Urban_Rural'],
        'Marriage Type': boy['Marriage_Type'] == girl['Marriage_Type'],
        'Intercaste Open': boy['Inter-Caste'] == girl['Inter-Caste'] and boy['Inter-Caste'] == 'Yes',
        'Interreligion Open': boy['Inter-Religion'] == girl['Inter-Religion'] and boy['Inter-Religion'] == 'Yes',
        'Children Goals': boy['Children_Count'] == girl['Children_Count']
    }
    
    # Age compatibility (ideal gap 2-5 years)
    age_diff = abs(boy['Age_at_Marriage'] - girl['Age_at_Marriage'])
    age_match = 2 <= age_diff <= 5
    matches['Age Compatibility'] = age_match
    
    # Calculate overall score
    total_matches = sum(matches.values())
    compatibility_score = (total_matches / len(matches)) * 100
    
    return matches, compatibility_score, age_diff

matches, score, age_diff = calculate_compatibility(boy, girl)

# Display Compatibility Score
st.markdown(f"""
<div class="compatibility-score">
    <div class="score-label">Your Compatibility Score</div>
    <div class="score-number">{score:.1f}%</div>
    <div class="score-label">
        {"🟢 Highly Compatible - Marriage Ready!" if score >= 75 else "🟡 Moderately Compatible - Good Potential" if score >= 50 else "🔴 Low Compatibility - Consider Keeping Casual"}
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Recommendation
st.markdown("### 📋 Recommendation")

if score >= 75:
    rec_color = "#27AE60"
    rec_title = "💚 Marriage-Ready"
    rec_text = f"""
    **You have strong compatibility ({score:.0f}%)!**
    
    Based on the analysis, you align well on most important factors. You share similar values, 
    goals, and expectations. If you love each other, this relationship has a strong foundation for marriage.
    
    **Next Steps:**
    - Have deeper conversations about long-term goals
    - Discuss family planning and lifestyle expectations
    - Involve parents if comfortable
    - Plan for the future together
    """
elif score >= 50:
    rec_color = "#F39C12"
    rec_title = "⚠️ Keep Casual First"
    rec_text = f"""
    **You have moderate compatibility ({score:.0f}%).**
    
    There's good potential, but some areas need exploration. Consider spending more time together 
    to understand how you handle differences before making a big commitment.
    
    **Areas to Work On:**
    - Discuss differing expectations
    - Understand each other's non-negotiables
    - Explore compatibility in these areas more deeply
    - Take time before deciding on marriage
    """
else:
    rec_color = "#E74C3C"
    rec_title = "❌ Approach with Caution"
    rec_text = f"""
    **Low compatibility score ({score:.0f}%).**
    
    While love is important, significant differences in core values, goals, or expectations 
    can create challenges. Consider whether these differences are dealbreakers or can be addressed.
    
    **Important Questions:**
    - Can you compromise on key differences?
    - Are values truly incompatible?
    - Is there flexibility on either side?
    - What would marriage look like with these differences?
    """

st.markdown(f"""
<div class="recommendation" style="border-left-color: {rec_color}; background: linear-gradient(90deg, white 0%, rgba({rec_color.lstrip('#')}, 0.02) 100%);">
    <h3 style="color: {rec_color}; margin-top: 0;">{rec_title}</h3>
    <p>{rec_text}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Side-by-side profile comparison
st.markdown("### 👥 Profile Comparison")

col_boy, col_spacer, col_girl = st.columns([1.5, 0.2, 1.5])

with col_boy:
    st.markdown("#### 👨 Boy's Profile")
    st.markdown(f"""
    <div class="profile-box">
        <p><strong>Age:</strong> {boy['Age_at_Marriage']} years</p>
        <p><strong>Education:</strong> {boy['Education_Level']}</p>
        <p><strong>Income:</strong> {boy['Income_Level']}</p>
        <p><strong>Religion:</strong> {boy['Religion']}</p>
        <p><strong>Caste Match:</strong> {boy['Caste_Match']}</p>
        <p><strong>Location:</strong> {boy['Urban_Rural']}</p>
        <p><strong>Marriage Type:</strong> {boy['Marriage_Type']}</p>
        <p><strong>Children Desired:</strong> {boy['Children_Count']}</p>
        <p><strong>Parental Approval:</strong> {boy['Parental_Approval']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_girl:
    st.markdown("#### 👩 Girl's Profile")
    st.markdown(f"""
    <div class="profile-box">
        <p><strong>Age:</strong> {girl['Age_at_Marriage']} years</p>
        <p><strong>Education:</strong> {girl['Education_Level']}</p>
        <p><strong>Income:</strong> {girl['Income_Level']}</p>
        <p><strong>Religion:</strong> {girl['Religion']}</p>
        <p><strong>Caste Match:</strong> {girl['Caste_Match']}</p>
        <p><strong>Location:</strong> {girl['Urban_Rural']}</p>
        <p><strong>Marriage Type:</strong> {girl['Marriage_Type']}</p>
        <p><strong>Children Desired:</strong> {girl['Children_Count']}</p>
        <p><strong>Parental Approval:</strong> {girl['Parental_Approval']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Matching factors visualization
st.markdown("### ✅ Matching Factors")

# Create matching data
match_data = []
for factor, is_match in matches.items():
    match_data.append({
        'Factor': factor,
        'Match': 'Yes' if is_match else 'No',
        'Value': 1 if is_match else 0
    })

match_df = pd.DataFrame(match_data)

# Horizontal bar chart
colors = ['#27AE60' if v == 1 else '#E74C3C' for v in match_df['Value']]
fig_match = go.Figure(data=[
    go.Bar(
        x=match_df['Value'],
        y=match_df['Factor'],
        orientation='h',
        marker=dict(color=colors),
        text=['✓ Match' if v == 1 else '✗ Mismatch' for v in match_df['Value']],
        textposition='auto',
        hovertemplate='%{y}<br>Status: %{text}<extra></extra>'
    )
])

fig_match.update_layout(
    title="Compatibility Factors",
    xaxis_title="",
    yaxis_title="",
    height=400,
    showlegend=False,
    template="plotly_white",
    xaxis=dict(range=[0, 1.2], showticklabels=False),
    margin=dict(l=200)
)

st.plotly_chart(fig_match, use_container_width=True)

st.divider()

# Radar chart for detailed analysis
st.markdown("### 📊 Compatibility Breakdown")

# Create radar data
categories = ['Education', 'Income', 'Religion', 'Location', 'Values', 'Age', 'Goals']
boy_scores = [
    80 if boy['Education_Level'] in ['Postgraduate', 'PhD'] else 60,
    80 if boy['Income_Level'] == 'High' else 60,
    80 if boy['Religion'] == girl['Religion'] else 50,
    80 if boy['Urban_Rural'] == girl['Urban_Rural'] else 50,
    80 if boy['Marriage_Type'] == girl['Marriage_Type'] else 50,
    80 if 2 <= age_diff <= 5 else 50,
    80 if boy['Children_Count'] == girl['Children_Count'] else 60
]

girl_scores = [
    80 if girl['Education_Level'] in ['Postgraduate', 'PhD'] else 60,
    80 if girl['Income_Level'] == 'High' else 60,
    80 if girl['Religion'] == boy['Religion'] else 50,
    80 if girl['Urban_Rural'] == boy['Urban_Rural'] else 50,
    80 if girl['Marriage_Type'] == boy['Marriage_Type'] else 50,
    80 if 2 <= age_diff <= 5 else 50,
    80 if girl['Children_Count'] == boy['Children_Count'] else 60
]

fig_radar = go.Figure(data=[
    go.Scatterpolar(
        r=boy_scores,
        theta=categories,
        fill='toself',
        name='Boy',
        marker_color='rgba(255, 107, 107, 0.5)',
        line_color='#FF6B6B'
    ),
    go.Scatterpolar(
        r=girl_scores,
        theta=categories,
        fill='toself',
        name='Girl',
        marker_color='rgba(44, 62, 80, 0.5)',
        line_color='#2C3E50'
    )
])

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=True,
    height=500,
    title="Compatibility Radar - Boy vs Girl"
)

st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# Action buttons
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("← Edit Boy Profile", use_container_width=True):
        st.switch_page("pages/1_Boy_Profile.py")

with col_btn2:
    if st.button("← Edit Girl Profile", use_container_width=True):
        st.switch_page("pages/2_Girl_Profile.py")

with col_btn3:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/0_Home.py")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; margin-top: 40px;">
<p>💕 Remember: Love is important, but compatibility helps create stronger foundations for lasting relationships.</p>
<p>This analysis is based on demographic factors. Your personal connection and communication are equally important.</p>
</div>
""", unsafe_allow_html=True)
