-- list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
-- Your query should output a table with a single column for the title of each movie.
-- You may assume that there is only one person in the database with the name Chadwick Boseman.

SELECT movies.title FROM movies, stars, people, ratings WHERE movies.id = stars.movie_id AND movies.id = ratings.movie_id AND stars.person_id = people.id AND people.name = "Chadwick Boseman" ORDER BY rating DESC
LIMIT 5;


-- -- My final solution
-- SELECT movies.title FROM movies, stars, people, ratings
-- WHERE movies.id = stars.movie_id
-- AND movies.id = ratings.movie_id
-- AND stars.person_id = people.id
-- AND people.name = "Chadwick Boseman"
-- ORDER BY rating DESC
-- LIMIT 5;
-- -- +--------------------------+
-- -- |          title           |
-- -- +--------------------------+
-- -- | 42                       |
-- -- | Black Panther            |
-- -- | Marshall                 |
-- -- | Ma Rainey's Black Bottom |
-- -- | Get on Up                |
-- -- +--------------------------+
