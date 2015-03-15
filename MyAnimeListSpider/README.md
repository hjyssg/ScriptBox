#####A Web spider for myanimelist.net


Iterate the whole website to get all anime information first

	php index.php > anime.txt

then parse the anime.txt and insert information into sqlite db "animeDB.sqlite"

	php parse_output.php


the db_setup.sql come with it to create tables.


*  run the program at midnight, otherwise the server will ban you.
*  it takes at 3 hours to iterate the website. Be aware. 


The outcome db has the Japan anime data from 1990 until now.