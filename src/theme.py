"""
LoveMatch AI — Shared Visual Theme
Inject via: from src.theme import inject_theme, page_header
"""

import streamlit as st

THEME_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Page background ── */
.stApp {
  background: linear-gradient(160deg, #FDF6F0 0%, #F7EFF4 50%, #FDF6F0 100%) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── DO NOT HIDE SIDEBAR NAV — only hide footer/menu ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* ── HEADINGS on main content ── */
.main h1 {
  font-family: 'Cormorant Garamond', serif !important;
  font-weight: 700 !important;
  color: #7B2D42 !important;
  font-size: 2.6em !important;
  letter-spacing: -0.5px !important;
  line-height: 1.2 !important;
}
.main h2 {
  font-family: 'Cormorant Garamond', serif !important;
  font-weight: 600 !important;
  color: #7B2D42 !important;
  font-size: 1.9em !important;
}
.main h3 {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  color: #C9446A !important;
  font-size: 1.15em !important;
}

/* ── SIDEBAR — use config.toml for colors, just style nav here ── */
[data-testid="stSidebarNavLink"] {
  border-radius: 8px !important;
  margin: 2px 0 !important;
  padding: 8px 14px !important;
  transition: background 0.15s !important;
}
[data-testid="stSidebarNavLink"]:hover {
  background: rgba(201, 68, 106, 0.12) !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
  background: rgba(201, 68, 106, 0.18) !important;
  font-weight: 600 !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%) !important;
  color: #FDF6F0 !important;
  border: none !important;
  border-radius: 30px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  padding: 0.6em 2em !important;
  box-shadow: 0 4px 14px rgba(201,68,106,0.30) !important;
  transition: all 0.2s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(201,68,106,0.40) !important;
}
.stFormSubmitButton > button {
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%) !important;
  color: #FDF6F0 !important;
  border: none !important;
  border-radius: 30px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  padding: 0.7em 2em !important;
  box-shadow: 0 4px 14px rgba(201,68,106,0.30) !important;
  transition: all 0.2s ease !important;
}
.stFormSubmitButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(201,68,106,0.40) !important;
}

/* ── WIDGET LABELS ── */
[data-testid="stWidgetLabel"] p {
  color: #2E2E2E !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9em !important;
  font-weight: 500 !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background: white !important;
  border: 1.5px solid #F2B5C8 !important;
  border-radius: 10px !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {
  color: #2E2E2E !important;
  font-family: 'DM Sans', sans-serif !important;
}
[data-baseweb="popover"] [role="option"] {
  color: #2E2E2E !important;
  font-family: 'DM Sans', sans-serif !important;
  background: white !important;
}
[data-baseweb="popover"] [role="option"]:hover {
  background: #FDF6F0 !important;
  color: #7B2D42 !important;
}
[data-baseweb="popover"] [aria-selected="true"] {
  background: #F7EFF4 !important;
  color: #C9446A !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [role="slider"] {
  background: #C9446A !important;
  border-color: #C9446A !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
  background: #C9446A !important;
}

/* ── RADIO ── */
[data-testid="stRadio"] label span {
  color: #2E2E2E !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: white !important;
  padding: 16px 20px !important;
  border-radius: 14px !important;
  border-bottom: 3px solid #F2B5C8 !important;
  box-shadow: 0 4px 24px rgba(122,45,66,0.10) !important;
}
[data-testid="stMetricLabel"] p {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.78em !important;
  text-transform: uppercase !important;
  letter-spacing: 0.8px !important;
  color: #888 !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 2em !important;
  font-weight: 700 !important;
  color: #7B2D42 !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
  background: white !important;
  padding: 8px !important;
  border-radius: 14px !important;
  border: 1px solid #F2B5C8 !important;
  gap: 6px !important;
}
[data-baseweb="tab"] {
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  color: #666 !important;
  background: transparent !important;
}
[data-baseweb="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%) !important;
  color: white !important;
}
[data-baseweb="tab"] p { color: inherit !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] details {
  border: 1px solid #F2B5C8 !important;
  border-radius: 14px !important;
  background: white !important;
}
[data-testid="stExpander"] summary {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  color: #7B2D42 !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li {
  color: #2E2E2E !important;
  font-family: 'DM Sans', sans-serif !important;
  line-height: 1.7 !important;
}

/* ── DIVIDER ── */
hr {
  border: none !important;
  border-top: 1px solid #F2B5C8 !important;
  margin: 28px 0 !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
  border-radius: 14px !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
  border-radius: 14px !important;
  border: 1px solid #F2B5C8 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #FDF6F0; }
::-webkit-scrollbar-thumb { background: #F2B5C8; border-radius: 3px; }

/* ════════════════════════════
   CUSTOM CARD COMPONENTS
   ════════════════════════════ */

.lm-card {
  background: white;
  border-radius: 14px;
  padding: 28px 32px;
  box-shadow: 0 4px 24px rgba(122,45,66,0.10);
  border: 1px solid rgba(242,181,200,0.4);
}

/* Rose gradient card */
.lm-card-rose {
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%) !important;
  border-radius: 14px;
  padding: 28px 32px;
  box-shadow: 0 8px 28px rgba(201,68,106,0.28);
}
.lm-card-rose * { color: white !important; }

/* Gold gradient card */
.lm-card-gold {
  background: linear-gradient(135deg, #E8972A 0%, #c67d1a 100%) !important;
  border-radius: 14px;
  padding: 28px 32px;
  box-shadow: 0 8px 28px rgba(232,151,42,0.28);
}
.lm-card-gold * { color: white !important; }

/* Sage gradient card */
.lm-card-sage {
  background: linear-gradient(135deg, #6B8F71 0%, #4e6e54 100%) !important;
  border-radius: 14px;
  padding: 28px 32px;
  box-shadow: 0 8px 28px rgba(107,143,113,0.28);
}
.lm-card-sage * { color: white !important; }

.lm-metric-val {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.4em;
  font-weight: 700;
  margin: 8px 0 4px;
  line-height: 1;
}
.lm-metric-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75em;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  opacity: 0.88;
}

.lm-badge {
  display: inline-block;
  padding: 6px 18px;
  border-radius: 20px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82em;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.lm-badge-rose  { background: rgba(255,255,255,0.22); color: white !important; }
.lm-badge-green { background: #e6f4ea; color: #2d6a4f !important; }
.lm-badge-amber { background: #fff3cd; color: #856404 !important; }
.lm-badge-red   { background: #fde8ee; color: #7B2D42 !important; }

.lm-suggestion {
  background: white;
  border-radius: 14px;
  padding: 24px 28px;
  border-left: 5px solid #E8972A;
  box-shadow: 0 4px 24px rgba(122,45,66,0.10);
  margin: 16px 0;
}
.lm-suggestion.high   { border-left-color: #6B8F71; }
.lm-suggestion.medium { border-left-color: #E8972A; }
.lm-suggestion.low    { border-left-color: #F2B5C8; }

.lm-before-after {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: #F7EFF4;
  border-radius: 12px;
  padding: 20px;
  margin: 14px 0;
  text-align: center;
}
.lm-before-after .val {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2em;
  font-weight: 700;
  color: #7B2D42;
}
.lm-before-after .lbl {
  font-size: 0.72em;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #888;
}
.lm-before-after .arrow { font-size: 1.8em; color: #6B8F71; }

.lm-divider-rose {
  height: 3px;
  background: linear-gradient(90deg, #C9446A 0%, #F2B5C8 60%, transparent 100%);
  border: none;
  border-radius: 2px;
  margin: 6px 0 24px;
}

.lm-step-badge {
  background: linear-gradient(135deg, #C9446A, #7B2D42);
  color: white !important;
  padding: 12px 24px;
  border-radius: 30px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 0.88em;
  letter-spacing: 0.5px;
  display: inline-block;
  margin-bottom: 20px;
}

.lm-profile-box {
  background: white;
  border-radius: 14px;
  padding: 22px 26px;
  box-shadow: 0 4px 24px rgba(122,45,66,0.10);
  border: 1px solid rgba(242,181,200,0.4);
}
.lm-profile-box p {
  margin: 8px 0;
  font-size: 0.95em;
  color: #2E2E2E;
  border-bottom: 1px solid #F7EFF4;
  padding-bottom: 8px;
}
.lm-profile-box p:last-child { border-bottom: none; }

.lm-compatibility-hero {
  background: linear-gradient(135deg, #C9446A 0%, #7B2D42 100%) !important;
  border-radius: 20px;
  padding: 48px 40px;
  text-align: center;
  margin: 20px 0;
  box-shadow: 0 12px 40px rgba(201,68,106,0.30);
  position: relative;
  overflow: hidden;
}
.lm-compatibility-hero * { color: white !important; }
.lm-compatibility-hero::before {
  content: '💍';
  position: absolute;
  font-size: 120px;
  opacity: 0.07;
  top: -20px;
  right: -10px;
}
.lm-compatibility-hero .score {
  font-family: 'Cormorant Garamond', serif;
  font-size: 5em;
  font-weight: 700;
  line-height: 1;
  margin: 16px 0 8px;
}
.lm-compatibility-hero .tagline {
  font-size: 1.15em;
  opacity: 0.92;
}

.lm-recommendation {
  background: white;
  padding: 28px 32px;
  border-radius: 14px;
  box-shadow: 0 4px 24px rgba(122,45,66,0.10);
  border-left: 6px solid #C9446A;
}
.lm-recommendation p,
.lm-recommendation li { color: #2E2E2E !important; line-height: 1.7; }

.lm-tech-pill {
  display: inline-block;
  background: #F7EFF4;
  border: 1px solid #F2B5C8;
  color: #7B2D42;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.82em;
  font-weight: 600;
  margin: 4px;
  font-family: 'DM Sans', sans-serif;
}

.lm-model-card {
  border-radius: 14px;
  padding: 28px;
  margin: 16px 0;
}
.lm-model-card * { color: white !important; }

.lm-model-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.18);
  font-size: 0.92em;
}
.lm-model-row:last-child { border-bottom: none; }
.lm-model-row .k { opacity: 0.8; }
.lm-model-row .v { font-weight: 600; }
</style>
"""


def inject_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="padding: 8px 0 4px;">
      <div style="font-size:2.4em; line-height:1; margin-bottom:6px;">{icon}</div>
      <h1 style="margin:0; padding:0; font-family:'Cormorant Garamond',serif;
                 color:#7B2D42; font-size:2.6em; font-weight:700;">{title}</h1>
      <div class="lm-divider-rose"></div>
      {"<p style='font-family:DM Sans,sans-serif; font-size:1.05em; color:#777; line-height:1.7; margin-bottom:20px;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def ornamental_divider():
    st.markdown("""
    <div style="text-align:center; color:#F2B5C8; font-size:1.3em;
                margin: 20px 0; letter-spacing:12px;">
      ✦ ✦ ✦
    </div>
    """, unsafe_allow_html=True)
