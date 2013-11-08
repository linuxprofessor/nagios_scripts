#!/usr/bin/env python
# coding: utf-8
#
# Check the RAID status on a Synology 
# Requires snmpget
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Check RAID Status on a Synology Disk Station')
parser.add_argument('-H', action="store", dest="hostname", help='Disk Station hostname')
parser.add_argument('-C', action="store", dest="community", help='SNMP community')
results = parser.parse_args()

# Locate snmpget binary and make sure it's executable
snmpbinary = str(os.popen('which snmpget').read())
snmpbinary = snmpbinary.rstrip()
if(os.path.isfile(snmpbinary) != True or os.access(snmpbinary, os.X_OK) != True):
	print "snmpget not found or not executable"
	raise SystemExit(3)

# Store parsed arguments in variables
hostname = results.hostname
community = results.community

# Connect to the Synology and put RAID Status in variable status
try:
	status = str(os.popen(snmpbinary + ' -c ' + community + ' -v 2c ' + hostname + ' 1.3.6.1.4.1.6574.3.1.1.3.0').read())
	status = status.split()
	status = status[3]
	status = int(status)
except:
	print "Could not connect to " + hostname + " or error reading RAID status"
	raise SystemExit(3)

# Print status
if (status < 11):
	if(status == 1):
		print "OK: RAID Status Normal"
	elif(status == 2):
		print "OK: RAID Status Repairing"
	elif(status == 3):
		print "OK: RAID Status Migrating"
	elif(status == 4):
		print "OK: RAID Status Expanding"
	elif(status == 5):
		print "OK: RAID Status Deleting"
	elif(status == 6):
		print "OK: RAID Status Creating"
	elif(status == 7):
		print "OK: RAID Status RaidSyncing"
	elif(status == 8):
		print "OK: RAID Status RaidParityChecking"
	elif(status == 9):
		print "OK: RAID Status RaidAssembling"
	elif(status == 10):
		print "OK: RAID Status Canceling"
	raise SystemExit(0)
elif (status >= 11 and sensor < 12):
	print "WARNING: RAID Status Degraded"
	raise SystemExit(1)
else:
	print "CRITICAL: RAID Status Crashed"
	raise SystemExit(2)

