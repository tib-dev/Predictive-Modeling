# Insurance Risk Analytics & Predictive Modeling — ACIS Project

Analyze historical car insurance data from AlphaCare Insurance Solutions (ACIS) in South Africa to uncover low-risk segments, optimize premiums, and support data-driven marketing strategies.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Objective](#business-objective)
- [Dataset Overview](#dataset-overview)
- [Folder Structure](#folder-structure)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Tasks Completed](#tasks-completed)
- [Technologies Used](#technologies-used)
- [Key Insights](#key-insights)

---

## Project Overview

This project covers end-to-end insurance risk analytics and predictive modeling:

- Understanding historical insurance policies, claims, and premiums
- Exploratory Data Analysis (EDA) to identify patterns and outliers
- Statistical hypothesis testing to validate risk drivers
- Feature engineering and data preprocessing
- Predictive modeling for:
  - Claim severity
  - Premium optimization
  - Probability of claim occurrence
- Visualization and reporting of insights for business strategy

---

## Business Objective

AlphaCare Insurance Solutions aims to:

- Identify low-risk segments for targeted marketing
- Optimize premiums to attract new clients while maintaining profitability
- Understand key factors driving claims and losses
- Support strategic decisions for product design and pricing

---

## Dataset Overview

**Historical Insurance Data (Feb 2014 – Aug 2015):**

| Column                | Description                                      |
| --------------------- | ------------------------------------------------ |
| PolicyID              | Unique insurance policy ID                       |
| TransactionMonth      | Month of policy transaction                      |
| Gender, MaritalStatus | Client demographics                              |
| Province, PostalCode   | Client location                                  |
| VehicleType, Make, Model | Vehicle details                                |
| TotalPremium           | Premium paid                                     |
| TotalClaims            | Claim amount                                     |
| CalculatedPremiumPerTerm | Premium per term                               |
| SumInsured             | Coverage amount                                  |
| CoverType, Product     | Insurance plan details                            |

- Includes policy, client, location, vehicle, plan, payment, and claim data
- Data stored as CSV files for reproducibility

---

## Folder Structure

```text
Insurance-Risk-Analytics/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── codeql.yml
├── configs/
│   ├── data.yaml
│   └── modeling.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── README_project_overview.md
│   ├── EDA_report_template.md
│   └── Modeling_report_template.md
├── notebooks/
│   ├── eda/
│   └── modeling/
├── scripts/
│   ├── run_eda.sh
│   └── run_modeling.sh
├── src/insurance_analytics/
│   ├── __init__.py
│   ├── config.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   └── versioning.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── feature_engineering.py
│   ├── eda/
│   │   ├── __init__.py
│   │   ├── exploration.py
│   │   └── visualization.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── linear_regression.py
│   │   ├── random_forest.py
│   │   ├── xgboost_model.py
│   │   ├── evaluation.py
│   │   └── interpretability.py
│   ├── viz/
│   │   ├── __init__.py
│   │   └── plots.py
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── io_utils.py
├── tests/unit/
│   ├── test_cleaner.py
│   ├── test_feature_engineering.py
│   ├── test_load_data.py
│   └── test_models.py
├── tests/integration/
│   ├── test_eda_pipeline.py
│   └── test_model_pipeline.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── README.md
├── .env
└── .gitignore
