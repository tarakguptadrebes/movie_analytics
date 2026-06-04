DROP TABLE IF EXISTS title_ratings_cleaned;

CREATE TABLE title_ratings_cleaned AS
	SELECT tconst AS imdb_id,
		"averageRating" AS avg_rating,
		"numVotes" AS votes
	FROM title_ratings;

SELECT * FROM title_ratings_cleaned


