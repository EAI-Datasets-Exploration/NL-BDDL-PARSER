import pandas as pd


def get_unique_commands(fp: str, nl_column: str) -> int:
    df = pd.read_csv(fp)
    unique_df = df[nl_column].unique()
    return unique_df
