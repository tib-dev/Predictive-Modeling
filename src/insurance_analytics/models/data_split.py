import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

class ModelingDataPrep:
    """
    Handles data splitting and defines the preprocessing steps (Scaling/OHE) 
    for both Claim Severity and Claim Frequency modeling tasks.
    """

    def __init__(self, df: pd.DataFrame):
        # Drop ID and date columns that are not directly used as features
        self.df = df.drop(columns=['PolicyID', 'TransactionMonth', 'VehicleIntroDate'], errors='ignore')
        
        # Convert non-numeric types to 'object' to ensure they are handled by the OneHotEncoder later, not the StandardScaler.
        for col in self.df.columns:
            if self.df[col].dtype != np.number:
                self.df[col] = self.df[col].astype('object')
        
        #  DEFINE A MASTER FEATURE LIST (All non-target columns)
        # We explicitly exclude all targets and target-related metrics here.
        self.TARGET_COLS = ['HasClaim', 'TotalClaims'] 
        self.FEATURE_COLS = [col for col in self.df.columns if col not in self.TARGET_COLS]        

    def get_preprocessor(self, X_train: pd.DataFrame) -> ColumnTransformer:
        """
        Defines the column transformer (preprocessing steps) needed for the modeling pipeline.
        This handles both numerical scaling and categorical encoding simultaneously.
        """
        
        # Identify feature types
        numerical_features = X_train.select_dtypes(exclude='object').columns.tolist()
        categorical_features = X_train.select_dtypes(include='object').columns.tolist()
        # Define preprocessing steps:
        preprocessor = ColumnTransformer(
            transformers=[
                # 1. Scaling for numerical features
                ('num', StandardScaler(), numerical_features),
                # 2. One-Hot Encoding for categorical features
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=True), categorical_features)
            ],
            remainder='passthrough'
        )
        return preprocessor

    def create_severity_split(self) -> tuple:
        """
        Creates the train/test split for Claim Severity (Regression). 
        Critical: Filters data to claims > 0 and log-transforms the target.
        """
        
        # Filter data to ONLY policies that had a claim (TotalClaims > 0)
        severity_df = self.df[self.df['HasClaim'] == 1].copy()
        
        # Explicitly ensure TotalClaims is a numeric type just before the calculation to resolve the TypeError.
        severity_df['TotalClaims'] = pd.to_numeric(severity_df['TotalClaims'], errors='coerce')
        # Handle any remaining NaNs that might have resulted from 'coerce' by filling with 0
        severity_df['TotalClaims'] = severity_df['TotalClaims'].fillna(0)
        
        # Log-transform the target to normalize its highly skewed distribution
        severity_df['LogTotalClaims'] = np.log1p(severity_df['TotalClaims'])
        
        
        # Use the MASTER feature list for X
        # Define features (X) and log-transformed target (y)
        X = severity_df[self.FEATURE_COLS].copy()
        y = severity_df['LogTotalClaims']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        print(f"Severity Model Data Split: Training policies={len(X_train)}, Testing policies={len(X_test)}")
        return X_train, X_test, y_train, y_test

    def create_frequency_split(self) -> tuple:
        """
        Creates the train/test split for Claim Frequency (Classification). 
        Target is HasClaim (0/1). Uses the full dataset.
        """
        
        # Use the MASTER feature list for X
        X = self.df[self.FEATURE_COLS].copy()
        y = self.df['HasClaim'].astype('int8') # Force target to integer type
        # Use stratify=y to ensure the rare 'HasClaim=1' instances are split proportionally
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
        print(f"Frequency Model Data Split: Training policies={len(X_train)}, Testing policies={len(X_test)}")
        return X_train, X_test, y_train, y_test