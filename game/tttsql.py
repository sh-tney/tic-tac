import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.2.11",
  user="gameserver",
  passwd="game_pw",
  database="tictac_db"
)
db_cur = mydb.cursor()

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM players WHERE id='fug'")

myresult = mycursor.fetchall()

if len(myresult) == 0:
    print('ey')

for (name, win, loss, draw) in myresult:
    print(name, win, loss, draw)