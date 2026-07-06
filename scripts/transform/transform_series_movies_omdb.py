import pandas as pd

# Alignement des noms de colonnes du CSV brut sur le schéma cible
RAW_COLUMN_MAPPING = {
    "Title": "title",
    "Year": "year",
    "Director": "director",
    "Rating": "rating",
    "Votes": "votes",
    "Metascore": "metascore",
}

def transform_omdb_for_load(df_omdb, df_movies_existing):
    """
    Sépare omdb en films/séries, et dédoublonne les films ajoutés contre les films
    déjà connus (df_movies_existing, déjà renommé au format cible).
    """
    df = df_omdb.copy()

    # --- Partie films ---

    df_movies_ready = df[df['type'] == 'movie'].copy()
    movies_columns = ['title', 'year', 'director', 'rating', 'votes', 'metascore']
    df_movies_ready = df_movies_ready[movies_columns]

    # --- Dédoublication ---

    # Force le type numérique de year côté omdb (actuellement en string)
    df_movies_ready['year'] = pd.to_numeric(df_movies_ready['year'], errors='coerce').astype('Int64')

    existing_keys = set(
        zip(
            df_movies_existing['title'].str.lower().str.strip(),
            df_movies_existing['year'],
        )
    )
    before = len(df_movies_ready)
    mask_duplicate = df_movies_ready.apply(
        lambda row: (row['title'], row['year']) in existing_keys, axis=1
    )
    duplicates = df_movies_ready[mask_duplicate]
    df_movies_ready = df_movies_ready[~mask_duplicate]

    print(f"   -> {before - len(df_movies_ready)} doublons retirés côté omdb (déjà présents dans movies).")
    if len(duplicates) > 0:
        print(duplicates[['title', 'year']].to_string(index=False))

    # --- Partie séries ---
    df_series_ready = df[df['type'] == 'series'][['title', 'year', 'rating', 'votes', 'total_seasons']]

    print(f"   -> Transform omdb : {len(df_movies_ready)} films et {len(df_series_ready)} séries préparés.")

    return df_movies_ready, df_series_ready


def main():
    df_omdb = pd.read_csv("data/processed/omdb_clean.csv")

    df_movies_raw = pd.read_csv("data/intermediate/movies_intermediate.csv")
    df_movies_raw = df_movies_raw.rename(columns=RAW_COLUMN_MAPPING)
    df_movies_raw = df_movies_raw[["title", "year", "director", "rating", "votes", "metascore"]]

    df_movies_ready, df_series_ready = transform_omdb_for_load(df_omdb, df_movies_raw)

    df_movies_full_intermediate = pd.concat([df_movies_raw, df_movies_ready], ignore_index=True)

    # Fichier intermédiaire (pas encore "clean" : sans données financières)
    df_movies_full_intermediate.to_csv("data/intermediate/movies_full_intermediate.csv", index=False)
    df_series_ready.to_csv("data/processed/series_clean.csv", index=False)


if __name__ == "__main__":
    main()