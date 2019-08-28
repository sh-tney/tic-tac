# Run updates & install dependecies to run the webserver, Apache, PHP,
# and php-mysql plugins
apt-get update
apt-get install -y apache2 php libapache2-mod-php php-mysql
            
# Change VM's webserver's configuration to use shared folder.
cp /vagrant/test-website.conf /etc/apache2/sites-available/

# Activate our config, and reload to apply changes
a2ensite test-website
a2dissite 000-default
service apache2 reload