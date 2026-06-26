import pandas as pd


df_books = pd.read_csv("data/processed/books_clean.csv")
df_movies = pd.read_csv("data/processed/movies_clean.csv")

df_books_subset = df_books[["title", "id"]].rename(columns={"id": "book_id"})
df_movies_subset = df_movies[["title", "id"]].rename(columns={"id": "movie_id"})

df_matching_ids = df_books_subset.merge(df_movies_subset, on="title", how="inner")

df_book_movie_adaptations = df_matching_ids.drop(columns=["title"])


def export(df, path):
    df.to_csv(path, index=False)


def main():
    export(df_book_movie_adaptations, "data/processed/join_books_movies.csv")


if __name__ == "__main__":
    main()

