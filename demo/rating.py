import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def show_rating(ratings_df):
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
