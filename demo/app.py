import sqlite3

import pandas as pd
import streamlit as st

from finance import show_finance
from info import show_info
from rating import show_rating


@st.cache_data
def get_ratings():
    con = sqlite3.connect("database/cinema.db")
    df = pd.read_sql_query(
        """
        SELECT movies.title, movies.year, movies.director, books.rating_average AS book_rating, movies.votes AS movie_votes, movies.rating AS movie_rating
        FROM books
        JOIN book_movie_adaptations ON books.id = book_movie_adaptations.book_id
        JOIN movies ON book_movie_adaptations.movie_id = movies.id;
        """,
        con,
    )
    con.close()
    return df


@st.cache_data
def get_finance():
    con = sqlite3.connect("database/cinema.db")
    df = pd.read_sql_query(
        """
        SELECT movies.title, movies.year, movies.director, movies.budget, movies.profit, movies.roi
        FROM movies
        JOIN book_movie_adaptations ON movies.id = book_movie_adaptations.movie_id;
        """,
        con,
    )
    con.close()
    return df


ratings_df = get_ratings()
finance_df = get_finance()

st.title("Le Succès des Adaptations de Livres en Films")

info_tab, rating_tab, finance_tab = st.tabs(["Informations", "Notes", "Finances"])

with info_tab:
    show_info(ratings_df, finance_df)

with rating_tab:
    show_rating(ratings_df)

with finance_tab:
    show_finance(ratings_df, finance_df)
