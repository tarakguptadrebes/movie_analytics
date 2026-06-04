import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from movie_analytics.database import get_engine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')

def download_ratings():
    engine = get_engine()
    url = "https://datasets.imdbws.com/title.ratings.tsv.gz"

    tmdb_df = pd.read_sql("SELECT imdb_id FROM tmdb_movies", engine)

    valid_ids = set(tmdb_df["imdb_id"].dropna().unique())

    reader = pd.read_csv(url, sep="\t", chunksize=100000, low_memory=False, na_values='\\N')

    first_write = True
    
    for i, df in enumerate(reader):

        df_filtered = df[df["tconst"].isin(valid_ids)]

        if not df_filtered.empty:
            if first_write:
                df_filtered.to_sql("title_ratings", con=engine, if_exists="replace", index=False)
                first_write = False
                print(f"Processed chunk {i+1}")
            else:
                df_filtered.to_sql("title_ratings", con=engine, if_exists="append", index=False)
                print(f"Processed chunk {i+1}")
        
if __name__ == "__main__":
    download_ratings()