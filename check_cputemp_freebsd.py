#!/usr/local/bin/python
# coding: utf-8
#
# Check the CPU temperature on FreeBSD
# Requires the kernel module coretemp to be loaded
# kldload coretemp
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse

coretempstat = int(os.popen("kldstat|grep coretemp|wc -l").read())

# Check if above binary really exists
if coretempstat == 0:
	print "coretemp kernel module not loaded. Exiting..."
	raise SystemExit(3) 

# Parse arguments
parser = argparse.ArgumentParser(description='Check CPU temperature on FreeBSD using coretemp')
parser.add_argument('-C', action="store", dest="core", type=int, help='Core, starting with 0')
parser.add_argument('-w', action="store", dest="warn", type=int, help='Warning temperature')
parser.add_argument('-c', action="store", dest="crit", type=int, help='Critical temperature')
results = parser.parse_args()

# Store parsed arguments in variables and make sure they're not empty
core = results.core
warn = results.warn
crit = results.crit
if (warn == None or crit == None or core == None):
	parser.print_help()
	raise SystemExit()
if (crit <= warn):
	print "Critical temperature can't be less or equal to warning temperature"
	parser.print_help()
	raise SystemExit()

# Read the CPU temperature
try:
	sensor = int(os.popen("sysctl -a | grep temperature | grep '\." + str(core) + "\.' | awk '{print $2}'|awk -F. '{print $1}'").read())
except:
	print "Error reading CPU temperature"
	raise SystemExit(3)

# Print status    
if (sensor < warn):
 print "OK: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
 raise SystemExit(0)
elif (sensor >= warn and sensor < crit):
 print "WARNING: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
 raise SystemExit(1)
else:
 print "CRITICAL: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
 raise SystemExit(2)