SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = "Post Malone");

-- Find 'Post Malone' id from the artists table
-- SELECT id FROM artists WHERE name = 'Post Malone';


-- -- List snog name and Post Malone
-- -- Can't use JOIN here, JOIN is for insert something....
-- -- SELECT songs.name, artists.name FROM songs JOIN artists ON artists.name = "Post Malone";
-- -- SELECT songs.name FROM songs JOIN artists ON artists.name = "Post Malone";