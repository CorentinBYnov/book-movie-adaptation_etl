import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

# Configuration des chemins et clés
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("OMDB_API_KEY")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_JSON = os.path.join(RAW_DIR, "omdb_raw.json")

if not API_KEY:
    raise ValueError("❌ Clé OMDB_API_KEY introuvable dans le fichier .env")

def download_file_stream(url, dest_path):
    """Télécharge un gros fichier par blocs pour éviter de surcharger la mémoire."""
    filename = os.path.basename(dest_path)
    print(f"📥 Téléchargement de {filename}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status() # Lève une erreur si le téléchargement échoue (ex: 404, 500)
    
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024): # Blocs de 1 Mo
            if chunk:
                f.write(chunk)
    print(f"✅ {filename} téléchargé avec succès.")

def fetch_financials_from_omdb(imdb_id):
    """Utilise ta clé OMDb pour récupérer le Box-Office et les détails via l'ID IMDb."""
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                return data
        return None
    except Exception:
        return None

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # Chemins locaux pour stocker les dumps IMDb
    local_basics = os.path.join(RAW_DIR, "title.basics.tsv.gz")
    local_ratings = os.path.join(RAW_DIR, "title.ratings.tsv.gz")
    
    url_basics = "https://datasets.imdbws.com/title.basics.tsv.gz"
    url_ratings = "https://datasets.imdbws.com/title.ratings.tsv.gz"
    
    # 1. Téléchargement sécurisé des fichiers s'ils n'existent pas déjà
    if not os.path.exists(local_basics):
        download_file_stream(url_basics, local_basics)
    else:
        print("ℹ️ Fichier title.basics.tsv.gz déjà présent localement.")
        
    if not os.path.exists(local_ratings):
        download_file_stream(url_ratings, local_ratings)
    else:
        print("ℹ️ Fichier title.ratings.tsv.gz déjà présent localement.")

    # 2. Lecture locale par Pandas
    print("⚡ Chargement et filtrage de la population IMDb (2016-2026)...")
    df_basics = pd.read_csv(local_basics, sep='\t', compression='gzip', low_memory=False)
    df_ratings = pd.read_csv(local_ratings, sep='\t', compression='gzip', low_memory=False)
    
    # On ne garde que les films/séries populaires (> 25 000 votes)
    df_ratings = df_ratings[df_ratings['numVotes'] > 25000]
    
    # Filtrage : On resserre la cible uniquement sur la décennie récente (2016-2026)
    df_basics = df_basics[df_basics['startYear'] != '\\N']
    df_basics['startYear'] = df_basics['startYear'].astype(int)
    df_basics = df_basics[(df_basics['startYear'] >= 2016) & (df_basics['startYear'] <= 2026) & (df_basics['titleType'].isin(['movie', 'tvSeries']))]
    
    # Jointure pour notre échantillon de contrôle
    df_control = pd.merge(df_basics, df_ratings, on='tconst', how='inner')
    
    # STRATÉGIE : On trie par popularité décroissante pour capter les œuvres majeures
    df_control = df_control.sort_values(by='numVotes', ascending=False)
    
    # On extrait le top 800 pour respecter ton quota journalier OMDb # 200 pour aujourd'hui
    target_ids = df_control['tconst'].head(200).tolist()
    
    print(f"🚀 [EXTRACT] Enrichissement de {len(target_ids)} œuvres via l'API OMDb...")
    
    raw_payloads = []
    for i, imdb_id in enumerate(target_ids, 1):
        payload = fetch_financials_from_omdb(imdb_id)
        if payload:
            # On conserve les métadonnées d'origine d'IMDb (comme le nombre de votes)
            payload['numVotes'] = int(df_control[df_control['tconst'] == imdb_id]['numVotes'].values[0])
            raw_payloads.append(payload)
        
        if i % 100 == 0:
            print(f"  📥 {i}/{len(target_ids)} requêtes OMDb effectuées...")

    # 3. Sauvegarde du JSON brut dans data/raw
    if raw_payloads:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(raw_payloads, f, ensure_ascii=False, indent=4)
        print(f"\n💾 [SUCCÈS] Fichier brut enrichi sauvegardé : {OUTPUT_JSON}")

if __name__ == "__main__":
    main()