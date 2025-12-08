import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")


def claim_frequency(df: pd.DataFrame) -> pd.Series:
    """
    Compute claim frequency flag per policy.
    Returns a Series of 0/1 integers (1 = at least one claim).
    """
    _require_columns(df, ["TotalClaims"])
    # Treat missing TotalClaims as 0 (no claim) unless you prefer to keep NaN
    freq = (df["TotalClaims"].fillna(0) > 0).astype(int)
    freq.name = "ClaimFrequency"
    return freq


def claim_severity(df: pd.DataFrame, keep_na: bool = True) -> pd.Series:
    """
    Compute claim severity per policy *conditional on having a claim*.
    For rows where TotalClaims <= 0 or is NaN:
      - if keep_na=True -> return NaN
      - if keep_na=False -> return 0

    Returned Series aligns with df.index.
    """
    _require_columns(df, ["TotalClaims"])
    total_claims = df["TotalClaims"]
    # Create series filled with NaN then set positive claims
    severity = pd.Series(np.nan, index=df.index, name="ClaimSeverity")
    positive_mask = total_claims.notna() & (total_claims > 0)
    severity.loc[positive_mask] = total_claims.loc[positive_mask].astype(float)
    if not keep_na:
        severity = severity.fillna(0.0)
    return severity


def margin(df: pd.DataFrame, fillna: Optional[float] = None) -> pd.Series:
    """
    Compute margin = TotalPremium - TotalClaims.

    Parameters:
    - fillna: if not None, fill missing TotalPremium/TotalClaims with this value
              before computing margin. If None, preserve NaNs.

    Returns a Series aligned to df.index named 'Margin'.
    """
    _require_columns(df, ["TotalPremium", "TotalClaims"])
    if fillna is not None:
        tp = df["TotalPremium"].fillna(fillna)
        tc = df["TotalClaims"].fillna(fillna)
    else:
        tp = df["TotalPremium"]
        tc = df["TotalClaims"]
    m = tp - tc
    m.name = "Margin"
    return m


def margin_rate(df: pd.DataFrame, eps: float = 1e-9) -> pd.Series:
    """
    Compute margin rate = Margin / TotalPremium.
    If TotalPremium is zero or NaN, result is NaN.

    eps: small number to avoid division-by-zero; zeros are treated as NaN.
    """
    _require_columns(df, ["TotalPremium", "TotalClaims"])
    tp = df["TotalPremium"]
    m = margin(df)
    # treat too-small premiums as NaN to avoid huge/inf rates
    safe_tp = tp.where(tp.abs() > eps)
    rate = m / safe_tp
    rate.name = "MarginRate"
    return rate


def attach_metrics(
    df: pd.DataFrame,
    *,
    keep_severity_na: bool = True,
    fillna_for_margin: Optional[float] = None,
    include_margin_rate: bool = True,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Attach ClaimFrequency, ClaimSeverity, Margin (and optional MarginRate) to df.

    Parameters:
    - keep_severity_na: if True, ClaimSeverity is NaN for non-claim rows; otherwise 0.
    - fillna_for_margin: if not None, fill missing TotalPremium/TotalClaims with this value before computing Margin.
    - include_margin_rate: whether to compute MarginRate.
    - inplace: if True, modify the input df; otherwise work on a copy and return it.

    Returns the DataFrame with new columns added, aligned to the original index.
    """
    if not inplace:
        df = df.copy()

    try:
        df["ClaimFrequency"] = claim_frequency(df)
        df["ClaimSeverity"] = claim_severity(df, keep_na=keep_severity_na)
        df["Margin"] = margin(df, fillna=fillna_for_margin)
        if include_margin_rate:
            df["MarginRate"] = margin_rate(df)
    except Exception as exc:
        logger.exception("Error attaching metrics: %s", exc)
        raise

    return df
