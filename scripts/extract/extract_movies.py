import pandas as pd


df = pd.read_csv("data/raw/imdb_movie_dataset.csv")


def main():
    if df:
        print("IMDb dataset loaded :" + df.shape)
    else:
        print("Error while loading IMDb dataset")


if __name__ == "__main__":
    main()
