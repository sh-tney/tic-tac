# First update software packages
apt-get update

# Create a MySQL root password to be subsequently used while installing
# Be sure to change this in actual deployment to something private
export MYSQL_PWD="mysql_root_pw"
echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
apt-get -y install mysql-server

# Now create and initialise the database, and a user with privileges
echo "CREATE DATABASE tictac_db;" | mysql
echo "CREATE USER 'dbserver'@'%' IDENTIFIED BY 'db_pw';" | mysql
echo "GRANT ALL PRIVILEGES ON tictac_db.* TO 'dbserver'@'%';" | mysql

# Create user for the game server, with row-level read/write privilege
echo "CREATE USER 'gameserver'@'%' IDENTIFIED BY 'game_pw';" | mysql
echo "GRANT SELECT, INSERT, UPDATE ON tictac_db.* TO 'gameserver'@'%';" | mysql

# Create user for the web server, with read-only privileges
echo "CREATE USER 'webserver'@'%' IDENTIFIED BY 'web_pw';" | mysql
echo "GRANT SELECT ON tictac_db.* TO 'webserver'@'%';" | mysql