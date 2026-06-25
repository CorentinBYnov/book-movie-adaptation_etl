import pandas as pd


df = pd.read_csv("data/raw/imdb_movie_dataset.csv")


def clean_na(df):
    return df.dropna()


def lower(df):
    return df.map(lambda x: x.lower() if isinstance(x, str) else x)


def change_column_names(df):
    return df.rename(columns=str.lower)


def export(df, path):
    df.to_csv(path)


def main():
    clean_df = change_column_names(lower(clean_na(df)))
    export(clean_df, "data/intermediaire/movies_clean.csv")


if __name__ == "__main__":
    main()
