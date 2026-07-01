import pandas as pd


df = pd.read_csv("data/raw/movies.csv")
keep = ["name", "budget", "gross"]


def pipe(df, functions):
    for f in functions:
        df = f(df)
    return df


def select_columns(df, columns):
    return df[columns]


def clean_na(df):
    return df.dropna()


def lower_column(df, column_name):
    new_df = df.copy()
    new_df[column_name] = new_df[column_name].str.lower().str.strip()
    return new_df


def add_profit(df):
    new_df = df.copy()
    new_df["profit"] = new_df.gross - new_df.budget
    return new_df


def add_roi(df):
    new_df = df.copy()
    new_df["roi"] = (new_df.gross - new_df.budget) / new_df.budget * 100
    return new_df


def export(df, path):
    df.to_csv(path, index=False)


functions = (
    lambda x: select_columns(x, keep),
    clean_na,
    lambda x: lower_column(x, "name"),
    add_profit,
    add_roi,
)


def main():
    clean_df = pipe(df, functions)
    export(clean_df, "data/intermediate/movie_finance_intermediate.csv")


if __name__ == "__main__":
    main()
