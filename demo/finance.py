import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def _show_raw_data(finance_df):
    st.write(finance_df)


def _show_economic_correlations(ratings_df, finance_df):
    st.subheader("Corrélations économiques")
    corr_book_profit = ratings_df.book_rating.corr(finance_df.profit)
    corr_movie_profit = ratings_df.movie_rating.corr(finance_df.profit)
    st.write(f"Corrélation [Note du Livre ➔ Profit du Film] : {corr_book_profit:.2f}")
    st.write(f"Corrélation [Note du Film  ➔ Profit du Film] : {corr_movie_profit:.2f}")
    return corr_book_profit


def _plot_book_popularity_vs_profit(ratings_df, finance_df, corr_book_profit):
    st.subheader("Impact de la popularité du livre sur le profit du film")
    plot_df = finance_df.copy()
    plot_df["book_rating"] = ratings_df["book_rating"]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=plot_df,
        x="book_rating",
        y="profit",
        color="#1b5e20",
        scatter_kws={"alpha": 0.6, "s": 70},
        line_kws={
            "color": "#d32f2f",
            "lw": 2,
            "label": f"Tendance (r = {corr_book_profit:.2f})",
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


def _plot_profit_rating_scatter(ratings_df, finance_df):
    st.subheader("Rapport entre le profit, la note du film et la popularité du livre")
    plot_df = finance_df.copy()
    plot_df["book_rating"] = ratings_df["book_rating"]
    plot_df["movie_rating"] = ratings_df["movie_rating"]
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        plot_df["profit"],
        plot_df["movie_rating"],
        c=plot_df["book_rating"] * 2,
        cmap="viridis",
        s=plot_df["profit"].abs() * 0.000001,
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


def _show_profit_extremes(finance_df):
    cols = ["title", "year", "director", "budget", "profit", "roi"]
    st.subheader("Les 3 adaptations les plus rentables")
    st.dataframe(finance_df.nlargest(3, "profit")[cols])
    st.subheader("Les 3 adaptations les moins rentables")
    st.dataframe(finance_df.nsmallest(3, "profit")[cols])


def show_finance(ratings_df, finance_df):
    _show_raw_data(finance_df)
    corr_book_profit = _show_economic_correlations(ratings_df, finance_df)
    _plot_book_popularity_vs_profit(ratings_df, finance_df, corr_book_profit)
    _plot_profit_rating_scatter(ratings_df, finance_df)
    _show_profit_extremes(finance_df)
