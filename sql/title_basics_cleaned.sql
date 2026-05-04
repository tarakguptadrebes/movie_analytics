DROP TABLE IF EXISTS title_basics_cleaned;

CREATE TABLE title_basics_cleaned AS 
	SELECT
		tconst AS imdb_id,
		"primaryTitle" AS title,
		CAST("startYear" AS INT) AS year,
		genres
	FROM title_basics
	WHERE "titleType"='movie'
		AND "startYear" BETWEEN 2000 AND 2025;

SELECT * FROM title_basics_cleaned
