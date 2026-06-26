import sqlite3
import pandas as pd


df_books = pd.read_csv("data/intermediaire/books_clean.csv")
df_movies = pd.read_csv("data/intermediaire/movies_clean.csv")

df_books_subset = df_books[["title", "id"]].rename(columns={"id": "book_id"})
df_movies_subset = df_movies[["title", "rank"]].rename(columns={"rank": "movie_id"})

df_matching_ids = df_books_subset.merge(df_movies_subset, on="title", how="inner")

df_book_movie_adaptations = df_matching_ids.drop(columns=["title"])


def main():
    con = sqlite3.connect("database/cinema.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            rating_average REAL,
            movie_release_year INTEGER,
            isbn TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE movies (
            rank INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT,
            description TEXT,
            director TEXT,
            actors TEXT,
            year INTEGER,
            "runtime (minutes)" INTEGER,
            rating REAL,
            votes INTEGER,
            "revenue (millions)" REAL,
            metascore REAL
        );
    """)

    cur.execute("""
        CREATE TABLE book_movie_adaptations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (movie_id) REFERENCES movies(rank)
        );
    """)

    df_books.to_sql("books", con, if_exists="append", index=False)
    df_movies.to_sql("movies", con, if_exists="append", index=False)
    df_book_movie_adaptations.to_sql(
        "book_movie_adaptations", con, if_exists="append", index=False
    )

    con.close()


if __name__ == "__main__":
    main()
