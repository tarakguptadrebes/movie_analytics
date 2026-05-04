DROP TABLE IF EXISTS tmdb_movies_cleaned;

CREATE TABLE tmdb_movies_cleaned AS
	SELECT imdb_id,
		revenue,
		budget
	FROM tmdb_movies
	WHERE imdb_id IS NOT NULL
		AND revenue!=0
		AND budget!=0;

SELECT * FROM tmdb_movies_cleaned
	
	
	
