unzip nagios-plugins.zip
cd nagios-plugins-master/
./tools/setup
mkdir nagios-plugin
./configure --prefix=$(pwd)/nagios-plugin
make
make install
make install-root
cd ..
cp nagios-plugins-master/nagios-plugin/libexec/check_http checks/check_http
cp nagios-plugins-master/nagios-plugin/libexec/check_tcp checks/check_tcp
cp nagios-plugins-master/nagios-plugin/libexec/check_dns checks/check_dns
cp nagios-plugins-master/nagios-plugin/libexec/check_icmp checks/check_icmp
rm -Rf nagios-plugins-master
echo "Enter root password for changing persmission for check_icmp"
sudo chown root:root checks/check_icmp
sudo chmod u+s checks/check_icmp
echo "Enter your MySQL password for root user to create database"
sudo mysqladmin create probe_db -p
echo "Enter your MySQL password for root user to configure database"
mysql -u root -p probe_db < probe_db.sql
mkdir output
chmod +x script/*
