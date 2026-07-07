import sqlite3

import pandas as pd
import streamlit as st

from finance import show_finance
from info import show_info
from rating import show_rating

st.set_page_config(
    page_title="Adaptations Livre → Film",
    page_icon="🎬",
    layout="wide",
)


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
        SELECT movies.title, movies.year, movies.director, movies.budget, movies.profit, movies.roi, movies.votes AS movie_votes, movies.rating AS movie_rating, books.rating_average AS book_rating
        FROM movies
        JOIN book_movie_adaptations ON movies.id = book_movie_adaptations.movie_id
        JOIN books ON books.id = book_movie_adaptations.book_id;
        """,
        con,
    )
    con.close()
    return df


ratings_df = get_ratings()
finance_df = get_finance()

st.title("🎬 Le Succès des Adaptations de Livres en Films")

# --- Sidebar : filtres globaux ---
with st.sidebar:
    st.header("Filtres")

    year_min, year_max = int(ratings_df.year.min()), int(ratings_df.year.max())
    year_range = st.slider("Année de sortie", year_min, year_max, (year_min, year_max))

    search = st.text_input("🔍 Rechercher un titre", placeholder="ex: Dune, Narnia...")

    st.caption(f"{len(ratings_df)} adaptations au total dans la base.")

# Application des filtres
ratings_df = ratings_df[ratings_df.year.between(*year_range)]
finance_df = finance_df[finance_df.year.between(*year_range)]

if search:
    ratings_df = ratings_df[ratings_df.title.str.contains(search, case=False, na=False)]
    finance_df = finance_df[finance_df.title.str.contains(search, case=False, na=False)]

if ratings_df.empty:
    st.warning("Aucune adaptation ne correspond aux filtres sélectionnés.")
    st.stop()

info_tab, rating_tab, finance_tab = st.tabs(["📋 Informations", "⭐ Notes", "💰 Finances"])

with info_tab:
    show_info(ratings_df, finance_df)

with rating_tab:
    show_rating(ratings_df)

with finance_tab:
    show_finance(finance_df)