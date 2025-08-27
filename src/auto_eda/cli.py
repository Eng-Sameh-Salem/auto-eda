from __future__ import annotations
import argparse
import os
import sys
import pandas as pd

from .io_utils import load_dataset, optimize_dtypes
from .report import build_report

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="auto-eda: fast, clear EDA reports for your data.")
    p.add_argument("--input", "-i", required=True, help="Path to dataset (.csv, .tsv, .xlsx, .xls, .parquet, .json)")
    p.add_argument("--output", "-o", default="report", help="Output directory (default: report)")
    p.add_argument("--target", "-t", default=None, help="Optional target column for feature insights")
    p.add_argument("--sep", default=None, help="Optional delimiter override for CSV/TSV")
    p.add_argument("--sheet", default=None, help="Excel sheet name or index")
    p.add_argument("--max-rows", type=int, default=None, help="Optional row cap for speed")
    p.add_argument("--sample", type=float, default=1.0, help="Optional fraction [0-1] to sample rows for visuals")
    return p.parse_args(argv)

def app(argv=None):
    args = parse_args(argv)

    df = load_dataset(args.input, sep=args.sep, sheet=args.sheet, nrows=args.max_rows)

    if 0 < args.sample < 1.0:
        df = df.sample(frac=args.sample, random_state=42).reset_index(drop=True)

    df = optimize_dtypes(df)

    out_html = build_report(df, output_dir=args.output, target=args.target)

    print(f"Report written to: {out_html}")
    return 0

if __name__ == "__main__":
    raise SystemExit(app())