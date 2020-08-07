# About
This will install apt-cacher-ng on a device, configure it, and host the required python script for other machines

Once the cacher is configured, running the python script on another machine will configure it to use the cacher for apt things.

Note: The sources list is backed up before making these changes and can be restored by running the python script with `-r`.

# Instructions
1. Clone repo onto desired cacher machine
2. Run cacher-install.sh on said machine
3. Run start-hosting.sh
4. On another device, run `wget <cacher's IP>:8000/edit-sources.py`
5. Run the python script `python3 edit-sources.py -i <IP> -p <port>` where IP is the cacher's IP and port is 3142 by default. Otherwise use your configured port for the cacher.
