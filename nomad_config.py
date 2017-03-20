
### BEGIN CONFIGURATION ###
#
# All of these configuration parameters are MANDATORY.  If they are omitted
# then nomad will raise an exception.

# update_site is the URL that is used by the DNS service as the interface for
# dynamic update requests.
# '''
#   update_site = 'https://dynamic.zoneedit.com/auth/dynamic.html'
# '''
# is the ZoneEdit site.
update_site = 'https://dynamic.zoneedit.com/auth/dynamic.html'

# host_site is the domain that is being updated.
# '''
#   host_site = 'my.domain.com'
# '''
# indicates a dynamic update for my.domain.com
host_site = 'omnifariousbox.com'

# site_user is the username that will be used to authenticate the process
# '''
#   site_user = 'my_user_name'
# '''
site_user = 'CMartin40'

# site_passwd indicates the authentication token or password used to 
# authenticate the DNS update request.
# '''
#   site_passwd = 'my_password'
# '''
site_passwd = '3C9E25201D37AD9C'

# cache_dir indicates a directory where nomad has read/write permissions to 
# cache information.  In this directory, nomad will create two files that are
# used each time it checks the system's current IP address.
# '''
#   cache_dir = '/var/cache/nomad'
# '''
# In this directory, nomad creates two files; ip and log.  log is a running log
# of each query made of the ip address, each attempted update, etc...
# ip contains the value of the ip address the last time nomad checked.  If the
# ip file is missing, nomad will create the ip file, force an update, and it 
# will log the incident.  If nomad fails to create the ip file, it will raise 
# an exception.
cache_dir = '/var/cache/nomad'

# interval_min indicates (in minutes) how often nomad will check for a change
# in the ip address.
# '''
#   interval_min = 120
# '''
# sets the poll interval to two hours.
interval_min = 120

# config_file indicates where to find a secondary configuration python file
# that can be used to overwrite these defaults
# '''
#   config_file = '/etc/nomad_config.py'
# '''
# The configuration file should be executable python code, but it will not be
# executed by the system; it will be executed by a call to exec within python.
# Changes to this value in the configuration file will have no effect after
# installation.
config_file = '/etc/nomad_config.py'

# time_format is the format string used by python's time.strftime to construct
# a date/time string in the log files
# '''
#   time_format = '%D %T'
# '''
# is shorthand for '%m/%d/%y %H:%M:%S'
time_format = '%D %T'