SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Drake');

-- -- Can't use JOIN here, JOIN is for insert something....
-- -- List all Drak song with song name and energy
-- -- SELECT songs.name, songs.energy, artists.name FROM songs JOIN artists ON artists.name = "Drake";
-- SELECT AVG(songs.energy) FROM songs JOIN artists ON artists.name = "Drake";
