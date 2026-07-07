import matplotlib.pyplot as plt  # type: ignore
import plotly.express as px # type: ignore
import streamlit as st# type: ignore
import pandas as pd # type: ignore


def _show_director_impact(finance_df):
    st.subheader("🎬 Impact du réalisateur")
    st.caption("Réalisateurs ayant signé au moins 2 adaptations dans le dataset.")

    stats = (
        finance_df.groupby("director")
        .agg(
            nb_adaptations=("title", "count"),
            profit_moyen=("profit", "mean"),
            note_moyenne=("movie_rating", "mean"),
        )
        .query("nb_adaptations >= 2")
        .sort_values("profit_moyen", ascending=False)
        .reset_index()
    )

    if stats.empty:
        st.info("Aucun réalisateur avec plusieurs adaptations dans la sélection actuelle.")
        return

    fig = px.bar(
        stats.head(10),
        x="director",
        y="profit_moyen",
        color="note_moyenne",
        color_continuous_scale="viridis",
        hover_data={"nb_adaptations": True, "note_moyenne": ":.1f", "profit_moyen": ":.1f"},
        labels={
            "director": "Réalisateur",
            "profit_moyen": "Profit moyen",
            "note_moyenne": "Note moyenne du film",
        },
    )
    fig.update_layout(coloraxis_colorbar_title="Note moy.")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        stats.rename(columns={
            "director": "Réalisateur",
            "nb_adaptations": "Nb adaptations",
            "profit_moyen": "Profit moyen",
            "note_moyenne": "Note moyenne",
        }),
        hide_index=True,
    )


def _show_temporal_evolution(ratings_df, finance_df):
    st.subheader("📅 Évolution dans le temps")
    st.caption("Nombre d'adaptations et qualité moyenne, par année de sortie du film.")

    yearly_ratings = (
        ratings_df.groupby("year")
        .agg(nb_films=("title", "count"), note_moyenne=("movie_rating", "mean"))
        .reset_index()
    )
    yearly_finance = (
        finance_df.groupby("year")
        .agg(profit_moyen=("profit", "mean"))
        .reset_index()
    )
    yearly = yearly_ratings.merge(yearly_finance, on="year", how="left")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(yearly["year"], yearly["nb_films"], color="#90a4ae", alpha=0.6, label="Nb adaptations")
    ax1.set_xlabel("Année")
    ax1.set_ylabel("Nombre d'adaptations", color="#455a64")
    ax1.tick_params(axis="y", labelcolor="#455a64")

    ax2 = ax1.twinx()
    ax2.plot(yearly["year"], yearly["note_moyenne"], color="#d32f2f", marker="o", label="Note moyenne")
    ax2.set_ylabel("Note moyenne du film (/10)", color="#d32f2f")
    ax2.tick_params(axis="y", labelcolor="#d32f2f")

    fig.suptitle("Volume et qualité des adaptations par année", fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig)


def _show_franchise_effect(ratings_df, finance_df):
    st.subheader("🌌 Effet franchise")
    st.caption(
        "Heuristique : les titres partageant leurs 2 premiers mots sont considérés "
        "comme appartenant à la même saga (ex. 'harry potter and...')."
    )

    df = finance_df.copy()
    df["franchise_key"] = df["title"].str.split().str[:2].str.join(" ")

    franchise_counts = df["franchise_key"].value_counts()
    franchises = franchise_counts[franchise_counts >= 2].index

    df["is_franchise"] = df["franchise_key"].isin(franchises)
    df["type"] = df["is_franchise"].map({True: "Franchise", False: "Film isolé"})

    summary = df.groupby("type").agg(
        nb_films=("title", "count"),
        profit_moyen=("profit", "mean"),
        note_moyenne=("movie_rating", "mean"),
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(
            summary.rename(columns={
                "type": "Type",
                "nb_films": "Nb films",
                "profit_moyen": "Profit moyen",
                "note_moyenne": "Note moyenne",
            }),
            hide_index=True,
        )
    with col2:
        fig = px.bar(
            summary, x="type", y="profit_moyen", color="type",
            labels={"type": "", "profit_moyen": "Profit moyen"},
            color_discrete_map={"Franchise": "#C9A227", "Film isolé": "#5B6472"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    if len(franchises) > 0:
        st.write("**Franchises détectées :** " + ", ".join(franchises[:8]))


def show_trends(ratings_df, finance_df):
    _show_director_impact(finance_df)
    st.divider()
    _show_temporal_evolution(ratings_df, finance_df)
    st.divider()
    _show_franchise_effect(ratings_df, finance_df)