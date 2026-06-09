import pandas as pd
import streamlit as st
import plotly.express as px
from movie_analytics.database import get_engine

st.set_page_config(page_title='Movie Analytics Dashboard', layout='wide')

engine = get_engine()

st.title('Movie Analytics Dashboard')

@st.cache_data
def load_genre_ratings():
    return pd.read_sql('SELECT * FROM genre_ratings', engine)

@st.cache_data
def load_genre_revenue_total():
    return pd.read_sql('SELECT * FROM genre_revenue_total', engine)

@st.cache_data
def load_genre_revenue_trend():
    return pd.read_sql('SELECT * FROM genre_revenue_trend', engine)


genres_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller']

colors = ['#FF5252', '#38EF7D', '#FFD700', '#00E5FF', '#E040FB', '#FF9100', '#5C5CFF', '#FF4081', '#00F5D4', '#B388FF', '#CCFF00']

genre_color_map = dict(zip(genres_list, colors))



df_ratings = load_genre_ratings()

fig = px.box(
    df_ratings,
    x='genre', 
    y='avg_rating',
    title='Average Rating by Genre',
    labels={'genre': 'Genre', 'mean_rating': 'Average Rating'},
    color='genre',
    color_discrete_map=genre_color_map,
    category_orders={'genre': genres_list}
)

st.plotly_chart(fig, width='stretch')

df_revenue_total = load_genre_revenue_total()

fig = px.bar(
    df_revenue_total,
    x='genre',
    y='weighted_revenue_share',
    title='Weighted Revenue Share by Genre',
    labels={'genre': 'Genre', 'weighted_revenue_share': 'Weighted Revenue Share (%)'},
    color='genre',
    color_discrete_map=genre_color_map
)

st.plotly_chart(fig, width='stretch')

df_revenue_trend = load_genre_revenue_trend()

selected_genres = st.multiselect(
    label='Filter Genres',
    options=genres_list,
    default=genres_list
)

df_filtered_trend = df_revenue_trend[df_revenue_trend['genre'].isin(selected_genres)]

fig = px.line(
    df_filtered_trend,
    x='year',
    y='weighted_revenue_share',
    title='Weighted Revenue Share by Genre Over Time',
    labels={'year': 'Year', 'weighted_revenue_share': 'Weighted Revenue Share (%)', 'genre': 'Genre'},
    color='genre',
    color_discrete_map=genre_color_map
)

st.plotly_chart(fig, width='stretch')