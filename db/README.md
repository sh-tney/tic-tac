 # db
 This subdirectory is both the logical place to store all of our database scripts, and also the actual shared volume inside the dbserver VM, which can be accessed via  ```vagrant ssh dbserver```. Once inside the ssh client for the dbserver, you can navigate this shared folder via ```cd /vagrant```, where you should see these exact contents. 
 
 Importantly for interacting with the dbserver here, in the *build-dbserver.sh* file in the top directory is where all the account credentials for the dbserver are located, and can be changed, but for easy access I've listed the defaults here. 
 
  - **Database Name:** tictac_db
  - **Root Password:** mysql_root_pw
  
  - ***Master Account:***
    - **Username:** dbserver
    - **Password:** db_pw
    - Full privileges on tictac_db, these credentials are stored in ```~/.my.cnf``` on boot (via the *build-dbserver.sh* script), and will be assumed by default when using the ```mysql``` command on this VM.
    
  - ***Read/Write Account:***
    - **Username:** gameserver
    - **Password:** game_pw
    - Only ```SELECT```, ```INSERT```, and ```UPDATE``` privileges on tictac_db, these are assumed by the gameserver, and so changing these credentials means you'll also have to edit */game/tttsql.py*.
    
  - ***Read-Only Account:***
    - **Username:** webserver
    - **Password:** web_pw
    - Only ```SELECT``` privileges on tictac_db, these are assumed by the webserver, and so changing these credentials means you'll also have to edit */web/www/index.php*.

## db-init.sql
This simple script intializes the single table of tictac_db, ```players```. This can easily be extended to have additional fields, however removing or altering the included fields will break things in */game/tttsql.py* and */web/www/index.php*.
