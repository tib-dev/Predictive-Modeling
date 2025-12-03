#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "---------------------------------------------"
echo "  Initializing Insurance Risk Analytics Project"
echo "---------------------------------------------"
echo ""

GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

created_dirs=()
created_files=()

# ----------------------------------------
# Helpers
# ----------------------------------------
ensure_dir () {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        touch "$1/.gitkeep"
        created_dirs+=("$1")
        echo -e "${GREEN}Created directory:${RESET} $1"
    else
        echo -e "${CYAN}Directory exists:${RESET} $1"
    fi
}

ensure_file () {
    if [ ! -f "$1" ]; then
        mkdir -p "$(dirname "$1")"
        touch "$1"
        created_files+=("$1")
        echo -e "${GREEN}Created file:${RESET} $1"
    else
        echo -e "${CYAN}File exists:${RESET} $1"
    fi
}

# ----------------------------------------
# DIRECTORIES
# ----------------------------------------
dirs=(
    ".github/workflows"
    "configs"
    "data/raw"
    "data/interim"
    "data/processed"
    "docs"
    "notebooks/eda"
    "notebooks/modeling"
    "scripts"
    "src/insurance_analytics"
    "src/insurance_analytics/data"
    "src/insurance_analytics/preprocessing"
    "src/insurance_analytics/eda"
    "src/insurance_analytics/models"
    "src/insurance_analytics/viz"
    "src/insurance_analytics/utils"
    "tests/unit"
    "tests/integration"
)

for d in "${dirs[@]}"; do
    ensure_dir "$d"
done

# ----------------------------------------
# FILES
# ----------------------------------------
files=(
    ".github/workflows/ci.yml"
    ".github/workflows/codeql.yml"

    "configs/data.yaml"
    "configs/modeling.yaml"

    "docs/README_project_overview.md"
    "docs/EDA_report_template.md"
    "docs/Modeling_report_template.md"

    "scripts/run_eda.sh"
    "scripts/run_modeling.sh"

    "src/insurance_analytics/__init__.py"
    "src/insurance_analytics/config.py"

    "src/insurance_analytics/data/__init__.py"
    "src/insurance_analytics/data/load_data.py"
    "src/insurance_analytics/data/versioning.py"

    "src/insurance_analytics/preprocessing/__init__.py"
    "src/insurance_analytics/preprocessing/cleaner.py"
    "src/insurance_analytics/preprocessing/feature_engineering.py"

    "src/insurance_analytics/eda/__init__.py"
    "src/insurance_analytics/eda/exploration.py"
    "src/insurance_analytics/eda/visualization.py"

    "src/insurance_analytics/models/__init__.py"
    "src/insurance_analytics/models/linear_regression.py"
    "src/insurance_analytics/models/random_forest.py"
    "src/insurance_analytics/models/xgboost_model.py"
    "src/insurance_analytics/models/evaluation.py"
    "src/insurance_analytics/models/interpretability.py"

    "src/insurance_analytics/viz/__init__.py"
    "src/insurance_analytics/viz/plots.py"

    "src/insurance_analytics/utils/__init__.py"
    "src/insurance_analytics/utils/helpers.py"
    "src/insurance_analytics/utils/io_utils.py"

    "tests/unit/test_cleaner.py"
    "tests/unit/test_feature_engineering.py"
    "tests/unit/test_load_data.py"
    "tests/unit/test_models.py"

    "tests/integration/test_eda_pipeline.py"
    "tests/integration/test_model_pipeline.py"

    "requirements.txt"
    "requirements-dev.txt"
    "pyproject.toml"
    "README.md"
    ".gitignore"
)

for f in "${files[@]}"; do
    ensure_file "$f"
done

echo ""
echo -e "${GREEN}Project structure for Insurance Risk Analytics initialized successfully.${RESET}"
echo ""

# Summary
echo "---------------------------------------------"
echo -e "${YELLOW}Summary${RESET}"
echo "---------------------------------------------"
echo "Directories created: ${#created_dirs[@]}"
echo "Files created: ${#created_files[@]}"

if (( ${#created_dirs[@]} > 0 )); then
    echo ""
    echo "New directories:"
    for d in "${created_dirs[@]}"; do
        echo " - $d"
    done
fi

if (( ${#created_files[@]} > 0 )); then
    echo ""
    echo "New files:"
    for f in "${created_files[@]}"; do
        echo " - $f"
    done
fi

echo ""
echo -e "${GREEN}All done.${RESET}"
