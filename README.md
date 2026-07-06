# Pipeline ETL Livres-Films (Adaptations)

Pipeline ETL qui télécharge et traite des jeux de données de livres et de films, identifie les adaptations littéraires au cinéma et en série, et charge les résultats dans une base SQLite.

## Jeux de données

| Fichier | Source | Description |
|---------|--------|-------------|
| `data/raw/top_1000_most_swapped_books.csv` | Kaggle (sergiykovalchuck/the-most-popular-books-for-exchanging) | 1000 livres populaires avec métadonnées incluant leur adaptation au cinéma |
| `data/raw/imdb_movie_dataset.csv` | Kaggle / IMDb (Yusuf Delikkaya, IMDB Movie Dataset) | 1000 films avec notes, votes, genres, réalisateur, casting |
| `data/raw/movies.csv` | Kaggle (Daniel Grijalva, Movie Industry) | Données financières des films (budget, recettes) |
| `data/raw/omdb_raw.json` | IMDb par OMDb API | Données enrichies (box-office, séries) via OMDb |

## Pipeline ETL

| Phase | Scripts | Produit |
|-------|---------|---------|
| **Extract** | `extract_books.py`, `extract_movies.py`, `extract_movie_finance.py`, `extract_omdb_api.py` | Fichiers bruts dans `data/raw/` |
| **Transform** | `transform_books.py`, `transform_movies.py`, `transform_omdb_api.py`, `transform_series_movies_omdb.py`, `transform_movie_finance.py`, `transform_merge_movie_finance.py`, `transform_join_books_movies.py`, `transform_join_books_series.py` | Fichiers nettoyés dans `data/processed/` |
| **Load** | `load_data.py` | `database/cinema.db` |

### 1. Extraction

Chaque script d'extraction collecte une source différente :

| Script | Source | Détails |
|--------|--------|---------|
| `extract_books.py` | Kaggle API (`sergiykovalchuck/the-most-popular-books-for-exchanging`) | Téléchargement via `KaggleApi.dataset_download_files()` → `data/raw/top_1000_most_swapped_books.csv` |
| `extract_movies.py` | Fichier CSV (commité) | Lit `data/raw/imdb_movie_dataset.csv` (1000 films IMDb) |
| `extract_movie_finance.py` | Fichier CSV (commité) | Lit `data/raw/movies.csv` (données financières : budget, recettes) |
| `extract_omdb_api.py` | IMDb dumps + OMDb API | Télécharge `title.basics.tsv.gz` et `title.ratings.tsv.gz` depuis IMDb ; filtre films/séries 2016-2026 avec >25 000 votes ; interroge l'API OMDb pour le top 200 (Box-Office, métadonnées) → `data/raw/omdb_raw.json` |

Se relance avec `python main.py --with-extract`. Par défaut, le pipeline réutilise les fichiers bruts déjà présents dans `data/raw/`.

### 2. Transformation

8 scripts exécutés en séquence. Chacun lit un CSV en entrée, applique des transformations pandas, et écrit le résultat :

| Script | Entrée | Transformations | Sortie |
|--------|--------|-----------------|--------|
| `transform_books.py` | `data/raw/top_1000_most_swapped_books.csv` | Filtre livres adaptés au cinéma ; supprime lignes sans année ; normalise titres/auteurs (minuscules) | `data/processed/books_clean.csv` |
| `transform_movies.py` | `data/raw/imdb_movie_dataset.csv` | Sélectionne 6 colonnes (Title, Year, Director, Rating, Votes, Metascore) ; supprime NA ; minuscules | `data/intermediate/movies_intermediate.csv` |
| `transform_omdb_api.py` | `data/raw/omdb_raw.json` | Remplace "N/A" par NaN ; convertit les champs numériques (BoxOffice, votes, rating…) ; normalise titres (minuscules, sans ponctuation) ; supprime films sans BoxOffice | `data/processed/omdb_clean.csv` |
| `transform_series_movies_omdb.py` | `omdb_clean.csv` + `movies_intermediate.csv` | Sépare films et séries ; déduplique les films déjà présents ; concatène avec movies_intermediate | `data/intermediate/movies_full_intermediate.csv` + `data/processed/series_clean.csv` |
| `transform_movie_finance.py` | `data/raw/movies.csv` | Sélectionne 5 colonnes (name, year, director, budget, gross) ; supprime NA ; calcule profit et ROI | `data/intermediate/movie_finance_intermediate.csv` |
| `transform_merge_movie_finance.py` | `movies_full_intermediate.csv` + `movie_finance_intermediate.csv` | Fusion gauche sur (title, year, director) | `data/processed/movies_full.csv` |
| `transform_join_books_movies.py` | `books_clean.csv` + `movies_full.csv` | Jointure interne sur le titre normalisé | `data/processed/join_books_movies.csv` (liaison n-n) |
| `transform_join_books_series.py` | `books_clean.csv` + `series_clean.csv` | Correspondance exacte + fuzzy (rapidfuzz, seuil 85%) | `data/processed/join_books_series.csv` |

### 3. Chargement

`load_data.py` crée la base SQLite `database/cinema.db` à partir des 5 fichiers CSV dans `data/processed/` :

1. Connexion et création des 5 tables (`books`, `movies`, `book_movie_adaptations`, `series`, `book_series_adaptations`) avec clés primaires et étrangères
2. Insertion des données via `pandas.to_sql()` avec `if_exists="append"`
3. Fermeture de la connexion

La base est recréée à chaque exécution (les tables sont créées via `CREATE TABLE`, sans `DROP IF EXISTS` préalable).

## Schéma de la base (cinema.db)

5 tables, recréées à chaque exécution :

### books - tous les livres du dataset top 1000

| Colonne | Type |
|---------|------|
| id | INTEGER (PK) |
| isbn | TEXT |
| title | TEXT |
| rating_average | REAL |

### movies - films issus du dataset IMDb, enrichis des données financières

| Colonne | Type |
|---------|------|
| id | INTEGER (PK) |
| title | TEXT |
| year | INTEGER |
| director | TEXT |
| rating | REAL |
| votes | INTEGER |
| metascore | REAL |
| budget | REAL |
| gross | REAL |
| profit | REAL |
| roi | REAL |

### book_movie_adaptations - liaison n-n entre livres et films

| Colonne | Type |
|---------|------|
| book_id | INTEGER (FK -> books.id) |
| movie_id | INTEGER (FK -> movies.id) |

Jointure sur les titres normalisés (minuscules, nettoyés) via jointure interne.

### series - séries issues des données OMDb

| Colonne | Type |
|---------|------|
| id | INTEGER (PK) |
| title | TEXT |
| year | INTEGER |
| rating | REAL |
| votes | INTEGER |
| total_seasons | INTEGER |

### book_series_adaptations - liaison n-n entre livres et séries

| Colonne | Type |
|---------|------|
| book_id | INTEGER (FK -> books.id) |
| series_id | INTEGER (FK -> series.id) |

## Pré-requis

- Python >= 3.13
- Gestionnaire de paquets `uv` (uv.lock fourni)
- Kaggle CLI pour l'étape 1 (compte Kaggle et identifiants API)
- Clé OMDb API dans `.env` pour l'étape 4

## Installation

```bash
uv venv
uv sync
```

## Orchestrateur

```bash
python main.py                          # transform + load uniquement
python main.py --with-extract           # pipeline complet
```
