#!/usr/bin/python

import requests
import sys, os
import time
import getopt

version = '1.0.0'
author = 'Chris Martin'
date = 'March 2017'

# Parse the command-line options
clopt = getopt.getopt(sys.argv[1:],
                      'upcCD:hvdf',
                      ['help', 'verbose', 'debug', 'force',
                      'domain=', 'user=', 'passwd=', 'config=', 
                      'cachedir=', 'timefmt='])

# Transform the output of getopt() into a dictionary
clopt_flags = {x[0]:x[1] for x in clopt[0]}

if '-h' in clopt_flags or '--help' in clopt_flags:
    sys.stdout.write("""
NOMAD dynamic DNS update service for ZoneEdit

Checks the system's current IP address with a call to ipinfo.io and 
compares it against the last known value.  If there has been a change,
nomad issues DDNS update request to the ZoneEdit server.

http://forum.zoneedit.com/index.php?threads/setting-up-dynamic-dns-for-your-domain.4/

HELP
-h or --help
    Print this help text.

ZONEEDIT LOGIN OPTIONS
-u or --user
    Sets the username used to log in to ZoneEdit
    -uUSERNAME  or  --user USERNAME
    
-p or --passwd
    Sets the plaintext password or token used to log in to ZoneEdit.
    Your administrative password will work, but you should use a login 
    token for security.  
    -pTOKEN  or  --passwd TOKEN

CONFIGURING THE BEHAVIOR OF NOMAD
-f or --force
    If this flag is found, then a DNS update will be forced regardless 
    of the result of the comparison against the cached ip file.

-c or --config
    Sets the nomad configuration file 
    -c/etc/nomad_config.py  or  --config /etc/nomad_config.py    

-C or --cachedir
    Sets the directory where the ip and log files are stored.  nomad 
    needs rwx permissions here.  Ending / is not mandatory.
    -d/var/cache/nomad/  or  --cachedir /var/cache/nomad/

-D or --domain
    Sets the domain whose IP should be updated.
    -Dmydomain.com --domain mydomain.com

--timefmt
    Sets the time format string used when logging.  The format string is
    passed verbatim to the python time.strftime() function to generate 
    the time stamp.
    --timefmt '[%D %T]'

DEBUGGING OPTIONS
Debugging should usually be done using the -dv options together.

-d or --debug
    Changes the behavior of nomad to perform a dry-run.  It will load the
    configuration, check the IP address, but it will not actually connect to
    the ZoneEdit servers.
    
-v or --verbose
    Prints the behavior of nomad to the screen for debugging.
    
(c) 2017 Christopher R. Martin
""")
    exit(0)


# Configuration defaults
config_dict = {
'domain':None,
'user':None,
'passwd':None,
'cachedir':'/var/cache/nomad',
'timefmt':'[%D %T]',
'config':'/etc/nomad_config.py',
'debug':False,
'force':False,
'verbose':False
}


# Define a routine for setting config parameters from the short and long 
# options
#   dopt    Indicates the config_dict keyword to modify
#   opt     Is a list of equivalent option strings as they appear in the output
#           of getopt().  For example, ['-o', '--output'] might indicate two
#           equivalent flags that should both be mapped to the same item in the
#           configuration dictionary.
# The clopt_flags dict will be checked for these options.  When any one of the
# options in the opt list is found in the clopt output, its value will be
# written to config_dict[].
#
#   set_config('user', ['-u', '--user'])
#
# will place the argument of the '-u' and '--user' flags into 
# config_dict['user'].
def set_config(dopt, opt=[]):
    found = None
    for thisopt in opt:
        if thisopt in clopt_flags:
            if found is None:
                found = thisopt
            else:
                sys.stderr.write(
                    'Redundant command line options %s, %s'%(found, thisopt))
                exit(-1)

    if found is not None:
        if clopt_flags[found] == '':
            config_dict[dopt] = True
        else:
            config_dict[dopt] = clopt_flags[found]


        
# First, assign the config file if it is present in the CL options.    
set_config('config',['-c','--config'])

# Go get the configuration 
# Execute the config file with the configuration dictionary as the locals dict
# Read/write privileges to the configuration file should be carefully 
# controlled since it will contain the access token for the DDNS service and
# the contents will be executed verbatim.
config_file = config_dict['config']
if os.access(config_file, os.R_OK):
    try:
        with open(config_file,'r') as cf:
            exec(cf.read(),config_dict)
    except:
        sys.stderr.write('Invalid configuration file.\n')
        sys.stderr.write(sys.exc_info()[1].message)
        exit(1)

else:
    sys.stderr.write('Could not open configuration file: ' + config_file)
    exit(1)

# Now read in the rest of the command line arguments.  Putting them second
# allows them to override the config file.
set_config('domain',['-D','--domain'])
set_config('verbose',['-v','--verbose'])
set_config('debug',['-d','--debug'])
set_config('force',['-f','--force'])
set_config('user',['-u','--user'])
set_config('passwd',['-p','--passwd'])
set_config('cachedir',['-C','--cachedir'])
set_config('timefmt',['--timefmt'])

# Build the log and IP file names
cache_dir = config_dict['cachedir']
log_file = os.path.join(config_dict['cachedir'],'log')
ip_file = os.path.join(config_dict['cachedir'],'ip')
verbose = bool(config_dict['verbose'])

# Before we go mucking about with files, be verbose to help with any debugging
# in case something breaks accessing the cache files
if verbose:
    sys.stdout.write(
"""*** NOMAD ***
Version %s
By %s, %s
Using configuration file: %s
Using log file: %s
Using ip file: %s
Domain: %s
User: %s
Force update: %s
*** ***
"""%(version, author, date, config_file, log_file, ip_file, 
     config_dict['domain'], config_dict['user'], str(config_dict['force'])))


cache_ip = (-1,-1,-1,-1)
web_ip = (-1,-1,-1,-1)


# Attempt to get the system's current ip address from ipinfo.io
IP_WEB_FAIL = False
IP_WEB_MEESSAGE = ''
if verbose:
    sys.stdout.write("Checking current ip...")
try:
    # Issue the web request.  Failure raises an exception caught by try:except
    page = requests.get('http://ipinfo.io')
    # Extract the IP address
    iptext = page.json()['ip']
except:
    IP_WEB_FAIL = True
    IP_WEB_MESSAGE = sys.exc_info()[1].message

# If everything is going well, then convert the text into a tuple of integers
if not IP_WEB_FAIL and page.status_code >= 200 and page.status_code <= 299:
    try:
        web_ip = tuple([int(this) for this in iptext.split('.')])
        if len(web_ip)!=4:
            raise Exception()
    except:
        IP_WEB_FAIL = True
        IP_WEB_MESSAGE = "Found nonsense IP address: %s"%iptext
else:
    IP_WEB_FAIL = True
    IP_WEB_MESSAGE = ip_page.content

if verbose:
    if IP_WEB_FAIL:
        sys.stdout.write("[FAILED]\n")
    else:
        sys.stdout.write(iptext + "\n")


# Get the Former IP address from the cached IP file
IP_CACHE_FAIL = False
IP_CACHE_MESSAGE = ''
IP_CHANGE = False
if verbose:
    sys.stdout.write("Checking cached IP address...")
# Does the ip cache file exist?
if os.access(ip_file,os.F_OK):
    try:
        # Read the old IP address and convert it into a tuple
        with open(ip_file,'r') as ff:
            iptext = ff.read()
        cache_ip = tuple([int(this) for this in iptext.split('.')])
    except:
        IP_CACHE_FAIL = True
        IP_CACHE_MESSAGE = 'Failed to open file %s'%ip_file
        
    # Compare the new IP to the old IP
    if not (IP_WEB_FAIL or IP_CACHE_FAIL):
        IP_CHANGE = cache_ip != web_ip
        
# If there is no IP history, then default to a change
else:
    IP_CHANGE = True

if verbose:
    if IP_CACHE_FAIL:
        sys.stdout.write("[FAILED]\n")
    else:
        sys.stdout.write(iptext + '\n')
    if IP_CHANGE:
        sys.stdout.write("CHANGE DETECTED\n")


# Update the cache IP address
IP_UPDATE_FAIL = False
IP_UPDATE_MESSAGE = ''
# Update the IP file ONLY if there is something meaningful to put in its place
if IP_CHANGE and not IP_WEB_FAIL:
    if verbose:
        sys.stdout.write("Updating IP cache...")
    try:
        with open(ip_file,'w') as ff:
            ff.write('%d.%d.%d.%d'%web_ip)
    except:
        IP_UPDATE_FAIL = True
        IP_UPDATE_MESSAGE = 'Failed to write IP cache %s'%ip_file

    if verbose:
        if IP_UPDATE_FAIL:
            sys.stdout.write("[FAILED]\n")
        else:
            sys.stdout.write("[done]\n")

# Update the DDNS
DNS_UPDATE_FAIL = False
DNS_UPDATE_MESSAGE = ''
# Update the DDNS ONLY if 
# (1) there has been a change (IP_CHANGE is True)
#     This prevents nomad from banging away on the ZoneEdit DDNS service
#     pointlessly.
# (2) the cache update succeeded (IP_UPDATE_FAIL is False)
#     This prevents a file write permission error from fooling nomad into 
#     believing that there has been a change in IP every time it checks.
# (3) the debug flag was not set
if IP_CHANGE and not IP_UPDATE_FAIL and not config_dict['debug']:
    if verbose:
        sys.stdout.write("Updating the ZoneEdit DNS record...")
    url = 'https://dynamic.zoneedit.com/auth/dynamic.html' + 
          '?host=%s&dnsto=%s'%(host,ip)
    host = config_dict['domain']
    ip = '%d.%d.%d.%d'%web_ip
    try:
        page = requests.get( url + '?host=%s&dnsto=%s'%(host,ip),
            auth = (config_dict['user'], config_dict['passwd']))
    except:
        DNS_UPDATE_FAIL = True
        DNS_UPDATE_MESSAGE = sys.exc_info()[1].message


#r = requests.get('https://dynamic.zoneedit.com/auth/dynamic.html?host=omnifariousbox.com&dnsto=72.45.43.82', auth=('CMartin40','3C9E25201D37AD9C'))

exit(0)