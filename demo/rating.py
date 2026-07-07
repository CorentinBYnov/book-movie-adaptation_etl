import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def _show_raw_data(ratings_df):
    st.write(ratings_df.drop("movie_votes", axis=1))


def _plot_rating_distribution(ratings_df):
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
        hue="Type",
        legend=False,
        width=0.4,
        linewidth=2,
    )
    ax.set_title("Distribution des notes")
    ax.set_ylabel("Note (sur 10)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    st.pyplot(fig)


def _plot_correlation(ratings_df):
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


def _show_extremes(ratings_df):
    ratings_df = ratings_df.copy()
    ratings_df["book_rating_10"] = ratings_df.book_rating * 2
    ratings_df["difference"] = ratings_df.movie_rating - ratings_df.book_rating_10
    ratings_df["abs_difference"] = ratings_df.difference.abs()

    cols = ["title", "year", "director", "book_rating", "movie_rating", "difference"]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Notes les plus fidèles")
        st.dataframe(ratings_df.nsmallest(3, "abs_difference")[cols], hide_index=True)
    with col2:
        st.subheader("↔️ Notes les moins fidèles")
        st.dataframe(ratings_df.nlargest(3, "abs_difference")[cols], hide_index=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("😲 Les plus surprenantes")
        st.dataframe(ratings_df.nlargest(3, "difference")[cols], hide_index=True)
    with col4:
        st.subheader("😞 Les plus décevantes")
        st.dataframe(ratings_df.nsmallest(3, "difference")[cols], hide_index=True)


def show_rating(ratings_df):
    _show_raw_data(ratings_df)
    _plot_rating_distribution(ratings_df)
    _plot_correlation(ratings_df)
    _show_extremes(ratings_df)