<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head><title>Database test page</title>
<style>
th { text-align: left; }

table, th, td {
  border: 2px solid grey;
  border-collapse: collapse;
}

th, td {
  padding: 0.2em;
}
</style>
</head>

<body>
<h1>Database test page</h1>

<p>Showing contents of papers table:</p>

<table border="1">
<tr><th>Players</th>
  <th>Wins</th>
  <th>Losses</th>
  <th>Draws</th>
  <th>Total</th>
  <th>Winrate</th>
  <th>Score</th></tr>

<form action="index.php" method="POST">
  Search by Player Name: <input type="text" name="search">
  <input type="submit">
</form>

<?php
 
$db_host   = '192.168.2.11';
$db_name   = 'tictac_db';
$db_user   = 'webserver';
$db_passwd = 'web_pw';
$pdo_dsn = "mysql:host=$db_host;dbname=$db_name";
$pdo = new PDO($pdo_dsn, $db_user, $db_passwd);

$search = "".$_POST['search'];

$q = $pdo->query(
  "SELECT ". 
  "id, win, loss, draw, ". 
  "(win+loss+draw) AS total, ".
  "((win*2)+draw)/((win+loss+draw)*2)*100 AS winrate, ".

  // This is the score/ranking generating method
  // Found at http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
  "((((win*2)+draw) + 1.9208) / (((win*2)+draw) + loss) - ".
  "1.96 * SQRT((((win*2)+draw) * loss) / (((win*2)+draw) + loss) + 0.9604) / ".
  "(((win*2)+draw) + loss)) / (1 + 3.8416 / (((win*2)+draw) + loss)) ".
  "AS score ".

  "FROM players ".
  "WHERE id LIKE '%".$search."%'".
  "ORDER BY score DESC");

while($row = $q->fetch()){
  echo "<tr><td>".$row["id"].
       "</td><td>".$row["win"]."</td>".
       "<td>".$row["loss"]."</td>".
       "<td>".$row["draw"]."</td>".
       "<td>".$row["total"]."</td>".
       "<td>".$row["winrate"]."%</td>".
       "<td>".$row["score"]."</td></tr>\n";
}

?>
</table>
</body>
</html>