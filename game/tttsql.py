import mysql.connector
import player
import sys

mydb = mysql.connector.connect(
  host="192.168.2.11",
  user="gameserver",
  passwd="game_pw",
  database="tictac_db"
)
db_cur = mydb.cursor()

def updateWin(p: str):
    db_cur.execute("SELECT id, win FROM players WHERE id='" + p.name + "'")
    result = db_cur.fetchall()
    if len(result) != 0:                  # If this player is already in our db
        for (name, win) in result:
            print(name, win)
            db_cur.execute("UPDATE players SET win=" + str(win+1) + \
                          " WHERE id='" + name + "'")
            print(name, "wins updated to", win+1)
    else:
        print("DB record not found for", p.name)
        db_cur.execute("INSERT INTO players VALUES ('" + p.name + "',1,0,0)")
        print("Record added")
    mydb.commit()

s = sys.stdin.read()
#print()
#print(s)
updateWin(player.player(name=s))