SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;



-- I misunderstood the question, it asking the longest song time not a longest name
-- SELECT name FROM songs ORDER BY LENGTH(name) DESC LIMIT 5;
-- order by length of name and longest to shortest
-- LIMIT 5 to show only 5 result

-- SELECT MAX(LENGTH(name)) FROM songs;
-- SELECT MAX(LENGTH(name)) ASC Longest FROM songs;
-- -- find the max length string and return length of string

-- SELECT name FROM songs WHERE LENGTH(name) = 55;
-- -- find the length of name = 55(longest in this library) and show the name of song

-- https://www.allthingssql.com/sql-max-min-column-length/