import os
import pandas as pd

def load_intermediate_data():
    """Charge les deux datasets nettoyés depuis le dossier intermediaire."""
    BOOKS_PATH = os.path.join("data", "processed", "books_clean.csv")
    MOVIES_PATH = os.path.join("data", "processed", "movies_clean.csv")
    
    if not os.path.exists(BOOKS_PATH) or not os.path.exists(MOVIES_PATH):
        raise FileNotFoundError(
            "❌ L'un des fichiers intermédiaires (books_clean.csv ou movies_clean.csv) est manquant. "
            "Assurez-vous que les deux scripts de transformation isolés ont été exécutés."
        )
        
    df_books = pd.read_csv(BOOKS_PATH)
    df_movies = pd.read_csv(MOVIES_PATH)
    return df_books, df_movies

def merge_datasets(df_books, df_movies):
    """
    Réalise la jointure entre les livres et les films.
    Ici, on part sur une jointure exacte (Inner Merge) sur le titre normalisé.
    """
    print("Fusion des données en cours...")
    
    # Jointure principale sur le titre
    df_final = pd.merge(
        df_books, 
        df_movies, 
        left_on='title', 
        right_on='title',
        how='inner',
        suffixes=('_book', '_movie') # Évite les conflits si vous avez des colonnes identiques (ex: rating)
    )
    
    return df_final

def save_processed_data(df, output_path):
    """Sauvegarde le dataset final prêt pour l'analyse ou la modélisation."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print("✅ Étape Transform Jointure réussie ! 🎉")
    print(f"💾 Dataset final sauvegardé dans : {output_path}")
    print(f"📊 Dimensions du dataset combiné : {df.shape[0]} lignes, {df.shape[1]} colonnes.\n")

def run_transform_jointure():
    """Point d'entrée principal pour la fusion de l'ETL."""
    PROCESSED_PATH = os.path.join("data", "processed", "adaptation_books_movies_full.csv")
    
    print("Démarage du script de jointure des datasets...")
    
    try:
        df_books, df_movies = load_intermediate_data()
        df_final = merge_datasets(df_books, df_movies)
        save_processed_data(df_final, PROCESSED_PATH)
        
    except Exception as e:
        print(f"❌ Erreur lors de la jointure : {e}")

if __name__ == "__main__":
    run_transform_jointure()