"""
Shared preprocessing utilities for LoveMatch AI models.
Handles loading models, preprocessors, and feature transformation.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
import streamlit as st


# Define the base path for models
MODELS_DIR = Path(__file__).parent.parent / "models"


@st.cache_resource
def load_model(model_name: str):
    """Load a trained model from the models directory."""
    model_path = MODELS_DIR / model_name
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    return joblib.load(model_path)


@st.cache_resource
def load_preprocessor(preprocessor_name: str):
    """Load a preprocessor (ColumnTransformer) from models directory."""
    preprocessor_path = MODELS_DIR / preprocessor_name
    if not preprocessor_path.exists():
        raise FileNotFoundError(f"Preprocessor not found: {preprocessor_path}")
    return joblib.load(preprocessor_path)


@st.cache_resource
def load_feature_names(feature_names_file: str) -> List[str]:
    """Load feature names list from models directory."""
    feature_path = MODELS_DIR / feature_names_file
    if not feature_path.exists():
        raise FileNotFoundError(f"Feature names file not found: {feature_path}")
    return joblib.load(feature_path)


@st.cache_resource
def load_feature_cols(feature_cols_file: str) -> List[str]:
    """Load raw input column names from models directory."""
    feature_path = MODELS_DIR / feature_cols_file
    if not feature_path.exists():
        raise FileNotFoundError(f"Feature columns file not found: {feature_path}")
    return joblib.load(feature_path)


@st.cache_resource
def load_label_encoder(encoder_name: str):
    """Load a LabelEncoder from models directory."""
    encoder_path = MODELS_DIR / encoder_name
    if not encoder_path.exists():
        raise FileNotFoundError(f"Label encoder not found: {encoder_path}")
    return joblib.load(encoder_path)


def preprocess_input(input_dict: Dict[str, Any], preprocessor) -> np.ndarray:
    """
    Preprocess input dictionary using the provided ColumnTransformer.
    
    Args:
        input_dict: Dictionary with feature names as keys and user inputs as values
        preprocessor: ColumnTransformer object
    
    Returns:
        Preprocessed numpy array ready for model prediction
    """
    df = pd.DataFrame([input_dict])
    preprocessed = preprocessor.transform(df)
    return preprocessed


def get_feature_names_for_prediction(
    raw_features: Dict[str, Any],
    feature_names: List[str]
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Align raw input features with preprocessed feature names for SHAP.
    
    Returns:
        Tuple of (preprocessed_array, feature_values_dict)
    """
    return {name: raw_features.get(name, None) for name in feature_names}


def build_input_form_fields(feature_cols: List[str]) -> Dict[str, Any]:
    """
    Build Streamlit input form based on feature column names.
    Handles different input types (categorical, numeric) based on column names.
    """
    user_input = {}
    
    numeric_cols = [
        'Age_at_Marriage',
        'Children_Count',
        'Years_Since_Marriage',
        'Income_Level_numeric'
    ]
    
    ordinal_cols = {
        'Education_Level': ['School', 'Graduate', 'Postgraduate', 'PhD'],
        'Income_Level': ['Low', 'Middle', 'High'],
        'Parental_Approval': ['No', 'Partial', 'Yes'],
        'Marital_Satisfaction': ['Low', 'Medium', 'High']
    }
    
    categorical_cols = {
        'Marriage_Type': ['Love', 'Arranged'],
        'Gender': ['Male', 'Female'],
        'Caste_Match': ['Same', 'Different'],
        'Religion': ['Hindu', 'Muslim', 'Sikh', 'Christian', 'Others'],
        'Urban_Rural': ['Urban', 'Rural'],
        'Dowry_Exchanged': ['Yes', 'No', 'Not Disclosed'],
        'Spouse_Working': ['Yes', 'No'],
        'Inter-Caste': ['Yes', 'No'],
        'Inter-Religion': ['Yes', 'No'],
        'Divorce_Status': ['Yes', 'No']
    }
    
    for col in feature_cols:
        if col in numeric_cols:
            if col == 'Age_at_Marriage':
                user_input[col] = st.slider(
                    f"Select {col}",
                    min_value=18,
                    max_value=60,
                    value=30,
                    step=1
                )
            elif col == 'Children_Count':
                user_input[col] = st.slider(
                    f"Select {col}",
                    min_value=0,
                    max_value=10,
                    value=2,
                    step=1
                )
            elif col == 'Years_Since_Marriage':
                user_input[col] = st.slider(
                    f"Select {col}",
                    min_value=0,
                    max_value=50,
                    value=5,
                    step=1
                )
        
        elif col in ordinal_cols:
            user_input[col] = st.selectbox(
                f"Select {col}",
                options=ordinal_cols[col],
                index=0
            )
        
        elif col in categorical_cols:
            user_input[col] = st.selectbox(
                f"Select {col}",
                options=categorical_cols[col],
                index=0
            )
    
    return user_input


def safe_model_load(model_name: str, display_name: str = None):
    """
    Safely load a model with user-friendly error handling.
    """
    try:
        return load_model(model_name)
    except FileNotFoundError as e:
        st.error(f"❌ {display_name or model_name} not found!")
        st.info(f"Please ensure `{model_name}` exists in the `models/` folder.")
        st.stop()


def safe_preprocessor_load(preprocessor_name: str, display_name: str = None):
    """
    Safely load a preprocessor with user-friendly error handling.
    """
    try:
        return load_preprocessor(preprocessor_name)
    except FileNotFoundError as e:
        st.error(f"❌ {display_name or preprocessor_name} not found!")
        st.info(f"Please ensure `{preprocessor_name}` exists in the `models/` folder.")
        st.stop()


def safe_feature_load(feature_file: str, display_name: str = None):
    """
    Safely load feature names/columns with user-friendly error handling.
    """
    try:
        return load_feature_names(feature_file)
    except FileNotFoundError:
        st.error(f"❌ {display_name or feature_file} not found!")
        st.info(f"Please ensure `{feature_file}` exists in the `models/` folder.")
        st.stop()


def format_probability(prob: float) -> str:
    """Format probability as percentage string."""
    return f"{prob * 100:.1f}%"


def get_confidence_label(prob: float) -> str:
    """Get confidence level label based on probability."""
    if prob >= 0.9:
        return "🟢 Very High Confidence"
    elif prob >= 0.75:
        return "🟢 High Confidence"
    elif prob >= 0.6:
        return "🟡 Moderate Confidence"
    elif prob >= 0.4:
        return "🟡 Low Confidence"
    else:
        return "🔴 Very Low Confidence"


def create_input_dataframe(user_input: Dict[str, Any], feature_cols: List[str]) -> pd.DataFrame:
    """
    Create a properly ordered DataFrame for preprocessing.
    """
    # Ensure all required columns are present
    complete_input = {col: user_input.get(col, None) for col in feature_cols}
    return pd.DataFrame([complete_input])
