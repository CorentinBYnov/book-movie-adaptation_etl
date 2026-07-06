import pandas as pd
import numpy as np


def transform_omdb_for_load(df_omdb):
    """
    Sépare et transforme le dataframe omdb en deux jeux de données prêts au chargement :
    - un dataframe 'movies' aligné sur le schéma de la table movies (fusionnable avec movies_clean.csv)
    - un dataframe 'series' aligné sur le schéma de la table series

    Retourne un tuple (df_movies_ready, df_series_ready)
    """
    df = df_omdb.copy()

    # --- Partie films ---
    df_movies_ready = df[df['type'] == 'movie'].copy()

    # Colonnes absentes dans omdb mais requises par le schéma movies -> valeurs par défaut
    df_movies_ready['budget'] = np.nan
    df_movies_ready['profit'] = np.nan
    df_movies_ready['roi'] = np.nan

    movies_columns = [
        'title', 'year', 'director', 'rating',
        'votes', 'metascore', 'budget', 'gross', 'profit', 'roi'
    ]
    df_movies_ready = df_movies_ready[movies_columns]

    # --- Partie séries ---
    df_series_ready = df[df['type'] == 'series'].copy()

    series_columns = [
        'title', 'year', 'rating', 'votes',
        'metascore', 'total_seasons'
    ]
    df_series_ready = df_series_ready[series_columns]

    print(f"   -> Transform omdb : {len(df_movies_ready)} films et {len(df_series_ready)} séries préparés pour le load.")

    return df_movies_ready, df_series_ready


def main():
    df_omdb = pd.read_csv("data/processed/omdb_clean.csv")

    df_movies_ready, df_series_ready = transform_omdb_for_load(df_omdb)

    # --- Fusion avec les films existants (avant 2016) ---
    df_movies = pd.read_csv("data/processed/movies_clean.csv")
    df_movies_full = pd.concat([df_movies, df_movies_ready], ignore_index=True)

    # --- Sauvegarde des jeux de données prêts à charger ---
    df_movies_full.to_csv("data/processed/movies_full.csv", index=False)
    df_series_ready.to_csv("data/processed/series_clean.csv", index=False)


if __name__ == "__main__":
    main()