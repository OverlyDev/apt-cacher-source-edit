#!/bin/bash

# get IP address
thisIP=$( hostname -I | sed 's/ //g')

# apt stuff
apt update
apt upgrade
apt install apt-cacher-ng -y

# make sure service is enabled
systemctl enable apt-cacher-ng

# firewall stuff
ufw allow 3142/tcp
ufw reload

# tunnel HTTPS
echo "PassThroughPattern: ^(.*):443$" >> /etc/apt-cacher-ng/acng.conf

# enable cache for this device
echo 'Acquire::http { Proxy "http://'"$thisIP"':3142"; }' | tee -a /etc/apt/apt.conf.d/proxy
