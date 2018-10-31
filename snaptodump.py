#Python

from sys import argv
from datetime import datetime

import sys, os, os.path

start_time = datetime.now()

# MySQL setup: put the MySQL user with dump permission and database name here
# password will be asked interactively later: 

dbusr = "your_mysql_username" 
dbname = "your_mysql_database_name"

print """

This script will launch Terraform to dump the latest snapshot of prod db

PREREQUISITES:

You need AWS tokens setup as ENV vars or Terraform won't work:
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="yyy"

USAGE:

python snaptodump.py

*** WARNING ***
This tool requires the mysqldump binary installed on your system and the necessary free space on your local disk for dumping!

"""

terraform_init_dir = "./.terraform"

if os.path.exists(terraform_init_dir):
    print "terraform init already ran!\n"
else:
    os.system( "./terraform init")

if ( os.system( "./terraform apply") != 0 ):
    print "*** ERROR while applying terraform config, dumping stopped! ***"
    exit()

host = os.popen('./terraform output address').read()
filename = os.popen('./terraform output snapshot').read() + ".sql.gz"

dumpcmd = "mysqldump -h %s -u %s --compress -p %s |gzip > %s" % (host.replace('\n',''), dbusr, dbname, filename.replace('\n',''))

print "Next step is mysqldump, you will be asked for a MySQL password\n"

dbdump_start = datetime.now()

if os.system( dumpcmd ):
    print "An error occurred!"
    print "command was: %s" % dumpcmd
else:
    print "All done!"
    print "Db dumped in %s" % ( datetime.now() - dbdump_start )

#Now let's destroy our temp RDS instance
os.system( "./terraform destroy ")

#Feeling bold? comment previous command and enable this!
#os.system( "./terraform destroy -auto-approve"

print "Total procedure completed in %s\n" % ( datetime.now() - start_time )

#print dumpcmd
