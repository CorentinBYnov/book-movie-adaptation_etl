import streamlit as st


def _show_mean_ratings(ratings_df):
    st.subheader("Moyenne des notes")
    col1, col2 = st.columns(2)
    col1.metric("Livres", f"{ratings_df['book_rating'].mean():.2f}/5")
    col2.metric("Films", f"{ratings_df['movie_rating'].mean():.2f}/10")


def _show_rating_comparison(ratings_df):
    st.subheader("Rapport des notes")
    total = len(ratings_df)
    book_higher = (ratings_df.book_rating * 2 > ratings_df.movie_rating).sum()
    movie_higher = (ratings_df.book_rating * 2 < ratings_df.movie_rating).sum()
    st.write(
        f"Le livre surpasse le film dans {book_higher * 100 / total:.2f}% des cas."
    )
    st.write(
        f"Le film surpasse le livre dans {movie_higher * 100 / total:.2f}% des cas."
    )


def _show_roi_stats(finance_df):
    st.subheader("Retour sur investissement")
    col1, col2, col3 = st.columns(3)
    col1.metric("ROI moyen", f"{finance_df.roi.mean():.2f}%")
    col2.metric("ROI max", f"{finance_df.roi.max():.2f}%")
    col3.metric("ROI min", f"{finance_df.roi.min():.2f}%")


def _show_profitability(finance_df):
    st.subheader("Rentabilité")
    total = len(finance_df)
    profitable = (finance_df.profit > 0).sum()
    loss = (finance_df.profit < 0).sum()
    st.write(
        f"L'adaptations est rentable dans {profitable * 100 / total:.2f}% des cas."
    )
    st.write(
        f"L'adaptations représente une perte dans {loss * 100 / total:.2f}% des cas."
    )


def show_info(ratings_df, finance_df):
    _show_mean_ratings(ratings_df)
    _show_rating_comparison(ratings_df)
    _show_roi_stats(finance_df)
    _show_profitability(finance_df)