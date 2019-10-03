# tic-tac
A lightweight turn-based game host, built on Vagrant.

## how to use

### server:
All you need to get started here is to have Vagrant installed (https://www.vagrantup.com/)
 - Navigate into this repository's folder and run ```vagrant up```.
 - That's it.
 
### clients:
All you need to get started here is Java
 - Go to your web browser and navigate to ```hostname:8080``` where hostname is just wherever the server is running.
 - From here, you can see the scores of the sample players, and download the Java client.
   - You can also just your own favourite TCP client for this, like PuTTY (https://www.putty.org) or just ```telnet```
 - Connect to ```hostname:6969```, and you'll be greeted by the gamesever's list of commands, from which you can get chatting with your friends, or grinding to rise on the tic-tac-toe ladder.

## for developers
This section covers the basics of modifying this package. Within the folders you'll find more detailed explanations of the files in those folders; But here is where we'll discuss the top-level files and folders.

### folders
Each of the folders at this level divide nicely into the roles of the respective VMs that vagrant will be running, and each of these folders are used as shared volumes with its respective VM also. So all of the files in game are accessible from within the gameserver VM. 

The exception to this is the client folder, which is not linked to any VM, and simply contains the source code of the Java TCP client, however a copy of the jar file in this directory is also inside the web subdirectory, as the webserver hosts the client jar so that it can be downloaded from the website. Naturally this means that compiling and changing the client in any way will also mean taking a new copy into the webserver, if you want a modified client to be distributed on the webserver.

### .gitignore & .gitattributes
These files are some simple housekeeping for the git project, .gitignore was generated from https://www.gitignore.io/, notably having been modified to allow uploading jar files (so that the client jar is ready to deploy straight from booting up vagrant). .gitattributes is a neccesity for ensuring all our files that are going to be run inside the VMs always checkout with unix line endings, as they run on an Ubuntu box, regardless of our external OS choices.

### Vagrantfile & build-xxx.sh
This file is the simple heart of the vagrant VMs, and is run during the initial ```vagrant up```, this builds each VM in the order:
 1. dbserver (this one comes first, as the other two servers depend on it)
 2. gameserver 
 3. webserver
In this order, each VM initialises it's own private network address and port forwarding schemes, which can be altered here, as well as any neccesary file mounting permissions, and then finally runs its own corresponding setup script, found here in the respective build-xxx.sh file.
