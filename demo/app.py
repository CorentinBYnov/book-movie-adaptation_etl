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

    st.subheader("Retour sur investissement")
    st.write(f"ROI moyen : {finance_df.roi.mean().round(2)}")
    st.write(f"ROI max : {finance_df.roi.max().round(2)}")
    st.write(f"ROI min : {finance_df.roi.min().round(2)}")

    st.subheader("Rentabilité")
    st.write(
        f"L'adaptations est rentable dans {((finance_df.profit > 0).sum() * 100 / len(finance_df)):.2f}% des cas."
    )
    st.write(
        f"L'adaptations représente une perte dans {((finance_df.profit < 0).sum() * 100 / len(finance_df)):.2f}% des cas."
    )

with rating_tab:
    st.write(ratings_df)

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

    ratings_df["book_rating_10"] = ratings_df.book_rating * 2
    ratings_df["difference"] = ratings_df.movie_rating - ratings_df.book_rating_10
    ratings_df["abs_difference"] = ratings_df.difference.abs()

    most_faithful = ratings_df.nsmallest(3, "abs_difference")
    least_faithful = ratings_df.nlargest(3, "abs_difference")

    biggest_improvements = ratings_df.nlargest(3, "difference")
    biggest_disappointments = ratings_df.nsmallest(3, "difference")

    st.subheader("Les 3 adaptations aux notes les plus fidèles")
    st.dataframe(
        most_faithful[
            ["title", "year", "director", "book_rating", "movie_rating", "difference"]
        ]
    )

    st.subheader("Les 3 adaptations aux notes les moins fidèles")
    st.dataframe(
        least_faithful[
            ["title", "year", "director", "book_rating", "movie_rating", "difference"]
        ]
    )

    st.subheader("Les 3 adaptations qui ont le plus surpris")
    st.dataframe(
        biggest_improvements[
            ["title", "year", "director", "book_rating", "movie_rating", "difference"]
        ]
    )

    st.subheader("Les 3 adaptations qui ont le plus déçu")
    st.dataframe(
        biggest_disappointments[
            ["title", "year", "director", "book_rating", "movie_rating", "difference"]
        ]
    )

with finance_tab:
    st.write(finance_df)

    st.subheader("Corrélations économiques")
    corr_livre_recettes = ratings_df.book_rating.corr(finance_df.profit)
    corr_film_recettes = ratings_df.movie_rating.corr(finance_df.profit)

    st.write(
        f"Corrélation [Note du Livre ➔ Profit du Film] : {corr_livre_recettes:.2f}"
    )
    st.write(f"Corrélation [Note du Film  ➔ Profit du Film] : {corr_film_recettes:.2f}")

    st.subheader("Impact de la popularité du livre sur le profit du film")

    finance_plot_df = finance_df.copy()
    finance_plot_df["book_rating"] = ratings_df["book_rating"]

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.regplot(
        data=finance_plot_df,
        x="book_rating",
        y="profit",
        color="#1b5e20",
        scatter_kws={"alpha": 0.6, "s": 70},
        line_kws={
            "color": "#d32f2f",
            "lw": 2,
            "label": f"Tendance (r = {corr_livre_recettes:.2f})",
        },
        ax=ax,
    )

    ax.set_title(
        "Impact de la popularité du livre sur le profit du film",
        fontsize=13,
        pad=15,
        fontweight="bold",
    )
    ax.set_xlabel("Note moyenne du livre (/5)")
    ax.set_ylabel("Profit du film")
    ax.legend(loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)

    st.subheader("Rapport entre le profit, la note du film et la popularité du livre")

    finance_plot_df = finance_df.copy()
    finance_plot_df["book_rating"] = ratings_df["book_rating"]
    finance_plot_df["movie_rating"] = ratings_df["movie_rating"]

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        finance_plot_df["profit"],
        finance_plot_df["movie_rating"],
        c=finance_plot_df["book_rating"] * 2,
        cmap="viridis",
        s=finance_plot_df["profit"].abs() * 0.000001,
        alpha=0.8,
        edgecolors="white",
        linewidth=0.5,
    )

    ax.set_title(
        "Rapport entre le profit, la note du film et la popularité du livre",
        fontsize=13,
        pad=15,
        fontweight="bold",
    )
    ax.set_xlabel("Profit du film")
    ax.set_ylabel("Note du film (sur 10)")
    ax.grid(True, linestyle="--", alpha=0.4)

    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Note moyenne du livre (sur 10)")

    st.pyplot(fig)

    most_profitable = finance_df.nlargest(3, "profit")
    least_profitable = finance_df.nsmallest(3, "profit")

    st.subheader("Les 3 adaptations les plus rentables")
    st.dataframe(
        most_profitable[["title", "year", "director", "budget", "profit", "roi"]]
    )

    st.subheader("Les 3 adaptations les moins rentables")
    st.dataframe(
        least_profitable[["title", "year", "director", "budget", "profit", "roi"]]
    )
