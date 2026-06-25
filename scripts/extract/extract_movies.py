import pandas as pd


df = pd.read_csv("data/raw/imdb_movie_dataset.csv")


def main():
    print(df.shape)


if __name__ == "__main__":
    main()
