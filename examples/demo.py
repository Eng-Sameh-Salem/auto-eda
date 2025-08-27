"""
Minimal demo showing how to run auto-eda on a toy dataset.
Usage:
    python examples/demo.py
"""
import os
from sklearn import datasets
import pandas as pd
from auto_eda.cli import app

def main():
    iris = datasets.load_iris(as_frame=True)
    df = iris.frame
    csv_path = "iris.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved demo dataset to {csv_path}")
    app(["--input", csv_path, "--output", "report", "--target", "target"])

if __name__ == "__main__":
    main()