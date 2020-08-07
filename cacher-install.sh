#!/bin/bash

# apt stuff
apt update
apt upgrade
apt install apt-cacher-ng -y

# make sure service is enabled
if ! systemctl is-enabled apt-cacher-ng ; then
  systemctl enable apt-cacher-ng

# firewall stuff
ufw allow 3142/tcp
ufw reload
