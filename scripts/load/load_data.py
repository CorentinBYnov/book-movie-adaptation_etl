import sqlite3
import pandas as pd


df_books = pd.read_csv("data/intermediaire/books_clean.csv")
df_movies = pd.read_csv("data/intermediaire/movies_clean.csv")


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

    df_books.to_sql("books", con, if_exists="append", index=False)
    df_movies.to_sql("movies", con, if_exists="append", index=False)

    con.close()


if __name__ == "__main__":
    main()
