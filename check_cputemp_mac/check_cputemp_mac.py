#!/usr/bin/env python
# coding: utf-8
#
# Check the CPU temperature on Mac OS X 
# Requires Temperature Monitor by Marcel Bresink Software-Systeme
# Can be downloadded from http://www.bresink.com/osx/TemperatureMonitor.html
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse

tempmonitor = "/Applications/TemperatureMonitor.app/Contents/MacOS/tempmonitor"

# Check if above binary really exists
if os.path.isfile(tempmonitor) == False:
	print "Temperature Monitor not installed in /Applications"
	raise SystemExit(3)

# Parse arguments
parser = argparse.ArgumentParser(description='Check CPU temperature on Mac OS X using Temperature Monitor')
parser.add_argument('-w', action="store", dest="warn", type=int, help='Warning temperature')
parser.add_argument('-c', action="store", dest="crit", type=int, help='Critical temperature')
results = parser.parse_args()

# Store parsed arguments in variables and make sure they're not empty
warn = results.warn
crit = results.crit
if (warn == None or crit == None):
	parser.print_help()
	raise SystemExit()

# Read the CPU temperature
try:
	sensor = int(os.popen(tempmonitor + " | awk '{print $1}'").read())
except:
	print "Error reading CPU temperature"
	raise SystemExit(3)

# Print status
if (sensor < warn):
	print "OK: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(0)
elif (sensor >= warn and total < crit):
	print "WARNING: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(1)
else:
	print "CRITICAL: Temperature: " + str(sensor) + " C|Temperature=" + str(sensor) + ";" + str(warn) + ";" + str(crit) + ";" + str(warn-5) + ";" + str(crit+5)
	raise SystemExit(2)
