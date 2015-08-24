#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
	try:
		deleteMatches('Battle Royale')
		print "1. Old matches per tournament can be deleted"
	except:
		print "ERROR! cannot delete tournament specific matches! (Using tournament name 'Battle Royale')"
	deleteMatches()
	print "2. All old matches can be deleted (without args)."

def testDelete():
	deleteMatches()
	try:
		deletePlayers('Battle Royale')
		print "3. Players per tournament can be deleted"
	except:
		print "ERROR! cannot delete tournament specific players! (Using tournament name 'Battle Royale')"
	deletePlayers()
	print "4. All player records can be deleted (without args)."


def testCount():
	deleteMatches()
	deletePlayers()
	c = countPlayers()
	if c == '0':
		raise TypeError(
			"countPlayers() should return numeric zero, not string '0'.")
	if c != 0:
		raise ValueError("After deleting, countPlayers should return zero.")
	print "5. After deleting, countPlayers() (which counts all players) returns zero."

def testRegister():
	deleteMatches()
	deletePlayers()
	registerPlayer("Chandra Nalaar","Battle Royale")
	c = countPlayers()
	if c != 1:
		raise ValueError(
			"After one player registers, countPlayers() should be 1.")
	print "6. After registering a player, countPlayers() returns 1 (no args)."
	d = countPlayers("Battle Royale")
	if d != 1:
		raise ValueError(
			"After one player registered for Battle Royale, countTournamentPlayers('Battle Royale') should be 1.")
	print "7. This player is part of tournament 'Battle Royale'; countPlayers('Battle Royale') returns 1."

def testRegisterCountDelete():
	deleteMatches()
	deletePlayers()
	registerPlayer("Markov Chaney","Battle Royale")
	registerPlayer("Joe Malik","Battle Royale")
	registerPlayer("Mao Tsu-hsi","Whose Got the Best Badger?")
	registerPlayer("Atlanta Hope","Whose Got the Best Badger?")
	c = countPlayers()
	if c != 4:
		raise ValueError(
			"After registering four players, countPlayers should be 4.")
	deletePlayers("Whose Got the Best Badger?")
	c = countPlayers()
	if c != 2:
		raise ValueError(
			"After deleting from a tournament, countPlayers should be 2.")
	print "8. Players can be registered and deleted from a specific tournament."
	deletePlayers()
	c = countPlayers()
	if c != 0:
		raise ValueError("After deleting, countPlayers should return zero.")
	print "9. Players can be registered and deleted (no args)."

def testStandingsBeforeMatches():
	deleteMatches()
	deletePlayers()
	registerPlayer("Melpomene Murray", "The Dinkle Derby")
	registerPlayer("Randy Schwartz", "The Dinkle Derby")
	standings = playerStandings("The Dinkle Derby")
	if len(standings) < 2:
		raise ValueError("Players should appear in playerStandings even before "
						"they have played any matches.")
	elif len(standings) > 2:
		raise ValueError("Only registered players for the tournament 'The Dinkle Derby' should appear in standings.")
	if len(standings[0]) != 5:
		raise ValueError("Each playerStandings row should have five columns.")
	[(tournament1, id1, name1, wins1, matches1), (tournament2, id2, name2, wins2, matches2)] = standings
	if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
		raise ValueError(
			"Newly registered players should have no matches or wins.")
	if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
		raise ValueError("Registered players' names should appear in standings, "
						"even if they have no matches played.")
	print "10. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton", "Kitten Kombat")
    registerPlayer("Boots O'Neal", "Kitten Kombat")
    registerPlayer("Cathy Burton", "Kitten Kombat")
    registerPlayer("Diane Grant", "Kitten Kombat")
    standings = playerStandings("Kitten Kombat")
    [id1, id2, id3, id4] = [row[1] for row in standings]
    reportMatch(id1, id2, "Kitten Kombat")
    reportMatch(id3, id4, "Kitten Kombat")
    standings = playerStandings("Kitten Kombat")
    for (t, i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "11. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Leonardo", "TMNT Comeback Tour")
    registerPlayer("Donatello", "TMNT Comeback Tour")
    registerPlayer("Raphael", "TMNT Comeback Tour")
    registerPlayer("Michaelangelo", "TMNT Comeback Tour")
    standings = playerStandings("TMNT Comeback Tour")
    [id1, id2, id3, id4] = [row[1] for row in standings]
    reportMatch(id1, id2, "TMNT Comeback Tour")
    reportMatch(id3, id4, "TMNT Comeback Tour")
    pairings = swissPairings("TMNT Comeback Tour")
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(ptourn, pid1, pname1, pid2, pname2), (ptourn2, pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "12. After one match, players with one win are paired."


if __name__ == '__main__':
	testDeleteMatches()
	testDelete()
	testCount()
	testRegister()
	testRegisterCountDelete()
	testStandingsBeforeMatches()
	testReportMatches()
	testPairings()
	print "Success!  All tests pass!"


