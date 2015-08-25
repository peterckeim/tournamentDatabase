-- THIS MUST BE EXECUTED OUTSIDE OF THE tournament DATABASE IN PSQL. DO NOT \c tournament BEFORE IMPORTING THIS.
-- as deleting, remaking, and connecting to the tournament database are the first steps of this import!

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- This table must be made first in the .sql file due to dependencies in players and matches.
create table tournaments(
	ID serial primary key,
	name text
);
-- table of players, making the ID the primary key.
create table players(
	ID serial primary key,
	name text,
	tournament_id int references tournaments(id)
);
-- table of matches, where the winners and losers are the IDs of the players. This will be used in aggregation of wins.
create table matches(
	ID serial primary key,
	tournament_id int references tournaments(id),
	winner int references players(id),
	loser int references players(id)
);

--Test Data: Uncomment this to populate data with 2 tournaments, 4 players each, which 2 rounds played. This is useful to test the v_player_record view.
-- insert into tournaments(name) values('Tourney1');
-- insert into tournaments(name) values('Tourney2');

-- insert into players(name,tournament_id) values('Abby',1);
-- insert into players(name,tournament_id) values('Bobby',1);
-- insert into players(name,tournament_id) values('Cassidy',1);
-- insert into players(name,tournament_id) values('Daniel',1);
-- insert into players(name,tournament_id) values('Erik',2);
-- insert into players(name,tournament_id) values('Fredrik',2);
-- insert into players(name,tournament_id) values('Gustav',2);
-- insert into players(name,tournament_id) values('Hans',2);

-- insert into matches(tournament_id, winner, loser) values(1,1,2);
-- insert into matches(tournament_id, winner, loser) values(1,3,4);
-- insert into matches(tournament_id, winner, loser) values(1,1,3);
-- insert into matches(tournament_id, winner, loser) values(1,2,4);
-- insert into matches(tournament_id, winner, loser) values(2,5,6);
-- insert into matches(tournament_id, winner, loser) values(2,7,8);
-- insert into matches(tournament_id, winner, loser) values(2,5,7);
-- insert into matches(tournament_id, winner, loser) values(2,6,8);

-- the view v_match_record returns a table of all Tournaments ID's, ID's of players and their number of matches played, sorted first by number of matches, then alphabetically.
CREATE VIEW v_match_record AS
    SELECT players.tournament_id, players.id, COUNT(matches.id) AS matches 
    FROM players 
    LEFT JOIN matches ON (players.id = matches.WINNER OR players.id = matches.LOSER) AND players.tournament_id = matches.tournament_id
    GROUP BY players.tournament_id, players.id 
    ORDER BY players.tournament_id, matches DESC, players.id;
	
-- the view v_match_record returns a table of all ID's and their wins, sorted first by wins, then alphabetically.
CREATE VIEW v_win_record AS
    SELECT players.tournament_id, players.id, COUNT(matches.winner) AS wins 
	FROM players 
        LEFT JOIN matches ON (players.id = matches.winner AND players.tournament_id = matches.tournament_id)
    GROUP BY players.tournament_id, players.id, matches.winner 
    ORDER BY players.tournament_id, wins DESC, players.id;

-- the view v_player_record returns a table of all Tournament names, the ID's participating within them, their names, wins, and number of matches played, 
-- sorted first by wins, then alphabetically.
CREATE VIEW v_player_record AS
    SELECT tournaments.name as tournament, players.id, players.name, wins, matches
	    FROM players
		    JOIN v_win_record
			    ON (players.id = v_win_record.id AND players.tournament_id = v_win_record.tournament_id)
		    JOIN v_match_record
			    ON (players.id = v_match_record.id AND players.tournament_id = v_win_record.tournament_id)
			JOIN tournaments
				ON tournaments.id = players.tournament_id
    GROUP BY tournaments.name, players.id, v_win_record.wins, v_match_record.matches
	ORDER BY tournament, wins desc, id;

-- For debugging purposes - this easily shows the names of the created tables and views in the database.
CREATE VIEW v_tablesviews AS
	SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='public' 
	UNION SELECT table_name FROM INFORMATION_SCHEMA.views WHERE table_schema = ANY (current_schemas(false)) ORDER BY TABLE_NAME; 

