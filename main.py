from src.movie_analytics.download_title_basics import download_basics
from src.movie_analytics.download_title_ratings import download_ratings
from src.movie_analytics.download_tmdb_data import download_tmdb
from src.movie_analytics.run_sql import run_sql

def main():

    download_basics()
    download_ratings()
    download_tmdb()
    run_sql()

if __name__ == "__main__":
    main()