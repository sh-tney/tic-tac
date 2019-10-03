# web
This subdirectory is both the logical place to store all of our web scripts, but also is the actual shared volume within the webserver VM, which can be accessed via ```vagrant ssh webserver```. Once inside the ssh client for the webserver, you can navigate to this shared folder via ```cd /vagrant```, where you should see these exact contents.

Importantly for interacting with the webserver here, in the *build-webserver.sh* file is where some of the scripts in here are run on boot, and those wishing to change this behaviour should start there.

The files in this directory are described as follows.

## test-website.conf
This file just changes some of the Apache server configuration such that log files are put into a sensible place (inside the shared volume folder), such that we can read them even if our VM dies.

## /www/index.php
This is our home webpage, where users will be directed. It accesses the dbserver to display user information, and as such any changes the networking of *Vagrantfile*, the credentials of *build-dbserver.sh*, or the general structure of the database will need to be reflected here. 

Also notable, this website contains a direct link to the following file, and changes to that file may also need to be reflected here.

## /www/files/ticTacClient.jar
This is a copy of */client/ticTacClient.jar*, which is in this folder so that the webserver can host the file directly for download. Changes to this file in the */client* directory will need to be copied over here as well.
