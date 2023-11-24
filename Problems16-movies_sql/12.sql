-- list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
-- Your query should output a table with a single column for the title of each movie.
-- You may assume that there is only one person in the database with the name Johnny Depp.
-- You may assume that there is only one person in the database with the name Helena Bonham Carter.


SELECT DISTINCT movies.title FROM movies, stars, people, ratings
WHERE movies.id = stars.movie_id
AND movies.id = ratings.movie_id
AND stars.person_id = people.id
AND people.name = "Johnny Depp" AND movies.title IN(
    SELECT movies.title FROM movies, stars, people, ratings
    WHERE movies.id = stars.movie_id
    AND movies.id = ratings.movie_id
    AND stars.person_id = people.id
    AND people.name = "Helena Bonham Carter");



