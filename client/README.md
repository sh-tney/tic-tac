# client
This subdirectory is both the logical place to store all of our client code. It is not linked directly to any of the VMs, and in fact, changing anything here will have no tangible effect on a live service. This is simply where one can see and edit the source code of the *ticTacClient.jar*. 

Any changes that one wishes to commit to their running webserver, will have to compile *ticTacClient.java*, run *makeJar.sh* to make a new jar file, and copy the resulting file over to */web/www/files/ticTacClient.jar*.
