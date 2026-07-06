import pandas as pd


df = pd.read_csv("data/raw/movies.csv")


def main():
    if df is not None:
        print("Movie finance dataset loaded :" + str(df.shape))
    else:
        print("Error while loading movie finance dataset")


if __name__ == "__main__":
    main()
