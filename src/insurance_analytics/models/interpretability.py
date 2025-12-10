import pandas as pd
import numpy as np
import shap
from sklearn.pipeline import Pipeline
import warnings
# Suppress warnings from SHAP and model evaluation for cleaner output
warnings.filterwarnings('ignore') 

class ModelInterpreter:
    """
    Performs SHAP (SHapley Additive exPlanations) analysis on the best performing model 
    to provide actionable business insights into risk drivers.
    """

    def __init__(self, best_model: Pipeline, X_test: pd.DataFrame):
        self.best_model = best_model
        self.X_test = X_test
        
        # 1. Get the preprocessor object and transform test data
        self.preprocessor = best_model.named_steps['preprocessor']
        self.X_test_preprocessed = self.preprocessor.transform(X_test)

        # 2. Get feature names after One-Hot Encoding (OHE)
        # This is necessary because SHAP requires feature names matching the transformed data
        try:
            # For modern Scikit-learn (often works for simple cases)
            self.feature_names = self.preprocessor.get_feature_names_out()
        except AttributeError:
            # Fallback for older versions or complex pipelines
            numerical_cols = X_test.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = X_test.select_dtypes(include='object').columns.tolist()
            
            # Combine numerical features and OHE feature names
            cat_features_out = self.preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
            self.feature_names = numerical_cols + list(cat_features_out)

    def run_shap_analysis(self, num_features: int = 10):
        """
        Calculates SHAP values for the test set and generates the interpretation plots.
        """
        
        # 3. Extract the trained model (e.g., XGBoost, RandomForest) from the pipeline
        model = self.best_model.named_steps['model']
        
        # 4. Create SHAP Explainer (TreeExplainer is fastest for tree-based models)
        explainer = shap.TreeExplainer(model)
        
        # 5. Calculate SHAP values
        shap_values = explainer.shap_values(self.X_test_preprocessed)
        
        print("\n--- SHAP Feature Importance Analysis ---")


        print("Visualizations will appear below, showing the top 10 features' impact on risk prediction.")
        
        # === Visualization 1: Overall Feature Importance (Bar Plot) ===
        # Shows the average magnitude of influence for each feature
        print("\n")
        shap.summary_plot(shap_values, features=self.X_test_preprocessed, feature_names=self.feature_names, max_display=num_features, plot_type="bar")

        # === Visualization 2: Directional Impact (Dot Plot) ===
        # Shows how high/low feature values increase/decrease the prediction (e.g., older cars -> higher predicted claim)
        print("\n")
        shap.summary_plot(shap_values, features=self.X_test_preprocessed, feature_names=self.feature_names, max_display=num_features)
        
        return self.feature_names # Return names for use in final business report
    