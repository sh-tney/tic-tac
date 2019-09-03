# First update software packages
apt-get update

# Create a MySQL root password to be subsequently used while installing
# Be sure to change this in actual deployment to something private
export MYSQL_PWD="mysql_root_pw"
echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
apt-get -y install mysql-server

#  ************
#   On release, change all the passwords in here to something more secure
#  ************

# Now create and initialise the database, and a user with privileges
echo "CREATE DATABASE tictac_db;" | mysql
echo "CREATE USER 'dbserver'@'%' IDENTIFIED BY 'db_pw';" | mysql
echo "GRANT ALL PRIVILEGES ON tictac_db.* TO 'dbserver'@'%';" | mysql

# Create user for the game server, with row-level read/write privileges
echo "CREATE USER 'gameserver'@'%' IDENTIFIED BY 'game_pw';" | mysql
echo "GRANT SELECT, INSERT, UPDATE ON tictac_db.* TO 'gameserver'@'%';" | mysql

# Create user for the web server, with read-only privileges
echo "CREATE USER 'webserver'@'%' IDENTIFIED BY 'web_pw';" | mysql
echo "GRANT SELECT ON tictac_db.* TO 'webserver'@'%';" | mysql

# Switch to the local (non-root) db user, an run structural setup
export MYSQL_PWD="db_pw"
echo "source /vagrant/db-init.sql" | mysql -u dbserver tictac_db

# This just adds a conveniece option for being able to SSH into the dbserver,
# and go straight into mysql and start working on things
echo "[client]
user=dbserver
password=db_pw" > /home/vagrant/.my.cnf

# By default, MySQL only listens for local network requests,
# i.e., that originate from within the dbserver VM. We need to
# change this so that the webserver VM can connect to the
# database on the dbserver VM. Use of `sed` is pretty obscure,
# but the net effect of the command is to find the line
# containing "bind-address" within the given `mysqld.cnf`
# configuration file and then to change "127.0.0.1" (meaning
# local only) to "0.0.0.0" (meaning accept connections from any
# network interface).
sed -i'' -e '/bind-address/s/127.0.0.1/0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# We then restart the MySQL server to ensure that it picks up
# our configuration changes.
service mysql restart