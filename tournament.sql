-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- table players, making the ID the primary key. Using a combination of ID and Tournament as the primary key is not necessary.
create table players(
	ID serial primary key,
	name text,
	tournament text
);

create table matches(
	ID serial primary key,
	tournament text,
	winner int references players(id),
	loser int references players(id)
);

-- the view v_match_record returns a table of all Tournaments, ID's of players and their number of matches played, sorted first by number of matches, then alphabetically.
CREATE VIEW v_match_record AS
    SELECT players.tournament, players.id, COUNT(matches.id) AS matches 
    FROM players 
    LEFT JOIN matches ON (players.id = matches.WINNER OR players.id = matches.LOSER) AND players.tournament = matches.tournament
    GROUP BY players.tournament, players.id 
    ORDER BY matches DESC, players.id, players.tournament;
	
-- the view v_match_record returns a table of all ID's and their wins, sorted first by wins, then alphabetically.
CREATE VIEW v_win_record AS
    SELECT players.tournament, players.id, COUNT(matches.winner) AS wins 
	FROM players 
        LEFT JOIN matches ON (players.id = matches.winner AND players.tournament = matches.tournament)
    GROUP BY players.tournament, players.id, matches.winner 
    ORDER BY wins DESC, players.id, players.tournament;

-- the view v_player_record returns a table of all ID's, their names, wins, and number of matches played, sorted first by wins, then alphabetically.
CREATE VIEW v_player_record AS
    SELECT players.tournament, players.id, name, wins, matches
	    FROM players
		    JOIN v_win_record
			    ON (players.id = v_win_record.id AND players.tournament = v_win_record.tournament)
		    JOIN v_match_record
			    ON (players.id = v_match_record.id AND players.tournament = v_win_record.tournament)
    GROUP BY players.tournament, players.id, v_win_record.wins, v_match_record.matches
    ORDER BY wins desc, id, tournament;

-- For debugging purposes - this easily shows the names of the created tables in the database.
CREATE VIEW v_tables AS
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='public';

	-- For debugging purposes - this easily shows the names of the created tables in the database.
CREATE VIEW v_views AS
    SELECT table_name FROM INFORMATION_SCHEMA.views WHERE table_schema = ANY (current_schemas(false))
