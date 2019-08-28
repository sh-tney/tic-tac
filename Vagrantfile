# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagrantfile will set up three VMs on an internal network, with 
# assigned IPs: a webserver to hold the front-end web interface, a 
# database server to house player & match history data, and a game 
# server to hold the back end game logic computation & ai opponent hosting

Vagrant.configure("2") do |config|
  # ubuntu/xenial64, a popular box config that will provide us a familiar
  # linux back-end
  config.vm.box = "ubuntu/xenial64"

  # The database server configuration
  config.vm.define "dbserver" do |dbserver|
    # Connecting to the internal private network, so that our VMs can talk
    # to eachother, as well as port forwarding, so we can access the sql
    # server from outside (on a guest account with read-only privileges).
    dbserver.vm.hostname = "dbserver"
    dbserver.vm.network "private_network", ip: "192.168.2.11"

    # Setting up a shared folder, for the database script storage
    dbserver.vm.synced_folder "./db", "/vagrant",
      owner: "vagrant",
      group: "vagrant",
      mount_options: ["dmode=775,fmode=777"]

    # Runs a shell script from here once the VM has booted, to do our
    # in-house database set-up
    dbserver.vm.provision "shell", path: "./build-dbserver.sh"
  end

  # The webserver configuration
  config.vm.define "webserver" do |webserver|
    # Connect to the internal private network, so that our VMs can talk
    # to eachother, as well as port forwarding, so we can actually see 
    # the web interface from outside the VM, available publically, for
    # example via http://127.0.0.1:8080 locally.
    webserver.vm.hostname = "webserver"
    webserver.vm.network "forwarded_port", guest: 80, host: 8080
    webserver.vm.network "private_network", ip: "192.168.4.11"

    # Setting up a shared folder, for the webserver's assets
    webserver.vm.synced_folder "./web", "/vagrant", 
      owner: "vagrant", 
      group: "vagrant", 
      mount_options: ["dmode=775,fmode=777"]

    # Runs a shell script from here once the VM has booted, to do our
    # in-house set up for the webserver
    webserver.vm.provision "shell", path: "./build-webserver.sh"
  end
end
