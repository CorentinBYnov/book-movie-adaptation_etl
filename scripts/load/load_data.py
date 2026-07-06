import sqlite3
import pandas as pd


df_books = pd.read_csv("data/processed/books_clean.csv")
df_movies = pd.read_csv("data/processed/movies_full.csv")
df_book_movie_adaptations = pd.read_csv("data/processed/join_books_movies.csv")
df_series = pd.read_csv("data/processed/series_clean.csv")


def main():
    con = sqlite3.connect("database/cinema.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT,
            title TEXT NOT NULL,
            rating_average REAL
        );
    """)

    cur.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            director TEXT NOT NULL,
            rating REAL,
            votes INTEGER,
            metascore REAL,
            budget REAL,
            gross REAL,
            profit REAL,
            roi REAL
        );
    """)

    cur.execute("""
        CREATE TABLE book_movie_adaptations (
            book_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, movie_id),
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        );
    """)

    cur.execute("""
        CREATE TABLE series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL,
            votes INTEGER,
            total_seasons INTEGER
        );
    """)

    df_books.to_sql("books", con, if_exists="append", index=False)
    df_movies.to_sql("movies", con, if_exists="append", index=False)
    df_book_movie_adaptations.to_sql(
        "book_movie_adaptations", con, if_exists="append", index=False
    )
    df_series.to_sql("series", con, if_exists="append", index=False)

    con.close()


if __name__ == "__main__":
    main()
