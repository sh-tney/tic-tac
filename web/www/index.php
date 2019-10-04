<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head><title>TicTac</title>
<style>

header {
  text-align: center;
  padding: 20px;
}
form {
  display: block;
  align: center;
  margin: 20px;
}
p { margin: 20px; }
th { text-align: left; }
table { 
  margin: 20px; 
}
table, th, td { 
  border: 2px solid grey;
  border-collapse: collapse;
}
th, td { padding: 5px; }
tr:hover { background-color: #f5f5f5; }

</style>
</head>

<header>
  <h1>TicTac Leaderboards & Info Page</h1>
</header>

<body>

<form action="index.php" method="POST">
  Search by Player Name: <input type="text" name="search">
  <input type="submit">
</form>

<table>

<tr><th>Players</th>
  <th>Wins</th>
  <th>Losses</th>
  <th>Draws</th>
  <th>Total</th>
  <th>Winrate</th>
  <th>Score</th></tr>

<?php
 
$db_host   = 'tic-tac-1.cfcpvj1lhbvf.us-east-1.rds.amazonaws.com';
$db_name   = 'tictac_db';
$db_user   = 'webserver';
$db_passwd = 'web_pw';
$pdo_dsn = "mysql:host=$db_host;dbname=$db_name";
$pdo = new PDO($pdo_dsn, $db_user, $db_passwd);

$search = "".$_POST['search'];

$q = $pdo->query(   # Pulls all the player's info, and generates useful numbers
  "SELECT ". 
  "id, win, loss, draw, ". 
  "(win+loss+draw) AS total, ".                       # Like total games played
  "((win*2)+draw)/((win+loss+draw)*2)*100 AS winrate, ".      # Average Winrate

  // This is the score/ranking generating method
  // Found at http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
  "ROUND((((((win*2)+draw) + 1.9208) / (((win*2)+draw) + loss) - ".
  "1.96 * SQRT((((win*2)+draw) * loss) / (((win*2)+draw) + loss) + 0.9604) / ".
  "(((win*2)+draw) + loss)) / (1 + 3.8416 / (((win*2)+draw) + loss)))*10000) ".
  "AS score ".

  "FROM players ".
  "WHERE id LIKE '%".$search."%'".           # This just facilitates the search
  "ORDER BY score DESC");

while($row = $q->fetch()){    # This loop just puts all our values on the table
  echo "<tr>".
       "<td>".$row["id"]."</td>".
       "<td>".$row["win"]."</td>".
       "<td>".$row["loss"]."</td>".
       "<td>".$row["draw"]."</td>".
       "<td>".$row["total"]."</td>".
       "<td>".$row["winrate"]."%</td>".
       "<td>".$row["score"]."</td>".
       "</tr>\n";
}

?>
</table>

<p> 
  Read about how this score was generated 
  <a href="http://www.evanmiller.org/how-not-to-sort-by-average-rating.html"
   target="_blank">here</a>.
  <br><br>
  Play via telnet, or via the java client 
  (<a href="https://tic-tac-client.s3.amazonaws.com/ticTacClient.jar" target="_blank">Direct Download Link</a>)
  at Port 6969
</p>

</body>
</html>