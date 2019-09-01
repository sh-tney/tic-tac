# Install updates, and then python
apt-get update
apt-get install -y python3

# Begin running the game manager
python3 /vagrant/game_manager.py > /vagrant/out.txt