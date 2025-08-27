from __future__ import annotations
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

def overview(df: pd.DataFrame) -> Dict[str, Any]:
    dtypes = df.dtypes.apply(lambda x: str(x)).to_dict()
    type_counts = df.dtypes.value_counts().astype(int).to_dict()
    missing_by_col = df.isna().sum().sort_values(ascending=False).to_dict()
    overall_missing_pct = float(df.isna().sum().sum()) / (df.shape[0] * df.shape[1]) * 100 if df.size else 0.0
    mem_bytes = df.memory_usage(deep=True).sum()
    return {
        "shape": {"rows": int(df.shape[0]), "cols": int(df.shape[1])},
        "dtypes": dtypes,
        "type_counts": type_counts,
        "missing_by_col": missing_by_col,
        "overall_missing_pct": overall_missing_pct,
        "memory_bytes": int(mem_bytes),
    }

def numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=["number"])
    if num.empty:
        return pd.DataFrame()
    desc = num.describe().T
    desc["missing"] = num.isna().sum()
    return desc

def categorical_stats(df: pd.DataFrame, top_n: int = 10) -> Dict[str, Any]:
    cat = df.select_dtypes(include=["object", "category", "bool"])
    result: Dict[str, Any] = {}
    for col in cat.columns:
        series = cat[col]
        vc = series.value_counts(dropna=True).head(top_n)
        result[col] = {
            "unique": int(series.nunique(dropna=True)),
            "top_values": vc.to_dict()
        }
    return result

def correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    num = df.select_dtypes(include=["number"])
    if num.empty or num.shape[1] < 2:
        return pd.DataFrame()
    corr = num.corr(method=method)
    return corr

def target_relationships(df: pd.DataFrame, target: Optional[str]) -> Dict[str, Any]:
    if not target or target not in df.columns:
        return {}
    import pandas as pd
    import numpy as np

    result: Dict[str, Any] = {}
    y = df[target]
    if pd.api.types.is_numeric_dtype(y):
        num = df.select_dtypes(include=["number"]).drop(columns=[target], errors="ignore")
        corrs = num.corrwith(y).sort_values(ascending=False)
        result["numeric_target_correlations"] = corrs.to_dict()
    else:
        num = df.select_dtypes(include=["number"])
        means = num.groupby(df[target]).mean(numeric_only=True)
        result["categorical_target_group_means"] = means.to_dict()
    return result