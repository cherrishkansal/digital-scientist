import pandas as pd
from scipy.stats import pearsonr


def analyze_dataset(file_path, independent_col, dependent_col):

    df = pd.read_csv(file_path)

    if independent_col not in df.columns:
        return {"error": f"Column '{independent_col}' not found."}

    if dependent_col not in df.columns:
        return {"error": f"Column '{dependent_col}' not found."}

    x = df[independent_col]
    y = df[dependent_col]

    correlation, p_value = pearsonr(x, y)

    significance = "Statistically Significant" if p_value < 0.05 else "Not Statistically Significant"

    return {
        "independent_variable": independent_col,
        "dependent_variable": dependent_col,
        "correlation": round(correlation, 4),
        "p_value": round(p_value, 6),
        "significance": significance,
        "rows": len(df)
    }