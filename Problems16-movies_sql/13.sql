-- list the names of all people who starred in a movie in which Kevin Bacon also starred.
-- Your query should output a table with a single column for the name of each person.
-- There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
-- Kevin Bacon himself should not be included in the resulting list.

SELECT DISTINCT people.name FROM people, movies, stars
WHERE movies.id = stars.movie_id
AND stars.person_id = people.id
AND people.name != "Kevin Bacon"
AND movies.title IN(SELECT DISTINCT movies.title FROM movies, stars, people
    WHERE movies.id = stars.movie_id
    AND stars.person_id = people.id
    AND people.name = "Kevin Bacon"
    AND people.birth = 1958);
