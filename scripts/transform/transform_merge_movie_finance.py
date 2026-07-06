import pandas as pd


df_movies = pd.read_csv("data/intermediate/movies_full_intermediate.csv")
df_finance = pd.read_csv("data/intermediate/movie_finance_intermediate.csv")


df_movies_finance = pd.merge(
    df_movies, 
    df_finance, 
    left_on=["title", "year", "director"], 
    right_on=["name", "year", "director"],
    how="left",
)

df_movies_finance_final = df_movies_finance.drop("name", axis=1).reset_index().rename(columns={"index": "id"})


def main():
    df_movies_finance_final.to_csv("data/processed/movies_full.csv", index=False)


if __name__ == "__main__":
    main()
