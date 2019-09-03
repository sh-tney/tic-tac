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
