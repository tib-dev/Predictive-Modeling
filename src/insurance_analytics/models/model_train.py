import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Dict, Any

from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, roc_auc_score, f1_score, precision_score, recall_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.compose import ColumnTransformer

# ---- Helpers ----
def auto_detect_column_types(df: pd.DataFrame, numeric_threshold: float = 0.9
                             ) -> Tuple[List[str], List[str]]:
    """
    Heuristic detection: if a column can be mostly coerced to numeric, treat as numeric.
    Returns (numeric_cols, categorical_cols).
    """
    numeric_cols, categorical_cols = [], []
    for c in df.columns:
        coerced = pd.to_numeric(df[c], errors='coerce')
        frac_numeric = coerced.notna().mean()
        # treat small-cardinality numeric-like as categorical (e.g., zipcode-like)
        if frac_numeric >= numeric_threshold and df[c].nunique() > 10:
            numeric_cols.append(c)
        else:
            categorical_cols.append(c)
    return numeric_cols, categorical_cols


def sanitize_numeric_columns(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    df = df.copy()
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df


def sanitize_categorical_columns(
    df: pd.DataFrame,
    categorical_cols: List[str],
    missing_token: str = "MISSING",
    null_like: Optional[List[str]] = None
) -> pd.DataFrame:
    df = df.copy()
    if null_like is None:
        null_like = ["nan", "NaN", "None", "NONE", "NA", "N/A", "", " "]

    for c in categorical_cols:
        if c not in df.columns:
            continue
        # replace common null-like strings with np.nan
        df[c] = df[c].replace(to_replace=null_like, value=np.nan)
        # strip whitespace for strings (safe even if mixed types)
        try:
            # convert to string only after handling NaN to avoid "nan" strings
            df[c] = df[c].where(df[c].notna(), other=np.nan)
            # For non-null values, convert to str and strip
            df.loc[df[c].notna(), c] = df.loc[df[c].notna(), c].astype(str).str.strip()
        except Exception:
            # fallback: cast entire column to str then strip (less ideal)
            df[c] = df[c].astype(str).str.strip()
            df[c] = df[c].replace(to_replace=null_like, value=np.nan)
        # fill missing with token and ensure uniform string dtype
        df[c] = df[c].fillna(missing_token).astype(str)
    return df


# ---- Main Trainer ----
class ModelTrainer:
    """
    Robust trainer for regression (severity) and classification (frequency).
    - Accepts a pre-built ColumnTransformer (self.preprocessor).
    - Sanitizes inputs to ensure encoders receive uniform types.
    - Optionally log-transforms regression targets (use target_transform='log').
    """

    def __init__(
        self,
        preprocessor: ColumnTransformer,
        numeric_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None,
        target_transform: Optional[str] = None,
    ):
        """
        :param preprocessor: ColumnTransformer that expects numeric & categorical arrays.
        :param numeric_cols: Optional list of numeric column names. If None, auto-detection is used.
        :param categorical_cols: Optional list of categorical column names. If None, auto-detection is used.
        :param target_transform: 'log' to apply np.log1p to regression y during fit; None otherwise.
        """
        self.preprocessor = preprocessor
        self.models: Dict[str, Pipeline] = {}
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self.target_transform = target_transform

    # ------------------------
    # Internal helpers
    # ------------------------
    def _prepare_X(self, X: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            # attempt to convert; ColumnTransformer often requires DataFrame for column names
            X = pd.DataFrame(X)

        # detect types if not provided explicitly
        if self.numeric_cols is None or self.categorical_cols is None:
            detected_num, detected_cat = auto_detect_column_types(X)
            numeric_cols = detected_num if self.numeric_cols is None else self.numeric_cols
            categorical_cols = detected_cat if self.categorical_cols is None else self.categorical_cols
        else:
            numeric_cols = self.numeric_cols
            categorical_cols = self.categorical_cols

        Xc = sanitize_numeric_columns(X, numeric_cols)
        Xc = sanitize_categorical_columns(Xc, categorical_cols)
        return Xc

    def _safe_target_transform(self, y: pd.Series, inverse: bool = False) -> pd.Series:
        if self.target_transform == "log":
            if inverse:
                # inverse: expm1
                return np.expm1(y)
            else:
                # forward: log1p
                return np.log1p(y)
        return y

    def _safe_predict_proba_values(self, model: Pipeline, X: pd.DataFrame) -> np.ndarray:
        """
        Return probability for positive class. If predict_proba unavailable, try decision_function,
        otherwise return predicted labels (not ideal but prevents crash).
        """
        try:
            probs = model.predict_proba(X)
            if probs.ndim == 2 and probs.shape[1] >= 2:
                return probs[:, 1]
            # if single-column probability returned (like for some libs), return it
            if probs.ndim == 1:
                return probs
        except Exception:
            pass

        # fallback: try decision_function
        try:
            df = model.decision_function(X)
            # scale to 0-1 using logistic in case it's raw scores
            probs = 1 / (1 + np.exp(-df))
            return probs
        except Exception:
            pass

        # last fallback: predicted labels
        try:
            preds = model.predict(X)
            return preds.astype(float)
        except Exception:
            # return zeros to avoid crash; caller should handle suspicious metrics
            return np.zeros(len(X), dtype=float)

    # ------------------------
    # Training / Evaluation APIs
    # ------------------------
    def train_regression_models(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Trains LinearRegression, RandomForestRegressor, XGBRegressor.
        If target_transform == 'log', y_train is transformed internally.
        """
        X_train_safe = self._prepare_X(X_train)
        y_train_safe = self._safe_target_transform(y_train, inverse=False)

        model_defs: Dict[str, Any] = {
            "Linear_Regression": LinearRegression(),
            "RandomForest_Regressor": RandomForestRegressor(random_state=42, n_jobs=-1, max_depth=10),
            "XGBoost_Regressor": XGBRegressor(random_state=42, n_jobs=-1, objective="reg:squarederror"),
        }

        for name, model in model_defs.items():
            pipeline = Pipeline(steps=[("preprocessor", self.preprocessor), ("model", model)])
            print(f"[train_regression] fitting {name} ...")
            pipeline.fit(X_train_safe, y_train_safe)
            self.models[name] = pipeline
        print("[train_regression] done. Models:", list(self.models.keys()))

    def evaluate_regression(self, X_test: pd.DataFrame, y_test_orig: pd.Series) -> pd.DataFrame:
        """
        Evaluate trained regression models. If target_transform == 'log' predictions are inverse-transformed
        before metric calculation.
        """
        X_test_safe = self._prepare_X(X_test)
        metrics = []
        for name, model in self.models.items():
            try:
                y_pred_model = model.predict(X_test_safe)
            except Exception as e:
                print(f"[evaluate_regression] model {name} predict failed: {e}")
                continue

            # If model was trained on transformed y, reverse it
            if self.target_transform == "log":
                # predictions are on log scale -> inverse transform with expm1
                y_pred_orig = np.expm1(y_pred_model)
            else:
                y_pred_orig = y_pred_model

            # safety: coerce to numeric arrays
            y_true = np.asarray(y_test_orig, dtype=float)
            y_pred_orig = np.asarray(y_pred_orig, dtype=float)

            # compute metrics
            mse = mean_squared_error(y_true, y_pred_orig)
            rmse = float(np.sqrt(mse))
            r2 = float(r2_score(y_true, y_pred_orig))

            metrics.append({"Model": name, "RMSE (Original Scale)": rmse, "R-squared": r2})
        return pd.DataFrame(metrics).sort_values(by="RMSE (Original Scale)")

    def train_classification_models(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Trains LogisticRegression, RandomForestClassifier, XGBClassifier.
        """
        X_train_safe = self._prepare_X(X_train)
        y_train_safe = y_train  # assume categorical labels already encoded 0/1

        model_defs: Dict[str, Any] = {
            "Logistic_Regression": LogisticRegression(random_state=42, solver="liblinear"),
            "RandomForest_Classifier": RandomForestClassifier(random_state=42, n_jobs=-1, max_depth=10),
            "XGBoost_Classifier": XGBClassifier(random_state=42, n_jobs=-1, use_label_encoder=False, eval_metric="logloss"),
        }

        for name, model in model_defs.items():
            pipeline = Pipeline(steps=[("preprocessor", self.preprocessor), ("model", model)])
            print(f"[train_classification] fitting {name} ...")
            pipeline.fit(X_train_safe, y_train_safe)
            self.models[name] = pipeline
        print("[train_classification] done. Models:", list(self.models.keys()))

    def evaluate_classification(self, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
        """
        Evaluate classification models using AUC-ROC, Precision, Recall, F1.
        Uses predict_proba when available; falls back to sensible alternatives.
        """
        X_test_safe = self._prepare_X(X_test)
        metrics = []
        for name, model in self.models.items():
            try:
                y_proba = self._safe_predict_proba_values(model, X_test_safe)
                y_pred = model.predict(X_test_safe)
            except Exception as e:
                print(f"[evaluate_classification] model {name} predict failed: {e}")
                continue

            # Ensure arrays numeric
            y_proba = np.asarray(y_proba, dtype=float)
            y_pred = np.asarray(y_pred, dtype=int)
            y_true = np.asarray(y_test, dtype=int)

            # Compute metrics carefully: guard invalid cases
            try:
                auc_roc = float(roc_auc_score(y_true, y_proba))
            except Exception:
                auc_roc = float("nan")
            try:
                precision = float(precision_score(y_true, y_pred))
            except Exception:
                precision = float("nan")
            try:
                recall = float(recall_score(y_true, y_pred))
            except Exception:
                recall = float("nan")
            try:
                f1 = float(f1_score(y_true, y_pred))
            except Exception:
                f1 = float("nan")

            metrics.append({
                "Model": name,
                "AUC-ROC": auc_roc,
                "F1-Score": f1,
                "Precision": precision,
                "Recall": recall
            })

        return pd.DataFrame(metrics).sort_values(by="AUC-ROC", ascending=False)
