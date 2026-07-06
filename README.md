# Pipeline ETL Livres-Films (Adaptations)

Pipeline ETL qui télécharge et traite des jeux de données de livres et de films, identifie les adaptations littéraires au cinéma et en série, et charge les résultats dans une base SQLite.

## Jeux de données

| Fichier | Source | Description |
|---------|--------|-------------|
| `data/raw/top_1000_most_swapped_books.csv` | Kaggle (sergiykovalchuck/the-most-popular-books-for-exchanging) | 1000 livres populaires avec métadonnées incluant leur adaptation au cinéma |
| `data/raw/imdb_movie_dataset.csv` | Kaggle / IMDb (Yusuf Delikkaya, IMDB Movie Dataset) | 1000 films avec notes, votes, genres, réalisateur, casting |
| `data/raw/movies.csv` | Kaggle (Daniel Grijalva, Movie Industry) | Données financières des films (budget, recettes) |
| `data/raw/omdb_raw.json` | IMDb par OMDb API | Données enrichies (box-office, séries) via OMDb |

## Pipeline

| Phase | Scripts | Produit |
|-------|---------|---------|
| **Extract** | `extract_books.py`, `extract_movies.py`, `extract_movie_finance.py`, `extract_omdb_api.py` | Fichiers bruts dans `data/raw/` |
| **Transform** | `transform_books.py`, `transform_movies.py`, `transform_omdb_api.py`, `transform_series_movies_omdb.py`, `transform_movie_finance.py`, `transform_merge_movie_finance.py`, `transform_join_books_movies.py`, `transform_join_books_series.py` | Fichiers nettoyés dans `data/processed/` |
| **Load** | `load_data.py` | `database/cinema.db` |

Utilisez `main.py` pour exécuter la pipeline.

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

### book_movie_adaptations - liaison many-to-many entre livres et films

| Colonne | Type |
|---------|------|
| book_id | INTEGER (FK -> books.id) |
| movie_id | INTEGER (FK -> movies.id) |

Jointure sur les titres normalisés (minuscules, nettoyés) via inner merge.

### series - séries issues des données OMDb

| Colonne | Type |
|---------|------|
| id | INTEGER (PK) |
| title | TEXT |
| year | INTEGER |
| rating | REAL |
| votes | INTEGER |
| total_seasons | INTEGER |

### book_series_adaptations - liaison many-to-many entre livres et séries

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
