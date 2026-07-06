import pandas as pd
from rapidfuzz import process, fuzz

FUZZY_THRESHOLD = 85  # score de similarité minimum (0-100) pour accepter un match approximatif


df_books = pd.read_csv("data/processed/books_clean.csv")
df_series = pd.read_csv("data/processed/series_clean.csv")

df_series_final = df_series.reset_index().rename(columns={"index": "id"})

df_books_subset = df_books[["title", "id"]].rename(columns={"id": "book_id"})
df_series_subset = df_series_final[["title", "id"]].rename(columns={"id": "series_id"})

# Clé de matching normalisée (comme pour movies, pour capter les écarts de ponctuation)
df_books_subset["title"] = df_books_subset["title"].str.lower().str.strip()
df_series_subset["title"] = df_series_subset["title"].str.lower().str.strip()

# df_matching_ids = df_books_subset.merge(
#     df_series_subset, on="title", how="inner", suffixes=("_book", "_series")
# )

# df_book_series_adaptations = df_matching_ids[["book_id", "series_id"]]


# def export(df, path):
#     df.to_csv(path, index=False)


# def main():
#     export(df_book_series_adaptations, "data/processed/join_books_series.csv")


# if __name__ == "__main__":
#     main()

# --- 1. Matching exact ---
df_exact = df_books_subset.merge(
    df_series_subset, on="title", how="inner", suffixes=("_book", "_series")
)
df_exact = df_exact[["book_id", "series_id"]]
matched_book_ids = set(df_exact["book_id"])

print(f"   -> {len(df_exact)} correspondances exactes trouvées.")

# --- 2. Matching approximatif (fuzzy) pour les livres non matchés ---
series_titles = df_series_subset["title"].tolist()
fuzzy_matches = []

remaining_books = df_books_subset[~df_books_subset["book_id"].isin(matched_book_ids)]

for _, book_row in remaining_books.iterrows():
    best_match = process.extractOne(
        book_row["title"], series_titles, scorer=fuzz.token_sort_ratio
    )
    if best_match is not None:
        matched_title_key, score, idx = best_match
        if score >= FUZZY_THRESHOLD:
            series_row = df_series_subset.iloc[idx]
            fuzzy_matches.append({
                "book_id": book_row["book_id"],
                "series_id": series_row["series_id"],
                "book_title": book_row["title"],
                "series_title": series_row["title"],
                "score": score,
            })

df_fuzzy = pd.DataFrame(fuzzy_matches)

if len(df_fuzzy) > 0:
    print(f"   -> {len(df_fuzzy)} correspondances approximatives trouvées (seuil >= {FUZZY_THRESHOLD}) :")
    print(df_fuzzy[["book_title", "series_title", "score"]].to_string(index=False))
else:
    print("   -> Aucune correspondance approximative trouvée.")

# --- 3. Fusion des deux résultats ---
df_book_series_adaptations = pd.concat(
    [df_exact, df_fuzzy[["book_id", "series_id"]] if len(df_fuzzy) > 0 else pd.DataFrame(columns=["book_id", "series_id"])],
    ignore_index=True,
)


def export(df, path):
    df.to_csv(path, index=False)


def main():
    export(df_book_series_adaptations, "data/processed/join_books_series.csv")


if __name__ == "__main__":
    main()