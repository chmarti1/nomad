#!/usr/bin/python
import sys, os, stat

nomad_config = 'nomad-config.py'
nomad_file = 'nomad.py'
cron_file = '/etc/cron.hourly/nomad'

# Configuration defaults
config_dict = {
'domain':None,
'user':None,
'passwd':None,
'cachedir':'/var/cache/nomad',
'timefmt':'[%D %T]',
'config':'/etc/nomad.conf',
'debug':False,
'force':False,
'verbose':False,
'installdir':'/bin'
}

# Read in the configuration file
sys.stdout.write('Reading in configuration file...')
try:
    with open(nomad_config,'r') as cf:
        exec(cf.read(),config_dict)
except:
    sys.stdout.write('[Failed]\n')
    sys.stderr.write('Failed to read the configuration file: %s\n'%nomad_config)
    exit(1)
sys.stdout.write('[done]\n')

cachedir = config_dict['cachedir']
config = config_dict['config']
ipfile = os.path.join(cachedir,'ip')
logfile = os.path.join(cachedir,'log')
installdir = config_dict['installdir']
installfile = os.path.join(installdir, 'nomad')

sys.stdout.write('Initializing %s...'%cachedir)
try:
    # Create the cache directory
    if not os.access(cachedir,os.F_OK):
        os.mkdir(cachedir)
    cmd = 'chmod 755 %s'%cachedir
    os.system(cmd)
    # Create the LOG file
    open(logfile,'w').close()
    cmd = 'chmod 644 %s'%logfile
    os.system(cmd)
except:
    sys.stdout.write('[Failed]\n')
    exit(1)
sys.stdout.write('[done]\n')

sys.stdout.write('Placing %s...'%config)
cmd = 'cp %s %s'%(nomad_config, config)
try:
    os.system(cmd)
    os.chmod(config,stat.S_IRUSR|stat.S_IWUSR)
except:
    sys.stdout.write('[Failed]\n')
    exit(1)
sys.stdout.write('[done]\n')

sys.stdout.write('Placing %s...'%installfile)
cmd = 'cp %s %s'%(nomad_file,installfile)
try:
    os.system(cmd)
    os.chmod(installfile, stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP)
except:
    sys.stdout.write('[Failed]\n')
    exit(1)
sys.stdout.write('[done]\n')

sys.stdout.write('Placing %s...'%cron_file)
try:
    with open(cron_file,'w') as ff:
        ff.write('#!/bin/bash\nnomad\n')
    os.chmod(cron_file, stat.S_IREAD|stat.S_IRWXU)
except:
    sys.stdout.write('[Failed]\n')
    sys.stderr.write('Failed to place the cron file: %s\n'%cron_file)
    exit(1)
sys.stdout.write('[done]\n')

