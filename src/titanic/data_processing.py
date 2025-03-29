import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder

def load_data(path_to_csv: str) -> pd.DataFrame:
    """Load a CSV as DataFrame."""
    df = pd.read_csv(path_to_csv)
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal cleaning/transformation steps.
        - Drop columns
        - Fill missing values
    """
    df = df.drop(["Name", "Ticket", "Cabin", "PassengerId", "Parch"], axis=1)
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("S")
    return df

def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordinal encoding for 'Sex' and 'Embarked'.
    # TODO: will come back latter to this stage and fix this because for production, ideally we can reuse a fitted encoder.
    """
    cat_cols = ["Sex", "Embarked"]
    encoder = OrdinalEncoder()
    df[cat_cols] = encoder.fit_transform(df[cat_cols])
    return df
