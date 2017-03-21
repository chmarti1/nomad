
### BEGIN CONFIGURATION ###
#

# domain is the domain that is being updated.
# '''
#   domain = 'my.domain.com'
# '''
# indicates a dynamic update for my.domain.com
domain = ''

# user is the username that will be used to authenticate the process
# '''
#   user = 'my_user_name'
# '''
user = ''

# site_passwd indicates the authentication token or password used to 
# authenticate the DNS update request.
# '''
#   passwd = 'my_password'
# '''
passwd = ''

# cachedir indicates a directory where nomad has read/write permissions to 
# cache information.  In this directory, nomad will create two files that are
# used each time it checks the system's current IP address.
# '''
#   cachedir = '/var/cache/nomad'
# '''
# In this directory, nomad creates two files; ip and log.  log is a running log
# of each query made of the ip address, each attempted update, etc...
# ip contains the value of the ip address the last time nomad checked.  If the
# ip file is missing, nomad will create the ip file, force an update, and it 
# will log the incident.  If nomad fails to create the ip file, it will raise 
# an exception.
cachedir = '/var/cache/nomad'

# installdir indicates the directory where the nomad scripts should be 
# installed.
# '''
#   installdir = '/bin'
# '''
# This indicates where the executables belong after installation.
installdir = '/bin'

# config indicates where to find a secondary configuration python file
# that can be used to overwrite these defaults
# '''
#   config = '/etc/nomad.conf'
# '''
# The configuration file should be executable python code, but it will not be
# executed by the system; it will be executed by a call to exec within python.
# Changes to this value in the configuration file will have no effect after
# installation.
config = '/etc/nomad.conf'

# timefmt is the format string used by python's time.strftime to construct
# a date/time string in the log files
# '''
#   timefmt = '%D %T'
# '''
# is shorthand for '%m/%d/%y %H:%M:%S'
timefmt = '[%D %T]'

