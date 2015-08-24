#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")

def deleteMatches(*args):
	"""Remove all matches from a given tournament. Uses bleach and no parameter interpolation to eliminate SQL and CSS attacks.
	If no arguments are supplied, this deletes all matches
	"""
	DB = connect()
	c = DB.cursor()
	if not args:
		c.execute("DELETE FROM matches;")
	else:
		clean_Tournament = bleach.clean(args[0], strip=True)
		c.execute("DELETE FROM matches WHERE tournament = (%s)", (clean_Tournament,))
	DB.commit()
	DB.close()
	
def deletePlayers(*args):
	"""Remove all players from a given tournament (MUST BE STRING). Uses bleach and no parameter interpolation to eliminate SQL and CSS attacks.
	If no arguments are supplied, this deletes all matches
	"""
	DB = connect()
	c = DB.cursor()
	if not args:
		c.execute("DELETE FROM players;")
	else:
		clean_Tournament = bleach.clean(args[0], strip=True)
		c.execute("DELETE FROM players WHERE tournament = (%s)", (clean_Tournament,))
	DB.commit()
	DB.close()

def countPlayers(*args):
	"""Returns the number of players currently registered in a given tournament (MUST BE STRING). Uses bleach and no parameter interpolation to eliminate SQL and CSS attacks.
	If no arguments are supplied, this count all players registered for all tournaments.
	"""
	DB = connect()
	c = DB.cursor()
	if not args:
		c.execute("SELECT count(*) as count FROM players;")
	else:
		clean_Tournament = bleach.clean(args[0], strip=True)
		c.execute("SELECT count(*) as count FROM players WHERE tournament = (%s);",(clean_Tournament,))
	count = c.fetchone()
	DB.close()
	return count[0]

def registerPlayer(name,tournament):
	"""Adds a player to the tournament database.
	The database assigns a unique serial id number for the player.
	Args:
	name: the player's full name (need not be unique).
	tournament: the name of the tournament the player is in.
	  
	Uses bleach to eliminate any possibility of SQL injections. Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	clean_Name = bleach.clean(name, strip=True)
	clean_Tournament = bleach.clean(tournament, strip=True)
	DB = connect()
	c = DB.cursor()
	c.execute("INSERT INTO players(name, tournament) values(%s,%s)", (clean_Name,clean_Tournament,))
	DB.commit()
	DB.close()
	print str(clean_Name)+" has been added to the player registry for tournament "+str(clean_Tournament)+"..."
	
def playerStandings(*args):
	"""Returns a list of the players and their win records, sorted by wins, based on the tournament (MUST BE STRING)in args.
	If no tournament is supplied, then the playerStandings for all tournaments will be displayed
	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.
	Returns:
        A list of tuples, each of which contains (tournament, id, name, wins, matches):
        tournament: the name of the tournament the player is in
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
	Uses bleach to eliminate any possibility of SQL injections. Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	DB = connect()
	c = DB.cursor()
	if not args:
		c.execute("""SELECT * from v_player_record""")
	else:
		clean_tournament = bleach.clean(args[0], strip=True)
		c.execute("SELECT * from v_player_record where tournament = (%s);", (clean_tournament,))
	results = c.fetchall()
	DB.close()
	return results

def reportMatch(winner, loser, tournament):
	"""Records the outcome of a single match between two players.
	Args:
	winner:  the id number of the player who won
	loser:  the id number of the player who lost
	tournament: the tournament the match was played in
	Uses bleach to eliminate any possibility of SQL injections. Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	clean_winner = bleach.clean(winner, strip=True)
	clean_loser = bleach.clean(loser, strip=True)
	clean_tournament = bleach.clean(tournament, strip=True)
	DB = connect()
	c = DB.cursor()
	c.execute("INSERT INTO matches(winner,loser,tournament) values(%s,%s,%s);", (clean_winner,clean_loser,clean_tournament,))
	DB.commit()
	DB.close()
	print "Match between:"+clean_winner+" (winner) and "+clean_loser+" (loser) in Tournament: "+clean_tournament+" - has been added to the match registry..."
 
def swissPairings(tournament):
	"""Returns a list of pairs of players for the next round of a match in a tournament.
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
	Returns:
	A list of tuples, each of which contains (tournament, id1, name1, id2, name2)
	tournament: the name of the tournament the players are in
	id1: the first player's unique id
	name1: the first player's name
	id2: the second player's unique id
	name2: the second player's name
	"""
	standing_list = playerStandings(tournament)
	count = 0
	final_List = []
	while count < len(standing_list):
		final_List.append((standing_list[count][0],standing_list[count][1],standing_list[count][2],standing_list[count+1][1],standing_list[count+1][2]))
		count += 2
	return final_List

