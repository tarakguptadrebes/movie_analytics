from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text
from movie_analytics.database import get_engine

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

engine = get_engine()

sql_files = [
    "title_basics_cleaned.sql",
    "title_ratings_cleaned.sql",
    "tmdb_movies_cleaned.sql",
    "movies_full_dataset.sql",
]

with engine.connect() as connection:
    with connection.begin():
        for sql_file in sql_files:
            with open(BASE_DIR /'sql' / sql_file, 'r') as file:
                sql_query = text(file.read())
                connection.execute(sql_query)
                print(f"Executed {sql_file}")
