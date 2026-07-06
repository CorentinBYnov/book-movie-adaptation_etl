import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3
import streamlit as st


def get_ratings():
    con = sqlite3.connect("database/cinema.db")
    df = pd.read_sql_query(
        """
        SELECT movies.title, movies.year, movies.director, books.rating_average AS book_rating, movies.rating AS movie_rating
        FROM books
        JOIN book_movie_adaptations ON books.id = book_movie_adaptations.book_id
        JOIN movies ON book_movie_adaptations.movie_id = movies.id;
        """,
        con,
    )
    con.close()
    return df


ratings_df = get_ratings()


st.title("Le Succès des Adaptations de Livres en Films")

info_tab, rating_tab, finance_tab = st.tabs(["Informations", "Notes", "Finances"])

with info_tab:
    st.write(ratings_df)

    st.subheader("Moyenne des notes")
    st.write(f"Livres : {ratings_df['book_rating'].mean().round(2)}/5")
    st.write(f"Films  : {ratings_df['movie_rating'].mean().round(2)}/10")

    st.subheader("Rapport des notes")
    st.write(
        f"Le livre surpasse le film dans {((ratings_df.book_rating * 2 > ratings_df.movie_rating).sum() * 100 / len(ratings_df)):.2f}% des cas."
    )
    st.write(
        f"Le film surpasse le livre dans {((ratings_df.book_rating * 2 < ratings_df.movie_rating).sum() * 100 / len(ratings_df)):.2f}% des cas."
    )

with rating_tab:
    st.subheader("Graphique des notes")

    plot_df = pd.DataFrame(
        {
            "Type": ["Livre"] * len(ratings_df) + ["Film"] * len(ratings_df),
            "Note": list(ratings_df["book_rating"] * 2)
            + list(ratings_df["movie_rating"]),
        }
    )

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(
        data=plot_df,
        x="Type",
        y="Note",
        ax=ax,
        palette=["#1b5e20", "#b71c1c"],
        width=0.4,
        linewidth=2,
    )

    ax.set_title("Distribution des notes")
    ax.set_ylabel("Note (sur 10)")

    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)

    st.pyplot(fig)


    st.subheader("Corrélation entre les notes")

    corr_pearson = (ratings_df["book_rating"] * 2).corr(ratings_df["movie_rating"])

    fig, ax = plt.subplots(figsize=(9, 6))

    sns.regplot(
        data=ratings_df,
        x=ratings_df["book_rating"] * 2,
        y="movie_rating",
        color="#4a148c",
        scatter_kws={"alpha": 0.6, "s": 70},
        line_kws={
            "color": "#ff6f00",
            "lw": 2,
            "label": f"Tendance (r = {corr_pearson:.2f})",
        },
        ax=ax,
    )

    ax.set_title("L'évaluation d'un livre influence-t-elle celle de son film ?")
    ax.set_xlabel("Note moyenne du livre (sur 10)")
    ax.set_ylabel("Note moyenne du film (sur 10)")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left")

    st.pyplot(fig)

    st.write(f"**Coefficient de corrélation de Pearson :** {corr_pearson:.2f}")
