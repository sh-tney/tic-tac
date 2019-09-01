<?php

if (!isset($_COOKIE['cookie']))
{
    header('Location: /index.php');
    exit;
}

?>
<!DOCTYPE html>
<html>
    <header>
        <h1>tic-tac</h1>
</header>
    <body>
    <?php
        $host    = "192.168.3.11";
        $port    = 6969;
        $message = "!name ".$_POST["username"];
        echo "Message To server :".$message."<br>";
        // create socket
        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
        // connect to server
        $result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");  
        // send string to server
        echo socket_read($socket, 1024) or die("Connection lost");
        socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
        // get server response
        $result = socket_read($socket, 1024) or die("Could not read server response\n");
        echo "Reply From Server  :".$result;
        // close socket
        socket_close($socket);
    ?>
</body>
</html>