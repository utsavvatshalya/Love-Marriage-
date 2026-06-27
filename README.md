# 💍 LoveMatch AI

> *Built by Utsav Vatshalya — a final-year CS student who thought it'd be interesting to point machine learning at one of the most human decisions there is.*

Indian marriages are fascinating to study from a data perspective. They sit at the intersection of personal choice, family dynamics, economic factors, and social context — all of which leave measurable signals. This project trains XGBoost models on 10,000 real Indian marriage records and wraps them in a Streamlit app that tries to make those signals legible.

It's not a matchmaking tool. It won't tell you who to marry. What it does is show you *what the data says* about patterns in marriage outcomes — and, more usefully, *why* it thinks that, using SHAP to break down every prediction feature by feature.

---

## What it actually does

Three modules, each asking a different question:

**💕 Love or Arranged?**
Fill in a marriage profile and see whether it statistically resembles a love marriage or an arranged one. The interesting part isn't the prediction — it's the SHAP waterfall chart that shows exactly which factors pushed it in either direction.

**✨ Will it last?**
Predict divorce risk and marital satisfaction (Low / Medium / High) from the same profile inputs. Useful for understanding which factors the model thinks matter most to a marriage's longevity.

**🎯 What would change the outcome?**
This is the most practically interesting module. It runs counterfactual analysis — "if parental approval changed from Partial to Yes, your success probability goes from 64% to 77%." Not magic, just the model being asked to reason about its own predictions.

---

## Project structure

```
lovematch_ai/
├── app.py                              # Home page, entry point
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml                     # Theme config (colors, fonts)
│
├── src/
│   ├── preprocess.py                   # Model loading, input processing
│   ├── explainer.py                    # SHAP + counterfactual logic
│   └── theme.py                        # Shared CSS / wedding UI theme
│
├── pages/
│   ├── 1_Love_Marriage_Predictor.py    # Module 1
│   ├── 2_Marriage_Success_Predictor.py # Module 2
│   ├── 3_Improve_My_Chances.py         # Module 3
│   └── 4_About.py
│
├── models/                             # ← put your .pkl files here
│   ├── love_marriage_model.pkl
│   ├── love_preprocessor.pkl
│   ├── love_feature_names.pkl
│   ├── love_feature_cols.pkl
│   ├── divorce_model.pkl
│   ├── divorce_preprocessor.pkl
│   ├── divorce_feature_names.pkl
│   ├── divorce_feature_cols.pkl
│   ├── satisfaction_model.pkl
│   ├── sat_preprocessor.pkl
│   ├── sat_feature_names.pkl
│   ├── sat_feature_cols.pkl
│   └── sat_label_encoder.pkl
│
└── data/
    └── marriage_data_india.csv
```

---

## Getting it running

**1. Clone and set up**

```bash
git clone https://github.com/utsavvatshalya/lovematch_ai.git
cd lovematch_ai
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Add the trained models**

Train the models using the Kaggle notebook (link in the repo wiki), then drop all `.pkl` files into the `models/` folder. The app will error clearly if any are missing.

**3. Run**

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## The dataset

10,000 Indian marriage records across 17 features:

| Type | Features |
|---|---|
| Numeric | Age at Marriage, Children Count, Years Since Marriage |
| Ordinal | Education Level, Income Level, Parental Approval |
| Categorical | Gender, Caste Match, Religion, Urban/Rural, Dowry, Spouse Working, Inter-Caste, Inter-Religion |
| Target (M1) | Marriage Type — Love / Arranged |
| Target (M2) | Divorce Status + Marital Satisfaction |

---

## How the models work

Three separate XGBoost classifiers, each trained to predict one thing:

- **Love Marriage model** — binary, predicts marriage type
- **Divorce Risk model** — binary, predicts whether a marriage ends in divorce
- **Satisfaction model** — multiclass (Low / Medium / High), predicts marital satisfaction

Preprocessing uses a `ColumnTransformer` pipeline: StandardScaler on numeric features, OrdinalEncoder on ordinal ones, OneHotEncoder on categoricals. SMOTE handles the class imbalance in the divorce model (only ~10% of records are divorces).

SHAP's `TreeExplainer` runs on the XGBoost models natively — fast and exact, no approximations.

The counterfactual logic in Module 3 isn't full DiCE. It's an iterative search: for each actionable feature (things you can realistically change — income, education, parental approval, spousal working status), it swaps the value to the next-best option, re-runs the preprocessor and model, and records the probability delta. Features like age, religion, and caste are intentionally excluded.

---

## Deploying to Streamlit Cloud

Streamlit Cloud is free and deploys directly from GitHub. Takes about 5 minutes.

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/yourusername/lovematch_ai.git
git push -u origin main
```

Then go to [streamlit.io/cloud](https://streamlit.io/cloud), connect your GitHub, select this repo, set the main file to `app.py`, and hit Deploy.

**Model files on GitHub:** If each `.pkl` is under 50MB, just commit them directly. If they're larger, use Git LFS:

```bash
git lfs install
git lfs track "*.pkl"
git add models/*.pkl
git commit -m "add model files"
```

---

## Input features quick reference

| # | Feature | Input type | Options / Range |
|---|---|---|---|
| 1 | Age at Marriage | Slider | 18 – 60 |
| 2 | Gender | Dropdown | Male / Female |
| 3 | Education Level | Dropdown | School → Graduate → Postgraduate → PhD |
| 4 | Income Level | Dropdown | Low → Middle → High |
| 5 | Caste Match | Dropdown | Same / Different |
| 6 | Religion | Dropdown | Hindu / Muslim / Sikh / Christian / Others |
| 7 | Parental Approval | Dropdown | No → Partial → Yes |
| 8 | Urban / Rural | Dropdown | Urban / Rural |
| 9 | Dowry Exchanged | Dropdown | Yes / No / Not Disclosed |
| 10 | Children Count | Slider | 0 – 10 |
| 11 | Years Since Marriage | Slider | 0 – 50 |
| 12 | Spouse Working | Dropdown | Yes / No |
| 13 | Inter-Caste | Dropdown | Yes / No |
| 14 | Inter-Religion | Dropdown | Yes / No |
| 15 | Marriage Type | Dropdown | Love / Arranged *(Module 2 & 3 only)* |
| 16 | Divorce Status | Dropdown | Yes / No *(Module 2 only)* |
| 17 | Marital Satisfaction | Dropdown | Low / Medium / High *(Module 2 only)* |

---

## Tech stack

| | |
|---|---|
| Models | XGBoost |
| Explainability | SHAP TreeExplainer |
| Counterfactuals | Custom iterative search (DiCE-inspired) |
| UI | Streamlit |
| Charts | Plotly |
| Data | Pandas, NumPy, Scikit-learn |
| Serialization | Joblib |
| Deployment | Streamlit Community Cloud |

---

## A note on what this isn't

The predictions are statistical patterns from historical data, not truth. A high divorce risk score doesn't mean a marriage will fail. A high success score doesn't mean it'll be happy. Real relationships are shaped by things no dataset captures — how people communicate, whether they trust each other, how they handle the hard moments.

Use this as a lens for self-reflection, not a verdict. If anything it surfaces raises a real concern, talk to someone who actually knows you — a counsellor, a trusted person, your partner.

---

## If you want to retrain the models

1. Update `data/marriage_data_india.csv` with new records
2. Run the training notebook (Kaggle link in wiki)
3. Export the new `.pkl` files
4. Drop them into `models/`, replacing the old ones
5. Test locally, then push — Streamlit Cloud redeploys automatically

---

## Resources

- [SHAP docs](https://shap.readthedocs.io/) — genuinely good documentation
- [XGBoost docs](https://xgboost.readthedocs.io/)
- [DiCE paper](https://github.com/interpretml/DiCE) — the original counterfactual method this is inspired by
- [Streamlit docs](https://docs.streamlit.io/)

---

## Future ideas

Things I'd add if I kept working on this:

- [ ] Hindi language support
- [ ] PDF export of the full prediction report
- [ ] A proper DiCE integration replacing the current iterative search
- [ ] Correlation heatmap in the About page
- [ ] API endpoint so the predictions can be called programmatically

---

*Made by Utsav Vatshalya · June 2026 · Python 3.10+ · Streamlit 1.40+*
