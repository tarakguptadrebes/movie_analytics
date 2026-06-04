# Movie Analytics

## Prerequisites

- Python 3.11+
- PostgreSQL
- Poetry installed (https://python-poetry.org/docs/#installation)

## Setup

```bash
# Clone the repository
git clone https://github.com/tarakguptadrebes/movie_analytics.git
cd movie_analytics

# Install dependencies
poetry install

# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE movies_db;"

# Initialize credentials
cp .env.example .env
# STOP: Open .env and enter your PostgreSQL password now!
```

## Run Project

```bash
# Load and transform data
poetry run python main.py

# Launch dashboard
poetry run streamlit run app.py
```