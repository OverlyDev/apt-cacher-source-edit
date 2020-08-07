apt install apt-cacher-ng

systemctl is-enabled apt-cacher-ng

ufw allow 3142/tcp
ufw reload

manual config
echo 'Acquire::http { Proxy "http://proxy:3142"; }' | sudo tee -a /etc/apt/apt.conf.d/proxy

tunnel HTTPS /etc/apt-cacher-ng/acng.conf
PassThroughPattern: ^(.*):443$
