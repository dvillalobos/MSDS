/*
School of Professional Studies - CUNY
Duubar Villalobos Jimenez
mydvtech@gmail.com
February 2017.

DATA 607 Week 2 Assignment SQL and R  
*/

 
  # I have created a new schema named "villalobos-movies" in order to do the work. I have set it as default.
  
  SELECT DATABASE();
  CREATE SCHEMA IF NOT EXISTS `villalobos-movies`;    
  USE `villalobos-movies`;
  

  
-- ----------------------------------------------
-- Table `users`
-- ----------------------------------------------
DROP TABLE IF EXISTS tblUsers; 
CREATE TABLE tblUsers
(
  user_id int PRIMARY KEY,
  fname varchar(30) NOT NULL
);

INSERT INTO tblUsers ( user_id, fname ) VALUES ( 1, 'Sarah');
INSERT INTO tblUsers ( user_id, fname ) VALUES ( 2, 'Maria');
INSERT INTO tblUsers ( user_id, fname ) VALUES ( 3, 'Elena');
INSERT INTO tblUsers ( user_id, fname ) VALUES ( 4, 'Diana');
INSERT INTO tblUsers ( user_id, fname ) VALUES ( 5, 'Michael');
INSERT INTO tblUsers ( user_id, fname ) VALUES ( 6, 'Heidy');

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

INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 1, 'Logan'            , 60  );
INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 2, 'Si3'              , 120 );
INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 3, 'Kung Fu Yoga'     , 141 );
INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 4, 'The Ghazi Attack' , 90  );
INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 5, 'Space'            , 121 );
INSERT INTO tblMovies ( movie_id, title, lenght) VALUES ( 6, 'Raees'            , 90  );

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

INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 1, 1, 1 , 5    , 'The Best'          );
INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 2, 1, 5 , 5    , 'Hala'              );
INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 3, 4, 4 , 3    , 'Horrible'          );
INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 4, 4, 4 , 4    , 'Historical'        );
INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 5, 3, 3 , NULL , 'Under rated'       );
INSERT INTO tblReviews ( review_id, movie_id, user_id, rating, review ) VALUES ( 6, 3, 1 , 4    , 'Really impressed'  );

SELECT * FROM tblReviews;

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
