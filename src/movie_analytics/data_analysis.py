import pandas as pd
from movie_analytics.database import get_engine

genres_list = ["Action", "Adventure", "Animation", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]

def analysis():

    engine = get_engine()
    movies_df = pd.read_sql("SELECT * FROM movies_full_dataset",engine)

    df_cleaned = movies_df.dropna(subset=["genres"]).copy()
    df_cleaned["genres_list"] = df_cleaned["genres"].str.split(',')
    df_cleaned["genres_weight"] = 1/df_cleaned["genres_list"].apply(len)
    df_exploded = df_cleaned.explode("genres_list")
    df = df_exploded.rename(columns={"genres_list":"genre","genres_weight":"genre_weight"})

    df_ratings = df.copy()
    df_ratings = df_ratings[df_ratings["genre"].isin(genres_list)]
    df_ratings = df_ratings.groupby("genre", as_index=False).agg(mean_rating=("avg_rating","mean"))[["genre","mean_rating"]]

    df_revenue_total = df.copy()
    df_revenue_total["weighted_revenue"] = df_revenue_total["revenue"]*df_revenue_total["genre_weight"]
    df_revenue_total = df_revenue_total.groupby("genre",as_index=False).agg(sum_weighted_revenue=("weighted_revenue","sum"))[["genre","sum_weighted_revenue"]]
    df_revenue_total["weighted_revenue_share"] = (df_revenue_total["sum_weighted_revenue"])*100/(df_revenue_total["sum_weighted_revenue"].sum())
    df_revenue_total = df_revenue_total[df_revenue_total["genre"].isin(genres_list)]

    df_revenue_trend = df.copy()
    df_revenue_trend["weighted_revenue"] = df_revenue_trend["revenue"]*df_revenue_trend["genre_weight"]
    df_revenue_trend = df_revenue_trend.groupby(["year","genre"],as_index=False).agg(sum_weighted_revenue=("weighted_revenue","sum"))[["year","genre","sum_weighted_revenue"]]
    df_revenue_trend["weighted_revenue_share"] = (df_revenue_trend["sum_weighted_revenue"])*100/(df_revenue_trend.groupby("year")["sum_weighted_revenue"].transform("sum"))
    df_revenue_trend = df_revenue_trend[df_revenue_trend["genre"].isin(genres_list)]

    df_ratings.to_sql("genre_ratings",con=engine,if_exists="replace",index=False)
    df_revenue_total.to_sql("genre_revenue_total",con=engine,if_exists="replace",index=False)
    df_revenue_trend.to_sql("genre_revenue_trend",con=engine,if_exists="replace",index=False)

if __name__ == "__main__":
    analysis()