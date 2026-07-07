import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def show_finance(ratings_df, finance_df):
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
