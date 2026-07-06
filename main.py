import subprocess
import sys
import argparse
from pathlib import Path

# Racine du projet (le dossier contenant ce main.py)
ROOT = Path(__file__).parent

EXTRACT_STEPS = [
    "scripts/extract/extract_books.py",
    "scripts/extract/extract_movies.py",
    "scripts/extract/extract_movie_finance.py",
    "scripts/extract/extract_omdb_api.py",
]

TRANSFORM_STEPS = [
    "scripts/transform/transform_books.py",
    "scripts/transform/transform_movies.py",
    "scripts/transform/transform_omdb_api.py",
    "scripts/transform/transform_series_movies_omdb.py",    # -> movies_full_intermediate.csv, series_clean.csv
    "scripts/transform/transform_movie_finance.py",
    "scripts/transform/transform_merge_movie_finance.py",   # -> movies_full.csv (complet)
    "scripts/transform/transform_join_books_movies.py",      # -> join_books_movies.csv
    "scripts/transform/transform_join_books_series.py",      # -> join_books_series.csv
]

LOAD_STEPS = [
    "scripts/load/load_data.py",
]


def run_step(script_path: str):
    full_path = ROOT / script_path
    print(f"\n{'='*75}")
    print(f"-> Exécution : {script_path}")
    print(f"{'='*75}")

    result = subprocess.run(
        [sys.executable, str(full_path)],
        cwd=ROOT,
    )

    if result.returncode != 0:
        print(f"Échec à l'étape : {script_path}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Pipeline ETL book-movie-adaptation")
    parser.add_argument(
        "--with-extract",
        action="store_true",
        help="Relance aussi les scripts d'extraction (extract_*.py). Désactivé par défaut.",
    )
    args = parser.parse_args()

    pipeline = []
    if args.with_extract:
        pipeline += EXTRACT_STEPS
    else:
        print("  Extracts ignorés (utilise --with-extract pour les relancer).")

    pipeline += TRANSFORM_STEPS + LOAD_STEPS

    for step in pipeline:
        run_step(step)

    print("\n Pipeline terminé avec succès.")


if __name__ == "__main__":
    main()