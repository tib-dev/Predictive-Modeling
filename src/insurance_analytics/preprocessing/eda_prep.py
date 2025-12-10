import pandas as pd
import numpy as np


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")


class DataPreprocessor:
    """
    Handles critical data cleaning, type correction, missing value imputation,
    and feature creation necessary for robust EDA and modeling.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    def _clean_financial_data(self) -> pd.DataFrame:
        """
        Converts financial columns to numeric, handling errors and non-standard
        values like currency symbols.
        """
        financial_cols = ['TotalPremium', 'TotalClaims', 'CustomValueEstimate']
        
        for col in financial_cols:
            # Coerce non-numeric values to NaN
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Note: Negative values in Claims (salvage/recovery) and Premium (refunds) 
        # are valid in insurance data and are retained for accurate profitability analysis.
        
        return self.df
    
    def _correct_data_types(self) -> pd.DataFrame:
        """
        Corrects dtypes for date, discrete count, and flag columns.
        """
        # 1. Date Conversion
        if 'TransactionMonth' in self.df.columns:
            self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'], errors='coerce')
        if 'VehicleIntroDate' in self.df.columns:
            self.df['VehicleIntroDate'] = pd.to_datetime(self.df['VehicleIntroDate'], errors='coerce')

        # 2. Discrete Count Conversion
        discrete_cols = ['Cylinders', 'NumberOfDoors']
        for col in discrete_cols:
            if col in self.df.columns:
                # Convert to integer, using -1 as a temporary placeholder for NaNs
                self.df[col] = self.df[col].fillna(-1).astype(int)
                # Convert to categorical to prevent model from treating them as continuous
                self.df[col] = self.df[col].astype('category')

        # 3. Categorical Conversion
        category_cols = ['Province', 'VehicleType', 'Gender', 'MaritalStatus']
        for col in category_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype('category')
        
        return self.df
    
        # NUMERIC CONVERSION FIX: Re-coerce all financial/age columns to numeric 
        # to prevent them from being mistaken for high-cardinality strings later.
        numeric_cols_to_check = ['TotalPremium', 'TotalClaims', 'CustomValueEstimate', 
                                 'CapitalOutstanding', 'SumInsured', 'CalculatedPremiumPerTerm']
        
        for col in numeric_cols_to_check:
             if col in self.df.columns:
                # Use to_numeric to force type conversion, coercing any remaining strings to NaN
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        return self.df
      
    def _handle_missing_values(self) -> pd.DataFrame:
        """
        Imputes missing values based on column type and domain knowledge.
        Note: This method assumes _correct_data_types() has already been run.
        """
        # 1. Financial/Claim Columns: Impute TotalClaims/TotalPremium NaNs with 0
        self.df[['TotalClaims', 'TotalPremium']] = self.df[['TotalClaims', 'TotalPremium']].fillna(0)

        # 2. Flag Columns (Missingness Implies 'No'): Impute NaNs with False
        flag_cols = ['WrittenOff', 'Rebuilt', 'Converted', 'CrossBorder', 'NewVehicle', 'AlarmImmobiliser']
        for col in flag_cols:
            if col in self.df.columns:
                # Use map for safer bool conversion without downcasting warnings
                self.df[col] = self.df[col].fillna('No').map({'Yes': True, 'No': False}).astype(bool)

        # 3. Critical Categorical Columns: Ensure categorical dtype, then impute with 'MISSING'
        critical_cat_cols = ['Province', 'Gender', 'MaritalStatus', 'PostalCode']  
        for col in critical_cat_cols:
            if col in self.df.columns:
                if not pd.api.types.is_categorical_dtype(self.df[col]):
                    self.df[col] = self.df[col].astype('category')
                self.df[col] = self.df[col].cat.add_categories('MISSING').fillna('MISSING')

        # 4. CustomValueEstimate (High Missing Rate)
        if 'CustomValueEstimate' in self.df.columns:
            self.df['ValueEstimate_MISSING'] = self.df['CustomValueEstimate'].isnull()
            median_val = self.df['CustomValueEstimate'].median()
            self.df['CustomValueEstimate'] = self.df['CustomValueEstimate'].fillna(median_val)

        # 5. NumberOfVehiclesInFleet (100% missing — likely individual policies)
        if 'NumberOfVehiclesInFleet' in self.df.columns:
            # Assume 1 for individuals; create fleet indicator
            self.df['IsFleetPolicy'] = self.df['NumberOfVehiclesInFleet'].notna()
            self.df['NumberOfVehiclesInFleet'] = self.df['NumberOfVehiclesInFleet'].fillna(1).astype(int)

        return self.df
    
    
    def _handle_high_cardinality(self, threshold: int = 100) -> pd.DataFrame:
        """
        Reduces the cardinality of ONLY CATEGORICAL features by grouping rare categories 
        into an 'Other' bucket. (Recommended approach over dropping).
        """
        # Target ONLY object columns, excluding any that contain critical numeric data
        # 'ZipCode' or 'PostalCode' (if it's the ID), and 'Model' are the typical culprits.
        categorical_cols_to_group = []
        for col in self.df.select_dtypes(include='object').columns:
            # We assume any remaining object column is a valid string/categorical feature
            if self.df[col].nunique() > threshold:
                categorical_cols_to_group.append(col)

        if not categorical_cols_to_group:
            print("No high-cardinality object columns found for grouping.")
            return self.df

        print(f"Grouping high-cardinality columns ({len(categorical_cols_to_group)}): {categorical_cols_to_group}")
        
        for col in categorical_cols_to_group:
            value_counts = self.df[col].value_counts()
            
            # Identify categories to keep (must appear >= threshold times)
            to_keep = value_counts[value_counts >= threshold].index
            
            # Replace rare categories with 'Other_Category'
            self.df[col] = np.where(
                self.df[col].isin(to_keep),
                self.df[col],
                'Other_Category'
            )
            print(f"  -> Cardinality of '{col}' reduced from {len(value_counts)} to {len(to_keep) + 1} categories.")
                
        return self.df
    
          
    def _create_eda_features(self) -> pd.DataFrame:
        """
        Creates essential features for EDA and Loss Ratio calculation.
        """
        # 1. Claim Indicator (for Claim Frequency)
        # 1 if TotalClaims > 0, else 0
        self.df['HasClaim'] = np.where(self.df['TotalClaims'] > 0, 1, 0)
        
        # 2. Vehicle Age (for risk modeling later)
        if 'VehicleIntroDate' in self.df.columns and 'TransactionMonth' in self.df.columns:
            # Calculate age in years
            self.df['VehicleAge_Years'] = (self.df['TransactionMonth'] - self.df['VehicleIntroDate']).dt.days / 365.25
            
        return self.df
    

         
    def run_pipeline(self) -> pd.DataFrame:
        """Executes all preprocessing steps in sequence."""
        print("Starting Data Preprocessing...")
        self.df = self._clean_financial_data()
        self.df = self._correct_data_types()
        self.df = self._handle_missing_values()
        # Apply SAFE cardinality reduction to remaining categorical columns
        self.df = self._handle_high_cardinality(threshold=100)
        self.df = self._create_eda_features()
        print("Preprocessing Complete.")
        return self.df
    