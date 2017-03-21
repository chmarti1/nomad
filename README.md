# NOMAD 

is a really simple dynamic IP client for the ZoneEdit DDNS service.

## Installation
```
$sudo apt-get install python python-requests
$git clone http://github.com/nomad.git
$cd nomad
```
Open the nomad-config.py file, and edit it to suit.  The installation script will detect your settings and honor them as best it can.  It will print a summary of every file it moves onto your system in case you want to undo anything.
```
$sudo ./nomad-setup.py
```

By default, this will install
 * The nomad executable in the /bin directory
 * The nomad.conf file in the /etc directory
 * A nomad directory in /var/cache
 * A wrapper shell script in /etc/cron.hourly

## Configuration
The nomad-config.py file has detailed comments describing its configuration.  Alternately, you can always execute 
```
$nomad --help
```
for a detailed description of the configuration options.

