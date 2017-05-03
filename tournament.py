#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(dbname="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=%s" % str(dbname))
    except:
        print("<Error: Unable to communicate with database: %s>" % str(dbname))

def deleteMatches():
    """Remove all the match records from the database.

    Returns the number of matches deleted.
    """
    sql = """DELETE FROM matches;"""
    conn = None
    rows_deleted = 0

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to delete matches: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

def deletePlayers():
    """Remove all the player records from the database.

    Returns the number of rows deleted
      (Note: truncate returns -1).
    """
    #sql = """DELETE FROM players;"""
    #deleteMatches()

    sql = """TRUNCATE players RESTART IDENTITY CASCADE;"""
    conn = None
    rows_deleted = 0

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to delete players: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted
    # truncate returns -1

def countPlayers():
    """Returns the number of players currently registered."""
    sql = """SELECT count(*) AS num FROM players;"""
    conn = None
    player_count = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        player_count = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to count players: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).

    Returns the ID of the new player.
    """
    sql = """INSERT INTO players(name)
             VALUES(%s) RETURNING id;"""
    conn = None
    player_id = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (name,))
        player_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to register player: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return player_id

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql = """SELECT * FROM view_standings"""
    conn = None
    standings = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        standings = cur.fetchall()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to get player standings: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    Returns the ID of the new match.
    """
    sql = """INSERT INTO matches(winner, loser)
             VALUES(%s, %s) RETURNING id;"""
    conn = None
    match_id = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (winner, loser))
        match_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("<Error: Unable to report match: %s>" % error)
    finally:
        if conn is not None:
            conn.close()

    return match_id

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairs = []

    for i in range(0, len(standings), 2):
        pair = (
            standings[i][0],
            standings[i][1],
            standings[i+1][0],
            standings[i+1][1]
        )
        pairs.append(pair)

    return pairs


