import pandas as pd


df_movies = pd.read_csv("data/intermediate/movies_intermediate.csv")
df_finance = pd.read_csv("data/intermediate/movie_finance_intermediate.csv")


df_movies_final = pd.merge(
    df_movies, 
    df_finance, 
    left_on="title", 
    right_on="name",
    how="left",
)


def main():
    df_movies_final.to_csv("data/processed/movies_clean.csv", index=False)


if __name__ == "__main__":
    main()
