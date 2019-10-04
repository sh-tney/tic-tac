# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # Online Vagrantfile documentation is at https://docs.vagrantup.com.

  # The AWS provider does not actually need to use a Vagrant box file.
  config.vm.box = "dummy"

  config.vm.provider :aws do |aws, override|
    # We will gather the data for these three aws configuration
    # parameters from environment variables (more secure than
    # committing security credentials to your Vagrantfile).
    aws.access_key_id = ENV['AWS_ACCESS_KEY_ID']
    aws.secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
    aws.session_token = ENV['AWS_SESSION_TOKEN']

    # The keypair_name parameter tells Amazon which public key to use.
    aws.keypair_name = "ticTac"
    override.ssh.private_key_path = "~/.ssh/ticTac.pem"
    override.ssh.username = "ubuntu"

    # The region for Amazon Educate is fixed.
    aws.region = "us-east-1" # Only Amazon Educate Region
    aws.availability_zone = "us-east-1a" 
    aws.subnet_id = "subnet-032a69b4c8adfce7a"
    aws.security_groups = ["sg-0474ca855d8035dc7"] # Open-SG

    # Choosing the starting software, and mounting materials
    aws.instance_type = "t2.micro"
    aws.ami = "ami-04763b3055de4860b"
    override.nfs.functional = false
    override.vm.allowed_synced_folder_types = :rsync
  end

  # Web-specific modifications, mostly just to starting resources
  config.vm.define "webserver" do |webserver|
    webserver.vm.synced_folder "./web", "/vagrant", 
      owner: "ubuntu",
      group: "ubuntu"
    webserver.vm.provision "shell", path: "./build-webserver.sh"
  end

  # Game-specific modifications, mostly just to starting resources
  config.vm.define "gameserver" do |gameserver|
    gameserver.vm.synced_folder "./game", "/vagrant", 
      owner: "ubuntu",
      group: "ubuntu"
    gameserver.vm.provision "shell", path: "./build-gameserver.sh"
  end

end
