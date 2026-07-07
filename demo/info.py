import streamlit as st


def show_info(ratings_df, finance_df):
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
