# Install updates, and then python, pip, and mysql-connector
apt-get update
apt-get install -y python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install mysql-connector

# Begin running the game manager
python3 /vagrant/game_manager.py > /home/vagrant/out.log &

# This runs the DEMO included in ttt, remove this line on release
python3 /vagrant/ttt.py > /home/vagrant/demo.log &