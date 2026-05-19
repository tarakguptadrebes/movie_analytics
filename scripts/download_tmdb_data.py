import kagglehub
import pandas as pd
import os
from movie_analytics.database import get_engine


def download():
    path = kagglehub.dataset_download("asaniczka/tmdb-movies-dataset-2023-930k-movies")
    print("Path to dataset files:", path)

    csv_path = os.path.join(path, "TMDB_movie_dataset_v11.csv")

    engine = get_engine()
    reader = pd.read_csv(csv_path, chunksize=100000)

    first_write = True

    for i, df in enumerate(reader):
        if not df.empty:
            if first_write:
                df.to_sql("tmdb_movies", con=engine, if_exists="replace", index=False)
                first_write = False
                print(f"Processed chunk {i+1}")
            else:
                df.to_sql("tmdb_movies", con=engine, if_exists="append", index=False)
                print(f"Processed chunk {i+1}")

if __name__ == "__main__":
    download()