import pandas as pd
import streamlit as st
import plotly.express as px
from movie_analytics.database import get_engine

st.set_page_config(page_title="Movie Analytics Dashboard",layout="wide")

engine = get_engine()

st.title("Movie Analytics Dashboard")

@st.cache_data
def load_genre_ratings():
    return pd.read_sql("SELECT * FROM genre_ratings",engine)

@st.cache_data
def load_genre_revenue_total():
    return pd.read_sql("SELECT * FROM genre_revenue_total",engine)

@st.cache_data
def load_genre_revenue_trend():
    return pd.read_sql("SELECT * FROM genre_revenue_trend",engine)


genres_list = ["Action", "Adventure", "Animation", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]

colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692", "#B6E880", "#FFD700", "#72B7B2", "#542788"]

genre_color_map = dict(zip(genres_list,colors))



df_ratings = load_genre_ratings()

fig=px.bar(df_ratings,
        x="genre", 
        y="mean_rating",
        color="genre",
        color_discrete_map=genre_color_map
    )
fig.update_yaxes(range=[5,7])

st.plotly_chart(fig, width='stretch')

df_revenue_total = load_genre_revenue_total()

fig = px.bar(
    df_revenue_total,
    x="genre",
    y="weighted_revenue_share",
    color="genre",
    color_discrete_map=genre_color_map
)

st.plotly_chart(fig, width='stretch')

df_revenue_trend = load_genre_revenue_trend()

selected_genres = st.multiselect(
    label="Filter Genres",
    options=genres_list,
    default=genres_list
)

df_filtered_trend = df_revenue_trend[df_revenue_trend["genre"].isin(selected_genres)]

fig = px.line(
    df_filtered_trend,
    x="year",
    y="weighted_revenue_share",
    color="genre",
    color_discrete_map=genre_color_map
)

st.plotly_chart(fig, width='stretch')