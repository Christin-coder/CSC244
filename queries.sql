-- Basic queries on IMDB tables
SELECT * FROM directors;

SELECT * FROM directors WHERE first_name='Ricardo';


-- Basic queries on System tables
SELECT * FROM system.tables WHERE schema='IMDB'; 

SELECT COUNT(*) AS num_of_tables FROM system.tables; 

SELECT * FROM system.datatypes;


-- Procedure to get all the movies and roles of a given actor
@delimiter %%;
CREATE OR REPLACE PROCEDURE imdb.getActorMovies(IN inFname VARCHAR(100), IN inLname VARCHAR(100))
	RETURNS tmp_table(name VARCHAR(100), role VARCHAR(100))
AS
	INSERT INTO tmp_table
	SELECT name, roles.role
	  FROM movies, roles, actors
	 WHERE movies.id = roles.movie_id AND roles.actor_id = actors.id AND actors.first_name = inFname AND actors.last_name = inLname;
END_PROCEDURE; 
%%
@delimiter ; %%

execute imdb.getActorMovies('Tom', 'Cruise');


-- Procedure to get all the movies of a given director
@delimiter %%;
CREATE OR REPLACE PROCEDURE imdb.getDirectorMovies(IN inFname VARCHAR(100), IN inLname VARCHAR(100))
	RETURNS tmp_table(name VARCHAR(100), year INTEGER)
AS
	INSERT INTO tmp_table
	SELECT name, movies.year
	  FROM directors, movies_directors, movies
	 WHERE directors.id = movies_directors.director_id AND movies.id = movies_directors.movie_id AND directors.first_name = inFname AND directors.last_name = inLname;
END_PROCEDURE;
%%
@delimiter ; %%

execute imdb.getDirectorMovies('James (I)', 'Cameron');


-- Procedure to get all the actors of a given movie
@delimiter %%;
CREATE OR REPLACE PROCEDURE imdb.getMovieActors(IN inMovie VARCHAR(100), IN inYear INTEGER)
	RETURNS tmp_table(fname VARCHAR(100), lname VARCHAR(100), role VARCHAR(100))
AS
	INSERT INTO tmp_table
	SELECT first_name, last_name, role
	  FROM actors, roles, movies
	 WHERE actors.id = roles.actor_id AND roles.movie_id = movies.id AND movies.name = inMovie AND movies.year = inYear;
END_PROCEDURE;
%%
@delimiter ; %%

execute imdb.getMovieActors('Titanic', 1997);


-- Function that gets count of how many movies the given director has
@delimiter %%;
CREATE OR REPLACE FUNCTION imdb.howManyMoviesDirected (iFname VARCHAR(100), iLname VARCHAR(100)) RETURNS INTEGER
AS
    RETURN (SELECT count(*) 
    FROM directors JOIN movies_directors ON directors.id = movies_directors.director_id
    WHERE first_name = Ifname AND last_name = iLname);
END_FUNCTION;
%%
@delimiter ; %%

SELECT first_name, last_name, imdb.howManyMoviesDirected(first_name, last_name) FROM directors WHERE first_name = 'James (I)' and last_name = 'Cameron';


-- View of Actors, Roles, and Movies table
CREATE OR REPLACE VIEW actorsRolesMoviesView(first_name, last_name, role, name, year)
AS
    SELECT first_name, last_name, role, name, year
    FROM actors JOIN roles ON actors.id = actor_id JOIN movies ON movie_id = movies.id;
    
SELECT * FROM actorsRolesMoviesView;