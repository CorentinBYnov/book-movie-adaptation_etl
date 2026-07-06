import pandas as pd
import numpy as np
import os

# --- CONFIGURATION DES CHEMINS ROBUSTE ---
# __file__ est le chemin de transform_omdb.py
# On remonte de 3 niveaux pour atteindre la racine : transform_omdb.py -> transform -> scripts -> racine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "omdb_raw.json")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
PROCESSED_PATH = os.path.join(PROCESSED_DIR, "omdb_clean.csv")

print(f"Racine du projet détectée : {BASE_DIR}")
print(f"Recherche du fichier brut dans : {RAW_PATH}")


try:
    df_raw = pd.read_json(RAW_PATH)
    print(f"   -> Succès : {df_raw.shape[0]} lignes chargées depuis {RAW_PATH}")
except FileNotFoundError:
    raise FileNotFoundError(f"Impossible de trouver le fichier brut à l'emplacement : {RAW_PATH}")

def transform_omdb_pipeline(df):
    df_out = df.copy()
    
    # Remplacement global des masques textuels 'N/A' par de vrais NaN
    df_out = df_out.replace(r'^\s*N/A\s*$', np.nan, regex=True)
    
    # --- Traitement des formats numériques ---
    if 'BoxOffice' in df_out.columns:
        df_out['BoxOffice'] = df_out['BoxOffice'].astype(str).str.replace(r'[\$,]', '', regex=True)
        df_out['BoxOffice'] = pd.to_numeric(df_out['BoxOffice'], errors='coerce')
        
    if 'imdbVotes' in df_out.columns:
        df_out['imdbVotes'] = df_out['imdbVotes'].astype(str).str.replace(',', '', regex=False)
        df_out['imdbVotes'] = pd.to_numeric(df_out['imdbVotes'], errors='coerce')
        
    if 'Metascore' in df_out.columns:
        df_out['Metascore'] = pd.to_numeric(df_out['Metascore'], errors='coerce')
        
    if 'imdbRating' in df_out.columns:
        df_out['imdbRating'] = pd.to_numeric(df_out['imdbRating'], errors='coerce')
        
    if 'totalSeasons' in df_out.columns:
        df_out['totalSeasons'] = pd.to_numeric(df_out['totalSeasons'], errors='coerce')
        
    # --- Gestion et normalisation des Titres ---
    if 'Title' in df_out.columns:
        # On sauvegarde le titre d'origine dans une nouvelle colonne dédiée
        df_out['Title_Original'] = df_out['Title']
        
        # Le champ 'Title' principal devient le titre nettoyé (minuscules, strip, sans ponctuation)
        df_out['Title'] = df_out['Title'].astype(str).str.lower().str.strip()
        df_out['Title'] = df_out['Title'].str.replace(r'[^\w\s]', ' ', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()

        # Le champ 'Director' devient le titre nettoyé (minuscules, strip, sans ponctuation)
        df_out['Director'] = df_out['Director'].astype(str).str.lower().str.strip()
        df_out['Director'] = df_out['Director'].str.replace(r'[^\w\s]', ' ', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()

    # --- Filtrage ciblé sur le Box-Office ---
    # Règle : Si c'est un film ('movie'), le Box-Office est obligatoire. Si c'est une série, pas touche.
    initial_count = len(df_out)
    df_out = df_out[~((df_out['Type'] == 'movie') & (df_out['BoxOffice'].isna()))]
    print(f"   -> Filtrage : {initial_count - len(df_out)} films sans Box-Office ont été supprimés (les séries n'ont pas été impactées).")

    # --- Sélection et ordonnancement des colonnes cibles ---
    target_columns = [
        'Title', 'Year', 'Director', 'imdbRating', 'imdbVotes', 
        'Metascore', 'Type', 'totalSeasons', 'BoxOffice'
    ]
    existing_targets = [col for col in target_columns if col in df_out.columns]

    # --- Modification des noms de colonnes pour la cohérence avec les précédentes données de imdb ---
    rename_mapping = {
        'Title': 'title',
        'Year': 'year',
        'Director': 'director',
        'imdbRating': 'rating',
        'imdbVotes': 'votes',
        'Metascore': 'metascore',
        'Type': 'type',
        'totalSeasons': 'total_seasons',
        'BoxOffice': 'gross'
    }

    # On sélectionne AVANT de renommer, pour garder les bons noms de colonnes
    df_out = df_out[existing_targets].rename(columns=rename_mapping)
    
    return df_out

df_omdb_clean = transform_omdb_pipeline(df_raw)

# --- Sauvegarde du DataFrame nettoyé ---
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Sauvegarde en CSV
df_omdb_clean.to_csv(PROCESSED_PATH, index=False, encoding='utf-8')
print(f"   -> Succès : Données sauvegardées dans '{PROCESSED_PATH}'")
print(f"Pipeline ETL terminé ! Dataset final : {df_omdb_clean.shape[0]} lignes et {df_omdb_clean.shape[1]} colonnes.")