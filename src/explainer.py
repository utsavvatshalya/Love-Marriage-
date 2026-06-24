"""
SHAP explainability and counterfactual explanation logic for LoveMatch AI.
Provides interpretability for model predictions.
"""

import shap
import pandas as pd
import numpy as np
import streamlit as st
from typing import Tuple, List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px


@st.cache_resource
def create_shap_explainer(_model, X_sample):
    """
    Create a SHAP TreeExplainer for XGBoost models.
    
    Args:
        _model: Trained XGBoost model (not hashed by Streamlit cache)
        X_sample: Sample data for expected values (preprocessed numpy array)
    
    Returns:
        shap.TreeExplainer object
    """
    explainer = shap.TreeExplainer(_model)
    return explainer


def get_shap_values(explainer, X_processed: np.ndarray, model_type: str = "binary"):
    """
    Calculate SHAP values for prediction explanation.
    
    Args:
        explainer: SHAP TreeExplainer
        X_processed: Preprocessed input data
        model_type: "binary" or "multiclass"
    
    Returns:
        SHAP values array
    """
    shap_values = explainer.shap_values(X_processed)
    return shap_values


def plot_shap_waterfall(explainer, X_processed: np.ndarray, feature_names: List[str],
                        expected_value_idx: int = 1) -> go.Figure:
    """
    Create a SHAP waterfall plot for binary classification models.
    Shows how each feature contributes to the prediction.
    
    Args:
        explainer: SHAP TreeExplainer
        X_processed: Preprocessed input data (single sample)
        feature_names: List of feature names
        expected_value_idx: Index for expected value (usually 1 for positive class)
    
    Returns:
        Plotly figure
    """
    shap_values = explainer.shap_values(X_processed)
    
    # For binary classification, take the positive class (index 1)
    if isinstance(shap_values, list):
        shap_vals = shap_values[expected_value_idx][0]
        expected_val = explainer.expected_value[expected_value_idx]
    else:
        shap_vals = shap_values[0]
        expected_val = explainer.expected_value
    
    # Get feature values
    feature_values = X_processed[0]
    
    # Create DataFrame for visualization
    shap_df = pd.DataFrame({
        'Feature': feature_names,
        'SHAP Value': shap_vals,
        'Feature Value': feature_values
    })
    
    # Sort by absolute SHAP value
    shap_df['Abs_SHAP'] = shap_df['SHAP Value'].abs()
    shap_df = shap_df.sort_values('Abs_SHAP', ascending=True).tail(10)
    
    # Create waterfall-style bar chart
    colors = ['#e74c3c' if x > 0 else '#3498db' for x in shap_df['SHAP Value']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=shap_df['SHAP Value'],
            y=shap_df['Feature'],
            orientation='h',
            marker=dict(color=colors),
            text=[f"{abs(x):.3f}" for x in shap_df['SHAP Value']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Top 10 Features Driving This Prediction",
        xaxis_title="SHAP Value (Impact on Prediction)",
        yaxis_title="Feature",
        height=400,
        showlegend=False,
        template="plotly_white"
    )
    
    return fig


def plot_shap_bar_top_features(explainer, X_processed: np.ndarray, feature_names: List[str],
                              top_n: int = 10) -> go.Figure:
    """
    Create a bar chart showing top N features by average absolute SHAP value.
    
    Args:
        explainer: SHAP TreeExplainer
        X_processed: Preprocessed input data
        feature_names: List of feature names
        top_n: Number of top features to show
    
    Returns:
        Plotly figure
    """
    shap_values = explainer.shap_values(X_processed)
    
    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]  # Positive class
    else:
        shap_vals = shap_values[0]
    
    # Create feature importance DataFrame
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'SHAP Value': np.abs(shap_vals)
    }).sort_values('SHAP Value', ascending=False).head(top_n)
    
    fig = px.bar(
        feature_importance,
        x='SHAP Value',
        y='Feature',
        orientation='h',
        title=f"Top {top_n} Features by Importance",
        labels={'SHAP Value': 'Absolute SHAP Value'},
        color='SHAP Value',
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(height=400, showlegend=False, template="plotly_white")
    
    return fig


class CounterfactualExplainer:
    """
    Wrapper for DiCE-based counterfactual explanations.
    Generates suggestions to improve prediction outcomes.
    """
    
    def __init__(self, model, feature_names: List[str], feature_cols: List[str],
                 continuous_features: List[str], categorical_features: List[str]):
        """
        Initialize counterfactual explainer.
        
        Args:
            model: Trained XGBoost model
            feature_names: Preprocessed feature names
            feature_cols: Raw feature column names
            continuous_features: List of continuous feature names
            categorical_features: List of categorical feature names
        """
        self.model = model
        self.feature_names = feature_names
        self.feature_cols = feature_cols
        self.continuous_features = continuous_features
        self.categorical_features = categorical_features
    
    def generate_counterfactuals_simple(self, current_pred: float, 
                                       user_input: Dict[str, Any],
                                       preprocessor) -> List[Dict[str, Any]]:
        """
        Generate simplified counterfactual suggestions by iteratively changing features.
        
        Since full DiCE can be complex, this generates rule-based suggestions
        based on feature importance and logical domain knowledge.
        
        Args:
            current_pred: Current prediction probability
            user_input: Original user input dictionary
            preprocessor: ColumnTransformer for preprocessing
        
        Returns:
            List of counterfactual suggestions with explanations
        """
        suggestions = []
        
        # Define actionable features and their changes
        actionable_changes = [
            {
                'features': ['Parental_Approval'],
                'changes': {'Parental_Approval': 'Yes'},
                'description': 'Increase parental approval'
            },
            {
                'features': ['Spouse_Working'],
                'changes': {'Spouse_Working': 'Yes'},
                'description': 'Have both spouses working'
            },
            {
                'features': ['Income_Level'],
                'changes': {'Income_Level': 'High'},
                'description': 'Improve household income level'
            },
            {
                'features': ['Education_Level'],
                'changes': {'Education_Level': 'Postgraduate'},
                'description': 'Increase education level'
            },
            {
                'features': ['Caste_Match'],
                'changes': {'Caste_Match': 'Same'},
                'description': 'Increase caste compatibility'
            }
        ]
        
        # Test each suggestion
        for i, suggestion in enumerate(actionable_changes):
            if len(suggestions) >= 3:
                break
            
            # Create modified input
            modified_input = user_input.copy()
            for feature, value in suggestion['changes'].items():
                if feature in modified_input:
                    modified_input[feature] = value
            
            # Preprocess and predict
            try:
                modified_df = pd.DataFrame([modified_input])
                modified_processed = preprocessor.transform(modified_df)
                new_pred = self.model.predict_proba(modified_processed)[0][1]
                
                # Only suggest if it improves the prediction
                if new_pred > current_pred:
                    improvement = (new_pred - current_pred) * 100
                    suggestions.append({
                        'description': suggestion['description'],
                        'old_value': current_pred,
                        'new_value': new_pred,
                        'improvement': improvement,
                        'changes': suggestion['changes']
                    })
            except Exception as e:
                st.warning(f"Could not generate suggestion {i+1}: {str(e)}")
                continue
        
        return suggestions


def display_counterfactual_suggestions(suggestions: List[Dict[str, Any]]):
    """
    Display counterfactual suggestions in an attractive format.
    """
    if not suggestions:
        st.info("✓ No immediate improvements needed!")
        return
    
    st.subheader("💡 Ways to Improve Your Outcome")
    
    for i, suggestion in enumerate(suggestions, 1):
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **#{i}. {suggestion['description']}**
                
                **Current Success Rate:** {suggestion['old_value']*100:.1f}%  
                **Projected Success Rate:** {suggestion['new_value']*100:.1f}%  
                **Improvement:** +{suggestion['improvement']:.1f}%
                """)
            
            with col2:
                # Visual indicator
                improvement_pct = suggestion['improvement']
                if improvement_pct > 10:
                    st.success(f"⬆ +{improvement_pct:.1f}%")
                elif improvement_pct > 5:
                    st.info(f"⬆ +{improvement_pct:.1f}%")
                else:
                    st.warning(f"⬆ +{improvement_pct:.1f}%")
            
            st.divider()


def create_comparison_dataframe(suggestions: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a DataFrame for displaying counterfactual comparisons.
    """
    data = []
    for i, suggestion in enumerate(suggestions, 1):
        data.append({
            'Suggestion': f"#{i}: {suggestion['description']}",
            'Current Success %': f"{suggestion['old_value']*100:.1f}%",
            'Projected Success %': f"{suggestion['new_value']*100:.1f}%",
            'Improvement': f"+{suggestion['improvement']:.1f}%"
        })
    
    return pd.DataFrame(data)


def plot_satisfaction_distribution(model, predictions: np.ndarray, 
                                  label_encoder) -> go.Figure:
    """
    Plot satisfaction level predictions as a gauge or distribution.
    
    Args:
        model: Trained XGBoost multiclass model
        predictions: Raw model predictions
        label_encoder: LabelEncoder for class labels
    
    Returns:
        Plotly figure
    """
    classes = label_encoder.classes_
    fig = go.Figure(data=[
        go.Bar(
            x=classes,
            y=predictions[0],
            marker_color=['#e74c3c', '#f39c12', '#27ae60'],
            text=[f"{p*100:.1f}%" for p in predictions[0]],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Predicted Marital Satisfaction Distribution",
        xaxis_title="Satisfaction Level",
        yaxis_title="Probability",
        height=300,
        showlegend=False,
        template="plotly_white"
    )
    
    return fig


def create_success_gauge(success_prob: float, divorce_prob: float) -> go.Figure:
    """
    Create a gauge chart showing marriage success probability.
    
    Args:
        success_prob: Probability of marriage success (no divorce)
        divorce_prob: Probability of divorce
    
    Returns:
        Plotly gauge figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=success_prob * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Marriage Success Probability"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2c3e50"},
            'steps': [
                {'range': [0, 25], 'color': "#e74c3c"},
                {'range': [25, 50], 'color': "#e67e22"},
                {'range': [50, 75], 'color': "#f39c12"},
                {'range': [75, 100], 'color': "#27ae60"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=350)
    return fig
