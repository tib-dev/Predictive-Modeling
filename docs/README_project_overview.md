Task 1: Git, EDA & Project Setup

Objective: Understand the data, create project structure, and perform exploratory data analysis.

Pipeline Steps:

Project Initialization

Initialize Git repository.

Create branch task-1.

Set up folder structure with init-setup.sh.

Add .gitignore, README.md, and basic requirements.txt.

Data Understanding

Load raw data using src/insurance_analytics/data/load_data.py.

Inspect columns: data types, null values, unique counts.

Identify numeric vs categorical features.

Data Quality Assessment

Check for missing values, duplicates, and inconsistent entries.

Generate a summary table of missing data percentage per column.

Exploratory Data Analysis (EDA)

Univariate analysis: Histograms for numeric features (TotalClaims, TotalPremium), bar charts for categorical (Province, VehicleType, Gender).

Bivariate analysis: Scatter plots, correlation heatmaps (TotalClaims vs TotalPremium, Claim Frequency vs Province/ZipCode).

Temporal trends: Line plots over 18 months to identify seasonal patterns.

Outlier detection: Boxplots on TotalClaims, CustomValueEstimate.

Visualization & Insights

Produce at least 3 creative plots highlighting key insights (loss ratio by Province, vehicle type, gender).

Save outputs in data/processed/eda_outputs.

Commit & Merge

Push code to task-1 branch, then merge to main after review.

Task 2: Data Version Control (DVC)

Objective: Ensure reproducibility, auditable pipelines for raw and processed data.

Pipeline Steps:

DVC Setup

Install DVC: pip install dvc.

Initialize DVC in project: dvc init.

Configure local remote storage: dvc remote add -d localstorage /path/to/storage.

Data Tracking

Move raw dataset to data/raw/.

Track dataset with dvc add data/raw/insurance_data.csv.

Commit .dvc files to Git.

Versioning

Create processed datasets during EDA and preprocessing.

Track processed datasets with DVC (dvc add data/processed/...).

Push data to local remote: dvc push.

Reproducibility

Ensure that src/insurance_analytics/data/versioning.py can pull datasets from DVC.

Commit & Merge

Push task-2 branch changes and merge to main.

Task 3: A/B Hypothesis Testing

Objective: Statistically validate differences in risk across provinces, zip codes, and gender.

Pipeline Steps:

Select Metrics

Claim Frequency: Proportion of policies with ≥1 claim.

Claim Severity: Average claim amount given a claim.

Margin: TotalPremium − TotalClaims.

Data Segmentation

For each hypothesis:

H₀: No risk difference across Provinces → Group by Province.

H₀: No risk difference across ZipCodes → Group by ZipCode.

H₀: No risk difference across Gender → Group by Gender.

Statistical Testing

Categorical outcomes: Chi-squared test for claim frequency.

Continuous outcomes: t-test or ANOVA for claim severity and margins.

Compute p-values to accept/reject null hypotheses.

Interpretation & Reporting

Document which hypotheses are rejected (p < 0.05).

Generate visualizations:

Boxplots for claim severity by Province.

Heatmaps for margins by ZipCode.

Save outputs to data/processed/stat_tests/.

Business Recommendations

Identify regions or client segments with higher/lower risk.

Suggest premium adjustments or targeted marketing.

Task 4: Predictive Modeling

Objective: Build risk-based pricing models for claims and premiums.

Pipeline Steps:

Data Preparation

Impute missing values (numeric → median, categorical → mode).

Feature engineering:

Vehicle age, policy age, claims history, coverage ratios.

Encode categorical variables using one-hot or label encoding.

Split data:

Claim Severity Model: Only policies with TotalClaims > 0.

Premium Optimization Model: All policies.

Train/Test split (70/30 or 80/20).

Model Building

Linear Regression (baseline)

Random Forest Regressor

XGBoost Regressor

Optional: Logistic Regression or Classification for probability of claim.

Model Evaluation

Metrics for regression: RMSE, R².

Metrics for classification (if probability model used): Accuracy, AUC, F1-score.

Compare model performances.

Model Interpretability

SHAP or LIME to analyze feature importance.

Identify top 5–10 features influencing claims and premiums.

Example insight: “Vehicle age increases predicted claim by X Rand per year.”

Report & Recommendations

Visualize predicted vs actual claims.

Visualize risk-based premium distributions.

Store models in models/ and results in data/processed/models/.

Provide actionable insights for marketing and premium adjustment.

Commit & Merge

Push task-4 branch and merge to main.