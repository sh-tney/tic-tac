# Install updates, and then python, pip, and mysql-connector
apt-get update
apt-get install -y python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install mysql-connector

# This installs mysql so othat we can use it to run the first script
export MYSQL_PWD="mysql_root_pw"
echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
apt-get -y install mysql-server