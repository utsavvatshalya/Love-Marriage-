 LoveMatch AI - Indian Marriage Outcome Predictor

An intelligent machine learning platform that predicts Indian marriage outcomes using XGBoost, explainable AI (SHAP), and counterfactual recommendations (DiCE).



---

LoveMatch AI analyzes 10,000+ Indian marriage records across 17 features to predict:

1.  Marriage Type- Is it a Love or Arranged marriage?
2. Marriage Success- What's the divorce risk and satisfaction level?
3. Improvement Path - How to increase success probability?

All predictions come with **SHAP-based explainability** so you understand WHY the model predicts what it does.

### Key Features

-  **Probabilistic Predictions** - Get confidence scores (0-100%)
-  **SHAP Explainability** - Waterfall charts showing feature contributions
-  **Counterfactual Recommendations** - Get actionable "what-if" suggestions
-  **Interactive Visualizations** - Gauge charts, bar plots, comparison tables
-  **Zero Data Storage** - Privacy-first, no personal data saved
-  **Free Deployment** - Streamlit Community Cloud hosting

---

## 📦 Project Structure

```
lovematch_ai/
├── app.py                           # Streamlit home page entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── src/
│   ├── preprocess.py               # Preprocessing utilities & model loading
│   └── explainer.py                # SHAP + DiCE logic for explainability
│
├── pages/
│   ├── 1_Love_Marriage_Predictor.py   # Module 1: Love vs Arranged
│   ├── 2_Marriage_Success_Predictor.py # Module 2: Divorce & Satisfaction
│   ├── 3_Improve_My_Chances.py         # Module 3: Counterfactuals
│   └── 4_About.py                      # Module 4: Info & Documentation
│
├── models/                          # ← Drop all .pkl files here
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
    └── marriage_data_india.csv      # Training dataset (reference)
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/lovematch_ai.git
cd lovematch_ai
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Add Model Files

Download trained model files and place them in the `models/` folder:

```
models/
├── love_marriage_model.pkl
├── love_preprocessor.pkl
├── love_feature_names.pkl
├── love_feature_cols.pkl
├── divorce_model.pkl
├── divorce_preprocessor.pkl
├── divorce_feature_names.pkl
├── divorce_feature_cols.pkl
├── satisfaction_model.pkl
├── sat_preprocessor.pkl
├── sat_feature_names.pkl
├── sat_feature_cols.pkl
└── sat_label_encoder.pkl
```

**Note:** If you have `.pkl` files from model training, copy them to this directory.

### 4. Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📚 How to Use

### Module 1: Love Marriage Predictor 💕

1. Fill in all 17 marriage profile fields
2. Click "Predict Marriage Type"
3. View:
   - Probability gauge (Love % vs Arranged %)
   - Confidence level badge
   - SHAP waterfall chart (top 10 driving features)
   - Feature importance bar chart

**What You Learn:** Which factors influenced the marriage type classification

### Module 2: Marriage Success Predictor ✨

1. Fill in marriage profile (same 17 fields)
2. Click "Predict Marriage Success"
3. View:
   - Success probability gauge
   - Divorce risk percentage
   - Predicted satisfaction level (Low/Medium/High)
   - Top 10 features driving success/divorce
   - Risk factor breakdown by importance

**What You Learn:** Divorce likelihood and relationship satisfaction expectations

### Module 3: Improve My Chances 🎯

1. Fill in your current marriage profile
2. Click "Generate Recommendations"
3. Receive Top 3 suggestions:
   - Each shows current success % → projected success %
   - Before/after comparison
   - Improvement percentage (+X%)
4. Compare all scenarios in a table
5. Download recommendations as CSV

**What You Learn:** Specific changes that would most improve outcomes

### Module 4: About ℹ️

Learn about:
- Dataset composition and sources
- Model architecture (XGBoost details)
- Feature descriptions
- Technology stack
- Explainability methods (SHAP & DiCE)
- Limitations and disclaimers

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **ML Models** | XGBoost (Gradient Boosting) |
| **Explainability** | SHAP (SHapley Additive exPlanations) |
| **Recommendations** | DiCE-inspired Iterative Search |
| **Web Framework** | Streamlit |
| **Visualizations** | Plotly & Plotly Express |
| **Data Processing** | Pandas, NumPy, Scikit-learn |
| **Model Serialization** | Joblib |
| **Deployment** | Streamlit Community Cloud (FREE) |
| **Language** | Python 3.10+ |

---

## 📊 Dataset Overview

**Training Data:** 10,000+ Indian marriage records

### Features (17 Total)

#### Numeric (3)
- Age at Marriage (18-60 years)
- Children Count (0-10)
- Years Since Marriage (0-50 years)

#### Ordinal Encoded (3)
- Education Level → [School, Graduate, Postgraduate, PhD]
- Income Level → [Low, Middle, High]
- Parental Approval → [No, Partial, Yes]

#### One-Hot Encoded (11)
- Gender (Male/Female)
- Caste Match (Same/Different)
- Religion (Hindu/Muslim/Sikh/Christian/Others)
- Urban/Rural (Urban/Rural)
- Dowry Exchanged (Yes/No/Not Disclosed)
- Spouse Working (Yes/No)
- Inter-Caste (Yes/No)
- Inter-Religion (Yes/No)
- Marriage Type (Love/Arranged) - *for training*
- Divorce Status (Yes/No) - *for training*
- Extra feature for flexibility

### Target Variables

| Module | Target | Type | Classes |
|--------|--------|------|---------|
| Module 1 | Marriage Type | Binary | Love (1) / Arranged (0) |
| Module 2 | Divorce Status | Binary | Divorced (1) / Together (0) |
| Module 2 | Satisfaction | Multiclass | Low / Medium / High |

---

## 🤖 Model Architecture

### Preprocessing Pipeline

1. **StandardScaler** → Numeric features (Age, Children, Years)
2. **OrdinalEncoder** → Ordinal features (Education, Income, Approval)
3. **OneHotEncoder** → Categorical features (Gender, Religion, etc.)

### Three Trained Models

#### 🔴 Model 1: Love Marriage Classifier
- **Algorithm:** XGBoost Binary Classification
- **Input:** All 17 preprocessed features
- **Output:** Probability of Love Marriage
- **Explainability:** SHAP TreeExplainer

#### 🔵 Model 2: Divorce Risk Predictor
- **Algorithm:** XGBoost Binary Classification
- **Input:** All 17 preprocessed features
- **Output:** Probability of Divorce
- **Explainability:** SHAP feature importance

#### 🟢 Model 3: Satisfaction Predictor
- **Algorithm:** XGBoost Multiclass Classification
- **Input:** All 17 preprocessed features
- **Output:** Satisfaction Level (Low/Medium/High)
- **Explainability:** Probability distribution

### Explainability Techniques

**SHAP (SHapley Additive exPlanations)**
- Quantifies each feature's contribution to prediction
- Generates waterfall charts showing cumulative impact
- Ranks features by absolute importance
- Model-agnostic approach

**DiCE (Diverse Counterfactual Explanations)**
- Generates "what-if" scenarios
- Identifies minimal changes needed for outcome flip
- Shows actionable recommendations
- Ranks suggestions by impact percentage

---

## 🌐 Deployment on Streamlit Cloud (FREE)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: LoveMatch AI"
git branch -M main
git remote add origin https://github.com/yourusername/lovematch_ai.git
git push -u origin main
```

### Step 2: Create Streamlit Cloud Account

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign up with GitHub account
3. Authorize Streamlit to access your GitHub repos

### Step 3: Deploy Application

1. Click "New app" in Streamlit Cloud dashboard
2. Select your repository: `lovematch_ai`
3. Set main file: `app.py`
4. Click "Deploy"

### Step 4: Configure (Optional)

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#e74c3c"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#2c3e50"

[server]
headless = true
port = 8501
```

### Important: Model Files on GitHub

Option A: Commit `.pkl` files directly (if < 50MB each)
```bash
git add models/*.pkl
git commit -m "Add trained model files"
```

Option B: Use Git LFS for large files
```bash
git lfs install
git lfs track "*.pkl"
git add models/*.pkl
git commit -m "Add large model files with LFS"
```

Option C: Load from Cloud Storage (Google Drive, S3)
- Modify `src/preprocess.py` to download models at startup
- Use `st.cache_resource` to avoid re-downloading

---

## 💻 Local Development

### Run with Auto-Reload

```bash
streamlit run app.py --logger.level=debug
```

### Debug Mode

Edit `app.py` and add:
```python
import streamlit as st
st.set_page_config(layout="wide")

# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Pages

```bash
# Test Love Marriage Predictor
streamlit run pages/1_Love_Marriage_Predictor.py

# Test Marriage Success Predictor
streamlit run pages/2_Marriage_Success_Predictor.py
```

---

## 📋 Input Features Reference

When using the app, ensure you provide values for:

1. **Age at Marriage** - Slider 18-60
2. **Gender** - Select: Male / Female
3. **Education Level** - Ordinal: School → Graduate → Postgraduate → PhD
4. **Income Level** - Ordinal: Low → Middle → High
5. **Caste Match** - Same / Different
6. **Religion** - Select: Hindu / Muslim / Sikh / Christian / Others
7. **Parental Approval** - Ordinal: No → Partial → Yes
8. **Urban/Rural** - Urban / Rural
9. **Dowry Exchanged** - Yes / No / Not Disclosed
10. **Children Count** - Slider 0-10
11. **Years Since Marriage** - Slider 0-50
12. **Spouse Working** - Yes / No
13. **Inter-Caste** - Yes / No
14. **Inter-Religion** - Yes / No
15. **Marriage Type** - Love / Arranged (Module 1 only)
16. **Divorce Status** - Yes / No (Module 2 only)
17. **Marital Satisfaction** - Low / Medium / High (Module 2 only)

---

## ⚠️ Important Disclaimers

### Educational Purpose Only

This system is designed for **educational and entertainment purposes**. It is NOT a substitute for:
- Professional relationship counseling
- Legal advice
- Medical or psychological assessment
- Personal decision-making with loved ones

### Limitations

1. **Probabilistic, Not Certain** - Predictions show statistical likelihood, not certainty
2. **Historical Data** - Trained on past patterns; future may differ
3. **Correlation ≠ Causation** - ML identifies patterns, not causal relationships
4. **Demographic Limitations** - Based on Indian marriage data; may not generalize globally
5. **Unmeasured Factors** - Real relationships involve emotional, psychological factors not in dataset
6. **No Data Storage** - We don't save any personal information you enter

### Ethical Use

- 🟢 Use for self-reflection and discussion
- 🟢 Explore patterns in relationship factors
- 🟢 Generate ideas for conversations with partners
- 🔴 Don't make major life decisions solely based on predictions
- 🔴 Don't use to judge others' relationships
- 🔴 Always consult professionals for serious concerns

---

## 🔄 Model Retraining

To retrain models with new data:

1. Prepare `marriage_data_india.csv` with all features
2. Run training pipeline (separate repo/notebook)
3. Export `.pkl` files using joblib
4. Replace files in `models/` folder
5. Test predictions locally
6. Push to GitHub (Streamlit Cloud auto-redeploys)

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/lovematch_ai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/lovematch_ai/discussions)
- **Email:** your.email@example.com
- **LinkedIn:** [Your Profile](https://linkedin.com)

---

## 📜 License

This project is licensed under the **MIT License** - see LICENSE file for details.

You are free to:
- ✅ Use this project for educational purposes
- ✅ Modify and distribute copies
- ✅ Fork and create derivatives

With the conditions:
- ⚠️ Include original license and copyright notice
- ⚠️ Provide clear description of changes
- ⚠️ Use for non-commercial purposes

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Test locally before submitting PR
- Update README if adding features
- Include any new dependencies in requirements.txt

---

## 🙏 Acknowledgments

- **Dataset:** Indian marriage records (open source)
- **Libraries:** XGBoost, SHAP, Streamlit, Plotly teams
- **Inspiration:** Explainable AI research and counterfactual methods
- **Community:** All contributors and users providing feedback

---

## 📈 Future Enhancements

Potential improvements for v2.0:

- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] User accounts & history tracking (opt-in)
- [ ] Export predictions as detailed PDF report
- [ ] API endpoint for programmatic access
- [ ] Advanced visualizations (sankey diagrams, correlation heatmaps)
- [ ] Comparison with user's friends' profiles (anonymized)
- [ ] Integration with relationship counseling resources
- [ ] Mobile app version
- [ ] Real-time dataset updates and model retraining
- [ ] Community insights dashboard

---

## 📚 Learning Resources

### About the Methods

- **SHAP:** [SHAP Documentation](https://shap.readthedocs.io/)
- **XGBoost:** [XGBoost Docs](https://xgboost.readthedocs.io/)
- **DiCE:** [DiCE Paper & Docs](https://github.com/interpretml/DiCE)
- **Streamlit:** [Streamlit Docs](https://docs.streamlit.io/)

### Related Projects

- [LIME](https://github.com/marcotcr/lime) - Local Interpretable Model Explanations
- [Alibi](https://github.com/SeldonIO/alibi) - Explainability library
- [InterpretML](https://github.com/interpretml/interpret) - Microsoft's interpretability library

---

## ⭐ Show Your Support

If you found this project helpful, please:
- ⭐ Star the repository
- 📢 Share with your network
- 💬 Provide feedback and suggestions
- 🤝 Contribute improvements

---

**Made  by Utsav Vatshalya**

*"Understanding relationships through data science and explainable AI"*

---

## Version History

- **v1.0** (2026-06) - Initial release
  - 3 prediction modules (Love/Arranged, Success/Divorce, Satisfaction)
  - SHAP explainability
  - DiCE counterfactual recommendations
  - Streamlit web interface
  - FREE deployment on Streamlit Cloud

---

Last Updated: June 2026  
Python 3.10+ | Streamlit 1.40+
