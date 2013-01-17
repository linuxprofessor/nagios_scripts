#!/usr/local/bin/python
# coding: utf-8
#
# Check the temperature of hard drives and calculate a mean value
# Requires smartmontools and privileges to check the disk temperatures
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse

# Set full directory and name of the smartctl binary, change if needed
smartctlbin="/usr/local/sbin/smartctl"

# Check if above binary really exists
if os.path.isfile(smartctlbin) == False:
	print "Binary file for smartctl is faulty: " + smartctlbin
	raise SystemExit(3) 

# Parse arguments
parser = argparse.ArgumentParser(description='Check hard drive temperatures using smartmontools')
parser.add_argument('-w', action="store", dest="warn", type=int, help='Warning temperature')
parser.add_argument('-c', action="store", dest="crit", type=int, help='Critical temperature')
parser.add_argument(nargs='*', action='store', dest='disk', help='Disks to check: /dev/sda /dev/sdb /dev/sdc etc.',)
results = parser.parse_args()

# Store parsed arguments in variables and make sure they're not empty
warn = results.warn
crit = results.crit
disks = results.disk
if (warn == None or crit == None or disks == []):
	parser.print_help()
	raise SystemExit()

# Do the actual disk temperature checks
total = 0
for x in disks:
	if os.path.exists(x):
		try:
			total = total + int(os.popen(smartctlbin + " -a " + x + "| grep Celsius | awk '{print $10}'").read())
		except:
			print "Error checking " + x + ". Is it a valid hard drive?"
			raise SystemExit(3)
	else:
		print "Disk " + x + " does not exist. Exiting."
		raise SystemExit(3)
try:
	total = total/len(disks)
except:
	print "Error calculating temperature mean value"

# Print status and make sure critical is greater than warning
if warn >= crit:
	print "ERROR: Critical must be greater than warning"
	raise SystemExit(3)

if (total < warn):
	print "OK: Temperature: " + str(total) + " C|Temperature=" + str(total) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(0)
elif (total >= warn and total < crit):
	print "WARNING: Temperature: " + str(total) + " C|Temperature=" + str(total) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(1)
else:
	print "CRITICAL: Temperature: " + str(total) + " C|Temperature=" + str(total) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(2)