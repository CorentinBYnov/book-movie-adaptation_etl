import matplotlib.pyplot as plt # type: ignore
import plotly.express as px # type: ignore
import seaborn as sns # type: ignore
import streamlit as st # type: ignore


def _show_raw_data(finance_df):
    st.write(finance_df)


def _show_economic_correlations(finance_df):
    st.subheader("Corrélations économiques")
    corr_book_profit = finance_df.book_rating.corr(finance_df.profit)
    corr_movie_profit = finance_df.movie_rating.corr(finance_df.profit)

    col1, col2 = st.columns(2)
    col1.metric("Corrélation Note Livre ➔ Profit", f"{corr_book_profit:.2f}")
    col2.metric("Corrélation Note Film ➔ Profit", f"{corr_movie_profit:.2f}")

    return corr_book_profit


def _plot_book_popularity_vs_profit(finance_df, corr_book_profit):
    st.subheader("Impact de la popularité du livre sur le profit du film")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=finance_df,
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


def _plot_profit_rating_scatter(finance_df):
    st.subheader("Rapport entre le profit, la note du film et la popularité du livre")
    st.caption("Survolez un point pour voir le détail du film. Taille des points = nombre de votes.")

    fig = px.scatter(
        finance_df,
        x="profit",
        y="movie_rating",
        color="book_rating",
        size="movie_votes",
        hover_name="title",
        hover_data={"year": True, "director": True, "profit": ":.1f", "book_rating": ":.2f"},
        color_continuous_scale="viridis",
        labels={
            "profit": "Profit du film",
            "movie_rating": "Note du film (sur 10)",
            "book_rating": "Note moyenne du livre",
        },
    )
    fig.update_layout(coloraxis_colorbar_title="Note du livre")
    st.plotly_chart(fig, use_container_width=True)


def _show_profit_extremes(finance_df):
    cols = ["title", "year", "director", "budget", "profit", "roi"]
    unique_df = finance_df.drop_duplicates(subset=["title", "year"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Les 3 plus rentables")
        st.dataframe(unique_df.nlargest(3, "profit")[cols], hide_index=True)
    with col2:
        st.subheader("📉 Les 3 moins rentables")
        st.dataframe(unique_df.nsmallest(3, "profit")[cols], hide_index=True)


def show_finance(finance_df):
    _show_raw_data(finance_df)
    corr_book_profit = _show_economic_correlations(finance_df)
    _plot_book_popularity_vs_profit(finance_df, corr_book_profit)
    _plot_profit_rating_scatter(finance_df)
    _show_profit_extremes(finance_df)