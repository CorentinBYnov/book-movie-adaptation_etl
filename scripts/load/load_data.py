import sqlite3
import pandas as pd


df = pd.read_csv("data/processed/adaptation_books_movies.csv")


def main():
    conn = sqlite3.connect("database/cinema.db")
    df.to_sql("adaptations", conn)
    conn.close()


if __name__ == "__main__":
    main()
