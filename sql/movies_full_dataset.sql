DROP TABLE IF EXISTS movies_full_dataset;

CREATE TABLE movies_full_dataset AS
SELECT 
	tb.imdb_id,
	tb.title,
	tb.year,
	tb.genres,
	tr.avg_rating,
	tr.votes,
	tm.popularity,
	tm.revenue,
	tm.budget
FROM title_basics_cleaned AS tb
INNER JOIN title_ratings_cleaned AS tr
	ON tb.imdb_id=tr.imdb_id
INNER JOIN tmdb_movies_cleaned AS tm
	ON tb.imdb_id=tm.imdb_id
ORDER BY votes DESC;

SELECT * FROM movies_full_dataset


	