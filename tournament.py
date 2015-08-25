#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def execute_query(query, variables=(), fetch=False, commit=False):
	"""Provides an easy way to connect to the PostgreSQL database, and execute a query based on a supplied
	args:
	query - the PostgreSQL query which will be executed
	variables - a tuple of variables to use. In many cases it would be player ID's, and tournament names
	fetch - default false -- if set to true, this would fetch and return data executed by the query, else return none.
	commit - default false -- if set to true, this will commit changes to the database after the query execution.
	"""
	# connects to the database then makes a cursor attached to it to perform manipulations and hold data flow.
	conn = psycopg2.connect("dbname=tournament")
	cur = conn.cursor()
	# executes the given query
	cur.execute(query,variables)
	# if the fetch parameter is true, fetch whatever data was pulled from the query (usually where a SELECT query is made)
	if fetch: fetched = cur.fetchall()
	else: fetched = None
	# if commit is true, the database will commit any changes made with the query.
	if commit: conn.commit()
	conn.close()
	return fetched	
	
def deleteMatches(*args):
	"""Remove all matches from a given tournament. Uses no parameter interpolation to eliminate SQL injection attacks.
	If no arguments are supplied, this deletes all matches
	"""
	if not args:
		# if there are no args given, delete all matches from the matches table
		execute_query("DELETE FROM matches;", commit = True)
	else:
		# if there args given (which must be a string of the tournament name), deletes all matches belonging to a given tournament from the matches table
		execute_query("DELETE FROM matches WHERE tournament = (%s)",(args[0],),commit = True)
	
def deletePlayers(*args):
	"""Remove all players from a given tournament (MUST BE STRING). Uses bleach and no parameter interpolation to eliminate SQL and CSS attacks.
	If no arguments are supplied, this deletes all matches
	"""
	if not args:
		# if there are no args give, delete all players from the players table
		execute_query("DELETE FROM players;", commit = True)
	else:
		# if there args given (which must be a string of the tournament name), deletes all players belonging to a given tournament from the players table.
		execute_query("DELETE FROM players WHERE tournament = (%s)", (args[0],),commit = True)

def countPlayers(*args):
	"""Returns the number of players currently registered in a given tournament (MUST BE STRING). Uses no parameter interpolation to eliminate SQL attacks.
	If no arguments are supplied, this counts all players registered for all tournaments.
	"""
	if not args:
		# if there are no arguments given, return count of all players
		count = execute_query("SELECT count(*) as count FROM players;", fetch = True)
	else:
		# if there are arguments (which must be a string of the tournament name), returns count of all players in the given tournament
		count = execute_query("SELECT count(*) as count FROM players WHERE tournament = (%s);", (args[0],),True)
	# because the returned data will be in a tuple within a tuple, this accesses the only value, which should be the value of the count.
	return count[0][0]

def registerPlayer(name,tournament):
	"""Adds a player to the tournament database.
	The database assigns a unique serial id number for the player.
	Args:
	name: the player's full name (need not be unique).
	tournament: the name of the tournament the player is in.
	  
	Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	execute_query("INSERT INTO players(name, tournament) values(%s,%s);",(name,tournament,),commit = True)
	print str(name)+" has been added to the player registry for tournament "+str(tournament)+"..."
	
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
	Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	if not args:
		# if there are no arguments given, return the standings for all players
		execute_query("SELECT * from v_player_record", fetch = True)
	else:
		# if there are arguments (which must be a string of the tournament name), returns standing of all players in the given tournament.
		results = execute_query("SELECT * from v_player_record where tournament = (%s);", (args[0],),True)
	return results

def reportMatch(winner, loser, tournament):
	"""Records the outcome of a single match between two players.
	Args:
	winner:  the id number of the player who won
	loser:  the id number of the player who lost
	tournament: the tournament the match was played in
	Does not use string parameter interpolation to eliminate any possibility of CSS attacks.
	"""
	execute_query("INSERT INTO matches(winner,loser,tournament) values(%s,%s,%s);", (winner, loser, tournament,), commit = True)
	print "Match between:"+str(winner)+" (winner) and "+str(loser)+" (loser) in Tournament: "+tournament+" - has been added to the match registry..."
 
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
	# NOTE: This only works if there are an even number of players in the given tournament, 
	# or if no args are passed, there must be an even number of players in the players table.
	
	# standing_list fetches the list of tuples generated from playerStandings. It is ordered by wins descending, so the strongest will always be at the top. 
	standing_list = playerStandings(tournament)
	# creates a count variable which will be used to iterate through the list. Once count = the list's length, the while loop will terminate.
	count = 0
	# the final_List is the list of tuples showing which pairs of players will face each other in the next round.
	final_List = []
	while count < len(standing_list):
		# grabs the tuples at count and count + 1 (the reason this only works with an even number of players now) and pits them against each other in the final_list,
		# then increases count by two and repeats the loop
		final_List.append((standing_list[count][0],standing_list[count][1],standing_list[count][2],standing_list[count+1][1],standing_list[count+1][2]))
		count += 2
	# the final list contains (tournament name, contender, contender's name, opponent, opponent's name)
	return final_List

