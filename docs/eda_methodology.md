EDA & Statistical Analysis of Insurance Data

Description:
This PR includes the initial exploratory data analysis (EDA) and foundational statistics for the insurance dataset. The goal is to understand data quality, distributions, and relationships between key variables such as TotalPremium, TotalClaims, and LossRatio.

Changes Made:

Data Cleaning Pipeline:

Trimmed and normalized string columns
Converted date columns with coercion
Converted numeric-like columns to proper numeric types
Renamed columns to readable snake_case, preserving acronyms (IsVATRegistered → is_vat_registered)
Dropped columns with >85% missing values
Summarized missing data

Univariate Analysis:

Histograms for numeric variables (TotalPremium, TotalClaims, LossRatio)
Bar charts for categorical variables (Province, VehicleType, Gender)
Boxplots for numeric columns to detect outliers

Bivariate / Multivariate Analysis:

Correlation matrix for numeric features
Scatter plots of TotalClaims vs TotalPremium by VehicleType
Boxplots of TotalClaims by Province and Gender
Pairplots for selected numeric columns

Feature Engineering:

Calculated LossRatio = TotalClaims / TotalPremium for analysis
Added insights for high-risk and low-risk vehicle types

Visualization & Insights:

Average LossRatio by Province (bar chart)
Distribution of LossRatio (histogram + KDE)
TotalClaims vs TotalPremium colored by VehicleType (scatter plot)

Next Steps / Recommendations:

Explore temporal trends in claims over 18 months
Investigate claim frequency and severity changes by VehicleMake/Model
Conduct deeper statistical tests for actionable insights

Files Added / Updated:

src/insurance_analytics/data/cleaner.py → Full cleaning pipeline
src/insurance_analytics/data/load_data.py → Chunked CSV loading
src/insurance_analytics/eda/exploration.py → Structural summary, univariate & bivariate analysis
src/insurance_analytics/viz/plots.py → Visualization functions for EDA

Testing:

Functions tested on sample CSV
Missing data, outliers, and data types verified