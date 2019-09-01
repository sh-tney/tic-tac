<?php
if (isset($_COOKIE['cookie']))
{
    header('Location: /menu.php');
    exit;
}
?>
<!DOCTYPE html>
<html>
<body>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        Set your username here:<br>
        <input type="text" name="username"> 
        <input type="submit" value="Go!">
    </form>
    <?php
    if($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = "gay";
        $username = htmlspecialchars(stripcslashes(trim($_POST["username"])));
        if($username != "") {
            $username = str_replace(" ", "-", $username);
            $host = '192.168.3.11';
            $port = 6969;
            $sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP) or die("Couldn't create socket\n");
            socket_connect($sock, $host, $port) or die("Couldn't connect\n");
            $result = socket_read($sock, 1024) or die("Could not read response\n");
            echo $result."<br>";
            socket_write($sock, "!name ".$username);
            $result = socket_read($sock, 1024) or die("Could not read response\n");
            echo $result."<br>";
            socket_write($sock, "!quit");
            $result = socket_read($sock, 1024) or die("Could not read response\n");
            echo $result."<br>";
            $result = socket_read($sock, 1024) or die("Could not read response\n");
            echo $result."<br>";
            socket_close($sock);
        } else {
            echo "<p id=error>Invalid username</p>";
        }
    }
    ?>
</body>
</html> 