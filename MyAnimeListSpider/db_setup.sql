-- USE FOR SQLITE


DROP TABLE animes;
DROP TABLE companies;
DROP TABLE genres;
DROP TABLE animes_companies;
DROP TABLE animes_genres;



CREATE TABLE animes (
     id INTEGER  PRIMARY KEY,
     name TEXT NOT NULL UNIQUE,
     romaji TEXT,
     type TEXT,
     rating TEXT,
     status TEXT,
     episodes INTEGER,
     minutes INTEGER,
     begin_date DATETIME DEFAULT NULL,
     end_date DATETIME DEFAULT NULL
    );


CREATE TABLE companies (
     id INTEGER  PRIMARY KEY,
     name text NOT NULL
    );

CREATE TABLE genres (
     id INTEGER  PRIMARY KEY,
     name text NOT NULL
    );

CREATE TABLE animes_companies (
     anime_id INTEGER,
     company_id INTEGER
    );




CREATE TABLE animes_genres (
     anime_id INTEGER,
     genre_id INTEGER
    );




