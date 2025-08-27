from __future__ import annotations
import os
import io
import json
from typing import Optional, Tuple
import pandas as pd

def _infer_sep(sample: str) -> Optional[str]:
    candidates = [",", ";", "\t", "|"]
    counts = {sep: sample.count(sep) for sep in candidates}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else None

def load_dataset(path: str, sep: Optional[str] = None, sheet: Optional[str] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Load dataset from CSV/TSV/Excel/Parquet/JSON. Attempts to infer separator for CSV/TSV.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext in [".csv", ".tsv"]:
        if sep is None:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                sample = f.read(4096)
            sep = _infer_sep(sample) or ("," if ext == ".csv" else "\t")
        df = pd.read_csv(path, sep=sep, nrows=nrows, low_memory=False)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(path, sheet_name=sheet, nrows=nrows)
    elif ext == ".parquet":
        df = pd.read_parquet(path)
        if nrows is not None:
            df = df.head(nrows)
    elif ext == ".json":
        try:
            df = pd.read_json(path, lines=True, nrows=nrows)
        except ValueError:
            df = pd.read_json(path, orient="records")
            if nrows is not None:
                df = df.head(nrows)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return df

def memory_human_readable(n_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def optimize_dtypes(df: pd.DataFrame, cat_threshold: int = 50) -> pd.DataFrame:
    """
    Downcast numeric and convert low-cardinality object columns to category to reduce memory footprint.
    """
    import numpy as np

    for col in df.select_dtypes(include=["int", "int64", "float", "float64"]).columns:
        if "int" in str(df[col].dtype):
            df[col] = pd.to_numeric(df[col], downcast="integer")
        else:
            df[col] = pd.to_numeric(df[col], downcast="float")

    for col in df.select_dtypes(include=["object"]).columns:
        nunique = df[col].nunique(dropna=True)
        if 0 < nunique <= cat_threshold:
            df[col] = df[col].astype("category")

    return df