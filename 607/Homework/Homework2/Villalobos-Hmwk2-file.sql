-- loadvillalobos-movies.sql

# Create a new schema if it does not exists
CREATE SCHEMA IF NOT EXISTS `villalobos-movies`;
USE `villalobos-tblmoviesmovies`;

# Drop Tables if they exitst
DROP TABLE IF EXISTS tblUsers;
DROP TABLE IF EXISTS tblMovies;
DROP TABLE IF EXISTS tblMovies;
DROP TABLE IF EXISTS tblReviews;

# Create Tables
-- ----------------------------------------------
-- Table `users`
-- ----------------------------------------------
DROP TABLE IF EXISTS tblUsers; 
CREATE TABLE tblUsers
(
  user_id int PRIMARY KEY,
  fname varchar(30) NOT NULL
);
  
LOAD DATA INFILE 'c:/data/dvillalobos-movies/tblUsers.csv'
INTO TABLE tblUsers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM tblUsers;

-- ----------------------------------------------
-- Table `movies`
-- ----------------------------------------------
DROP TABLE IF EXISTS tblMovies;
CREATE TABLE tblMovies
(
  movie_id int PRIMARY KEY,
  title varchar(80) NOT NULL,
  lenght int NOT NULL
);
  
LOAD DATA INFILE 'c:/data/dvillalobos-movies/tblMovies.csv' 
INTO TABLE tblMovies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM tblMovies;


-- ----------------------------------------------
-- Table `reviews`
-- ----------------------------------------------
DROP TABLE IF EXISTS tblReviews;
CREATE TABLE tblReviews
(
  review_id int PRIMARY KEY,
  movie_id int NOT NULL REFERENCES tblMovies,
  user_id int NOT NULL REFERENCES tblUsers,
  rating int,
  review varchar(30) NOT NULL
);


LOAD DATA INFILE 'c:/data/dvillalobos-movies/tblReviews.csv' 
INTO TABLE tblReviews
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT * FROM tblReviews;


SET SQL_SAFE_UPDATES = 0;


/*
Report on Movie Reviews.
*/

SELECT 
M.title As 'Title',
M.lenght AS 'Lenght',
U.fname As 'User',
R.rating As 'Rating',
R.review AS 'Review'
FROM tblMovies AS M
JOIN tblReviews AS R
ON M.movie_id = R.movie_id
JOIN tblUsers AS U
ON U.user_id = R.user_id;

