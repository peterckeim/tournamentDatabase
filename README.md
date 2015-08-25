# Tournament Database
Tournament Results Database -- Project 2 for Full-Stack Web Dev Udacity Program

**Assignment**

You will develop a database schema to store the game matches between players. You will then write a Python module to rank the players and pair them up in matches in a tournament.

---

The given files uses PostgreSQL object-relational database management system (ORDBMS) to create, store, organize, fetch, and update data for multiple Swiss-Style tournaments within a single database. Through using the library psycopg2, these files are able to use Python to add, gather, and manipulate data for several tournaments, while adhering to the rules for managing a basic Swiss-Style tournament (Read more on Swiss-Style Tournaments here https://en.wikipedia.org/wiki/Swiss-system_tournament).

###Please note:###
The following libraries and programs are required to use these series of files:

-*PostgreSQL* (http://www.postgresql.org/download/)

-*Python 2.7.1* (https://www.python.org/downloads/)

along with the following python library installed:

-*psycopg2* (http://initd.org/psycopg/download/ or 'pip install psycopg2' in cmd)

This file current cannot support odd numbered tournaments. Only an even amount of players in each tournament will parse correctly.
However, this database does support several tournaments without the need to reset all data for each tournament.

---

##Running the Program##

First, download this repository. You should only have 3 files in total:

_tournament.sql_, (Container of all SQL table and view initializations)

_tournament.py_, (The supplemental Python file containing methods to manipulate data)

_tournament_test.py_, (A testing file, giving examples of how the database works, and how its functions perform)

After you have PostgreSQL installed, enter your Shell of choice and navigate to your folder containing this .git repository.
Enter PostgreSQL while in the command prompt (psql) and perform the following commands to initialize the database

```
CREATE DATABASE tournament;
\c tournament
\i tournament.sql
```

This will create the database, connect you to it, and import the .sql configuration file, giving you access to all configured tables and views.
You have now successfully set up the database, and you are able to use the python functions found in tournament.py to manipulate and add data.

For examples of how the functions are used, please look in the _tournament_test.py_ file

Please note that per the functions, you MUST enter the name of the tournaments as parameters in the functions. However, most functions will still work without arguments, such as deleteMatches(), deletePlayers(), countPlayers() and playerStandings(). Please bear in mind the execution of parameter-less functions affects the whole database.
