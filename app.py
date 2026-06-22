import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pandas as pd
import streamlit as st
import plotly.express as px
from movie_analytics.database import get_engine

st.set_page_config(page_title='Movie Analytics Dashboard', layout='wide')

st.title('Movie Analytics Dashboard')

@st.cache_resource
def get_db_engine():
    return get_engine()

@st.cache_data
def load_genre_ratings():
    return pd.read_sql('SELECT * FROM genre_ratings', get_db_engine())

@st.cache_data
def load_genre_revenue_total():
    return pd.read_sql('SELECT * FROM genre_revenue_total', get_db_engine())

@st.cache_data
def load_genre_revenue_trend():
    return pd.read_sql('SELECT * FROM genre_revenue_trend', get_db_engine())

genres_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller']
colors = ['#FF6B6B', '#51CF66', '#FFD43B', '#74C0FC', '#B197FC', '#FFA94D', '#63E6BE', '#F783AC', '#94D82D', '#3BC9DB', '#DA77F2']
genre_color_map = dict(zip(genres_list, colors))

df_ratings = load_genre_ratings()
df_revenue_total = load_genre_revenue_total()
df_revenue_trend = load_genre_revenue_trend()

selected_genres = st.multiselect(
    label='Filter Genres',
    options=genres_list,
    default=genres_list
)

df_filtered_ratings = df_ratings[df_ratings['genre'].isin(selected_genres)]
df_filtered_total = df_revenue_total[df_revenue_total['genre'].isin(selected_genres)]
df_filtered_trend = df_revenue_trend[df_revenue_trend['genre'].isin(selected_genres)]

dynamic_order = sorted(df_filtered_ratings['genre'].unique().tolist())

fig = px.bar(
    df_filtered_total,
    x='genre',
    y='weighted_revenue_share',
    title='Weighted Revenue Share by Genre (2000-2022)',
    labels={'genre': 'Genre', 'weighted_revenue_share': 'Weighted Revenue Share (%)'},
    color='genre',
    color_discrete_map=genre_color_map
)

fig.update_xaxes(
    range=[-0.5, len(genres_list) - 0.5] 
)

fig.update_layout(
    showlegend=False
)

st.plotly_chart(fig, width='stretch')

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

sort_metric = st.selectbox(
    "Order Box Plot By:",
    options=["Alphabetical","Median","IQR"]
)

df_stats = df_filtered_ratings.groupby('genre')['avg_rating'].agg(
    Median='median',
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75)
).reset_index()

df_stats['IQR'] = df_stats['Q3'] - df_stats['Q1']

if sort_metric == "Alphabetical":
    boxplot_order = sorted(df_filtered_ratings['genre'].unique().tolist())
elif sort_metric == "Median":
    boxplot_order = df_stats.sort_values(by='Median', ascending=False)['genre'].tolist()
elif sort_metric == "IQR":
    boxplot_order = df_stats.sort_values(by='IQR', ascending=False)['genre'].tolist()

fig = px.box(
    df_filtered_ratings, 
    x='avg_rating',
    y='genre',
    title='Ratings by Genre',
    labels={'avg_rating': 'Rating', 'genre': 'Genre'},
    color='genre',
    color_discrete_map=genre_color_map,
    category_orders={'genre': boxplot_order}
)

fig.update_layout(
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)