import pandas as pd
from pathlib import Path

FILE_PATH = Path("dob_history.csv")

def load_dobs():
    if not FILE_PATH.exists():
        return []

    df = pd.read_csv(FILE_PATH)
    return df["dob"].tolist()

def save_dob(dob_string: str):
    try:
        if FILE_PATH.exists():
            df = pd.read_csv(FILE_PATH)
            if dob_string in df["dob"].values:
                return
        else:
            df = pd.DataFrame(columns=["dob"])

        df.loc[len(df)] = [dob_string]
        df.to_csv(FILE_PATH, index=False)

    except Exception:
        pass
