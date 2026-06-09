from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text
from movie_analytics.database import get_engine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQL_DIR = BASE_DIR / 'sql'

load_dotenv(BASE_DIR / '.env')

def run_sql():
    engine = get_engine()

    sql_files = [
        'title_basics_cleaned.sql',
        'title_ratings_cleaned.sql',
        'tmdb_movies_cleaned.sql',
        'movies_full_dataset.sql'
    ]

    with engine.begin() as conn:
        for sql_file in sql_files:
            sql_query = text((SQL_DIR / sql_file).read_text())
            conn.execute(sql_query)
            print(f"Executed {sql_file}")

if __name__ == '__main__':
    run_sql()