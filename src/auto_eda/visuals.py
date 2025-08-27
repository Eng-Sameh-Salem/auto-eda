from __future__ import annotations
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def histogram(df: pd.DataFrame, col: str):
    return px.histogram(df, x=col, marginal="box", nbins=40, title=f"Histogram of {col}")

def boxplot(df: pd.DataFrame, col: str):
    return px.box(df, y=col, points="outliers", title=f"Boxplot of {col}")

def bar_top_categories(df: pd.DataFrame, col: str, top_n: int = 20):
    vc = df[col].astype(str).value_counts().head(top_n).reset_index()
    vc.columns = [col, "count"]
    fig = px.bar(vc, x=col, y="count", title=f"Top {top_n} categories in {col}")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def correlation_heatmap(corr: pd.DataFrame):
    if corr.empty:
        return None
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        zmin=-1, zmax=1,
        coloraxis="coloraxis"
    ))
    fig.update_layout(title="Correlation Heatmap", coloraxis={"colorscale": "RdBu"})
    return fig

def scatter_pair(df: pd.DataFrame, cols: List[str], sample: float = 1.0):
    use = df[cols].dropna().copy()
    if 0 < sample < 1.0 and len(use) > 0:
        use = use.sample(frac=sample, random_state=42)
    return px.scatter_matrix(use, dimensions=cols, title="Pairwise Scatter Matrix")