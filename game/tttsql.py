import mysql.connector
import player
import sys

"""Establishes a mysql connection, and from there waits for requests"""

mydb = mysql.connector.connect(
  host="tic-tac-1.cfcpvj1lhbvf.us-east-1.rds.amazonaws.com",
  user="gameserver",
  passwd="game_pw",
  database="tictac_db"
)
db_cur = mydb.cursor()

def updateWin(p: player.player):
    """Either adds 1 to a player's DB win-count, or makes a new player"""

    db_cur.execute("SELECT id, win FROM players WHERE id='" + p.name + "'")
    result = db_cur.fetchall()
    if len(result) != 0:                  # If this player is already in our db
        for (name, win) in result:
            db_cur.execute("UPDATE players SET win=" + str(win+1) + \
                          " WHERE id='" + name + "'")
            print(name, "wins updated to", win+1)
    else:                                          # Otherwise add a new record
        print("DB record not found for", p.name)
        db_cur.execute("INSERT INTO players VALUES ('" + p.name + "',1,0,0)")
        print("Record added")
    mydb.commit()

def updateLoss(p: player.player):
    """Either adds 1 to a player's DB loss-count, or makes a new player"""

    db_cur.execute("SELECT id, loss FROM players WHERE id='" + p.name + "'")
    result = db_cur.fetchall()
    if len(result) != 0:                  # If this player is already in our db
        for (name, loss) in result:
            db_cur.execute("UPDATE players SET loss=" + str(loss+1) + \
                          " WHERE id='" + name + "'")
            print(name, "losses updated to", loss+1)
    else:                                          # Otherwise add a new record
        print("DB record not found for", p.name)
        db_cur.execute("INSERT INTO players VALUES ('" + p.name + "',0,1,0)")
        print("Record added")
    mydb.commit()

def updateDraw(p: player.player):
    """Either adds 1 too a player's DB draw-count, or adds a new player"""
    
    db_cur.execute("SELECT id, draw FROM players WHERE id='" + p.name + "'")
    result = db_cur.fetchall()
    if len(result) != 0:                  # If this player is already in our db
        for (name, draw) in result:
            db_cur.execute("UPDATE players SET draw=" + str(draw+1) + \
                          " WHERE id='" + name + "'")
            print(name, "draws updated to", draw+1)
    else:                                          # Otherwise add a new record
        print("DB record not found for", p.name)
        db_cur.execute("INSERT INTO players VALUES ('" + p.name + "',0,0,1)")
        print("Record added")
    mydb.commit()