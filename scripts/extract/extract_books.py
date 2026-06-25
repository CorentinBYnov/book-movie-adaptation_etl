import os
from kaggle.api.kaggle_api_extended import KaggleApi

def extract_raw_books():
    """
    Extrait le jeu de données brut depuis l'API Kaggle et le stocke
    dans le dossier de destination data/raw/.
    """
    # 1. Initialisation et authentification automatique via le jeton d'accès
    api = KaggleApi()
    api.authenticate()
    
    # 2. Définition des chemins (relatifs au dossier d'exécution attendu du projet)
    # On cible l'identifiant exact renvoyé par ton terminal
    dataset_slug = "sergiykovalchuck/the-most-popular-books-for-exchanging"
    target_dir = os.path.join("..", "..", "data", "raw")
    
    # S'assurer que le dossier data/raw/ existe bien
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"📥 Début du téléchargement du dataset '{dataset_slug}' depuis Kaggle...")
    
    try:
        # 3. Téléchargement et extraction (unzip) automatique du fichier CSV
        api.dataset_download_files(dataset_slug, path=target_dir, unzip=True)
        print(f"✅ Extraction réussie ! Fichiers bruts stockés dans : {target_dir}")
        
        # Petit check visuel pour lister ce qu'on a téléchargé dans data/raw
        print("Contenu de data/raw/ :", os.listdir(target_dir))
        
    except Exception as e:
        print(f"❌ Une erreur est survenue lors de l'extraction : {e}")

if __name__ == "__main__":
    extract_raw_books()