import pandas as pd


df = pd.read_csv("data/raw/imdb_movie_dataset.csv")
keep = ["Rank", "Title", "Rating", "Votes", "Metascore"]


def pipe(df, functions):
    for f in functions:
        df = f(df)
    return df


def select_columns(df, columns):
    return df[columns]


def clean_na(df):
    return df.dropna()


def lower(df):
    return df.map(lambda x: x.lower() if isinstance(x, str) else x)


def change_column_names(df):
    return df.rename(columns=str.lower).rename(columns={"rank": "id"})


def export(df, path):
    df.to_csv(path, index=False)


functions = (lambda x: select_columns(x, keep), clean_na, lower, change_column_names)


def main():
    clean_df = pipe(df, functions)
    export(clean_df, "data/intermediate/movies_intermediate.csv")


if __name__ == "__main__":
    main()
