-- Scripts to create tables and import 'movies.csv'
    -- Create database "db_tts"
    -- Execute scripts below to create "t_movie" & "t_user"
    -- Import "movies.csv" to table:
        -- ex: COPY t_movie('all', 'columns', 'except', 'id') FROM 'pathtofile/filename.csv' DELIMITER ',' CSV HEADER;
        -- attention : must list all colums except 'id' which is generated automatically


-- Get contrib modules, if not already available : sudo apt-get install postgresql-contrib-9.4
DROP TABLE IF EXISTS t_movie;
CREATE EXTENSION "pgcrypto"; -- enable gen_random_uuid()
CREATE TABLE t_movie (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(50) UNIQUE,
    release_year INTEGER,
    production_company VARCHAR(255),
    distributor VARCHAR(50),
    director VARCHAR(255),
    writer VARCHAR(255),
    actor_1 VARCHAR(50),
    actor_2 VARCHAR(50),
    actor_3 VARCHAR(50),
    location_funfact JSON NOT NULL,
    movie_like_counter INTEGER,
    location_like_counter INTEGER
);


DROP TABLE IF EXISTS t_user;
CREATE TABLE t_user (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    mail VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    is_activated BOOLEAN NOT NULL,
    liked_movie_id UUID [],
    liked_location_id UUID []
);


-- COPY t_movie(title,release_year,production_company,distributor,director,writer,actor_1,actor_2,actor_3,location_funfact,movie_like_counter,location_like_counter) FROM '/Users/Jr/Documents/self_project/tonight_tomorrow_sanfrancisco/db_sql/movies.csv' DELIMITER ',' CSV HEADER;
