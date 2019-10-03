# game
This subdirectory is both the logical place to store all of our game scripts, but also is the actual shared volume within the gameserver VM, which can be accessed via ```vagrant ssh gameserver```. Once inside the ssh client for the gameserver, you can navigate to this shared folder via ```cd /vagrant```, where you should see these exact contents.

Importantly for interacting with the gameserver here, in the *build-gameserver.sh* file is where some of the scripts in here are run on boot, and those wishing to change this behaviour should start there.

The remaining files in this directory are briefly outlined below, and some help with debugging is provided at the end.

## game_manager.py
This is the main server script, that is always run on booting the VM, and contains most of the networking logic involved, as well as the top-level command handling. Users who are looking to expand the game library available with their own files, provided they are already interfacing correctly via the other classes in this directory, will want to add these as via ```import``` in this file, as well as adding them to the ```cmdlist``` and ```game_list``` arrays, as detailed in the comments.

Beyond that, it is recomended that users do not touch the rest of this file unless they intend on adding additional command functions, or changing the entire logic of the gameserver in some way, such as enabling multi-threading. Changing behaviours in this file (other than extending the command list) will likely require further changing the rest of the files in this directory as well.

If one wants to change the port fowarding scheme in *Vagrantfile*, they may need to change the port used in this file as well.

## player.py & tttai.py
This is the only other place in this directory that in anyway cares about networking, and is likely unnneccesary to change outside of using some other kind of network encoding scheme. This class can easily be extended upon to include more variables if a developer wishes to have player objects store their own game information and this can easily be done without conflict, however interfering in any way with the included fields will likely break things in *game_manager.py*.

This class can also be extended to function as an AI opponent, as shown in *tttai.py*. By taking advantage of the ```sendUpdate``` function's ability to take in any message (to tell the AI of the internal state of the game); as well as return something (which a normal player object normally will not) to differentiate itself from a real player object. This requires a game class to handle it differently, even if this just means redirecting this return value to the normal response handling.

It's important to note here that such an AI opponent will not (and should not) be added to the *game_manager.py* ```player_list``` array, and as such will not naturally be updated by the server; These must be called directly from a game class, most likely in response to a player update, like in *ttt.py*.

## game.py & ttt.py 
This is where the logic for each independent lobby of the server is carried out, and will be expected to handle methods called by *game_manager.py*, and extending this class requires implementing all of the methods in this class, for *game_manager.py* to handle them correctly. User commands will always be passed to the game object directly by the server if the player's state indicates that they are in the corresponding "lobby", and should be handled as such.

  - ```addPlayer``` is somewhat self-explanatory, and usually can be passed to as-is, unless one wants to have some kind of extended logic run on-entry. 
  - ```removePlayer``` however is more important; in that this will be called not only if a player leaves willingly, but also if they disconnect unexpectedly. As such, appropriate handling and cleaning up of the game object's resources for that player needs to be accounted for here (This doesn't include the player object itself, or their networking information, this is handled in *game_manager.py*).
  - ```updatePlayers``` is also rather simple and can likely be passed to as-is, simply broadcasting the included message to all the listed players. 
  - ```updateGame``` is the other important part of game objects, as this will be called by *game_manager.py* in direct response to a player inside the game object's lobby sending anything to the server, and so this is where the vast majority of game logic will likely be carried out.
  
*game.py* on it's own acts as a functional public chat server, in which users' messages are broadcast to everyone, but also acts as the base class. *ttt.py* is an example of extending *game.py*, by creating a tic-tac-toe game lobby, in which users can either play against other opponents, or *tttai.py*.

## tttsql.py
This file specifically only interacts with *ttt.py*, acting as the mediator of the connection to the dbserver. It is not intended to be extended in any way, but can serve as an example structure for interacting with an SQL server in the this project. 

Changes to the networking of the *Vagrantfile*, or to the credentials of *build-dbserver.sh* will need to be updated here. Changes to the general structure of the database may also need to be reflected here.
