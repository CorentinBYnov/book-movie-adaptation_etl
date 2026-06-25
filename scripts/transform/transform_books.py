import os
import pandas as pd

def load_raw_data(file_path):
    """Charge le dataset de livres brut."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Le fichier brut est introuvable à l'emplacement : {file_path}")
    return pd.read_csv(file_path)

def clean_books_dataset(df):
    """
    Applique les règles de nettoyage et de filtrage validées lors de l'EDA :
    1. Filtrage strict des livres adaptés en films.
    2. Suppression des lignes dont l'année du film (movie_release_year) est manquante.
    3. Conversion de cette année en entier.
    4. Normalisation textuelle (minuscules + strip) sur les titres et auteurs.
    5. Sélection des 6 colonnes cibles spécifiées.
    """
    # Copie profonde pour éviter le SettingWithCopyWarning de Pandas
    df_clean = df.copy()
    
    # 1. Filtrage sur la colonne 'adapted_to_movie'
    df_clean = df_clean[df_clean['adapted_to_movie'] == True]
    
    # 2. Gestion des valeurs manquantes (NaN) sur la colonne 'movie_release_year'
    df_clean = df_clean.dropna(subset=['movie_release_year'])
    
    # 3. Normalisation du type de la colonne 'movie_release_year' (de float à int)
    df_clean['movie_release_year'] = df_clean['movie_release_year'].astype(int)
    
    # 4. Normalisation textuelle (Minuscules et nettoyage des espaces blancs)
    df_clean['title'] = df_clean['title'].str.lower().str.strip()
    df_clean['author'] = df_clean['author'].str.lower().str.strip()
    
    # 5. Sélection stricte des 6 colonnes cibles définies
    target_columns = [
        'id', 
        'title', 
        'author', 
        'rating_average', 
        'movie_release_year', 
        'isbn'
    ]
    df_clean = df_clean[target_columns]
    
    return df_clean

def save_intermediaire_data(df, output_path):
    """Sauvegarde le DataFrame nettoyé dans le dossier d'étape intermediaire."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Étape Transform (Livres) réussie !")
    print(f"💾 Fichier intermédiaire sauvegardé dans : {output_path}")
    print(f"📊 Dimensions de la mini-table : {df.shape[0]} lignes, {df.shape[1]} colonnes.\n")

def run_transform_books():
    """Point d'entrée principal pour l'exécution isolée ou orchestrée."""
    RAW_BOOKS_PATH = os.path.join("..", "..", "data", "raw", "top_1000_most_swapped_books.csv")
    INTERMEDIAIRE_BOOKS_PATH = os.path.join("..", "..", "data", "intermediaire", "books_clean.csv")
    
    print("🧹 Démarrage du nettoyage du dataset des livres...")
    
    try:
        df_raw = load_raw_data(RAW_BOOKS_PATH)
        df_clean = clean_books_dataset(df_raw)
        save_intermediaire_data(df_clean, INTERMEDIAIRE_BOOKS_PATH)
        
    except Exception as e:
        print(f"❌ Erreur lors de la transformation des livres : {e}")

if __name__ == "__main__":
    run_transform_books()