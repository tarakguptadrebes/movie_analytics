from movie_analytics.download_title_basics import download_basics
from movie_analytics.download_title_ratings import download_ratings
from movie_analytics.download_tmdb_data import download_tmdb
from movie_analytics.run_sql import run_sql
from movie_analytics.data_analysis import analysis

def main():

    download_basics()
    download_ratings()
    download_tmdb()
    run_sql()
    analysis()

if __name__ == "__main__":
    main()