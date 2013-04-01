#!/usr/bin/env python
# coding: utf-8
#
# Check the humidity probes from a DS2438 sensor on EDS 1-wire server
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse, urllib2, xml
from xml.dom.minidom import parseString

# Parse arguments
parser = argparse.ArgumentParser(description='Check humidity probes on EDS 1-wire server')
parser.add_argument('-H', action="store", dest="hostname", help='1-wire server hostname')
parser.add_argument('-p', action="store", dest="probe", type=int, help='Probe number, starting with 0')
parser.add_argument('-w', action="store", dest="warn", type=int, help='Warning humidity')
parser.add_argument('-c', action="store", dest="crit", type=int, help='Critical humidity')
results = parser.parse_args()

# Store parsed arguments in variables and make sure they're not empty
warn = results.warn
crit = results.crit
probe = results.probe
if (warn == None or crit == None or probe == None):
	parser.print_help()
	raise SystemExit()
if (crit <= warn):
	print "Critical humidity can't be less or equal to warning humidity"
	parser.print_help()
	raise SystemExit()

# Connect to the 1-wire server and download details.xml
hostname = results.hostname
try:
	file = urllib2.urlopen('http://' + hostname + '/details.xml')
except:
	print "Could not connect to " + hostname
	raise SystemExit(3)

# Read the data from the XML file and close it
data = file.read()
file.close()

# Parse XML
try:
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('Humidity')[probe].toxml()
	sensor = float(xmlTag.replace('<Humidity Units="PercentRelativeHumidity">','').replace('</Humidity>',''))
except:
	print "Error reading 1-wire probe"
	raise SystemExit(3)

# Print status
if (sensor < warn):
	print "OK: Humidity: " + str(sensor) + " %|Humidity=" + str(sensor) + "%;" + str(warn) + ";" + str(crit) + ";" + str(sensor-10) + ";" + str(sensor+10)
	raise SystemExit(0)
elif (sensor >= warn and sensor < crit):
	print "WARNING: Humidity: " + str(sensor) + " %|Humidity=" + str(sensor) + "%;" + str(warn) + ";" + str(crit) + ";" + str(sensor-10) + ";" + str(sensor+10)
	raise SystemExit(1)
else:
	print "CRITICAL: Humidity: " + str(sensor) + " %|Humidity=" + str(sensor) + "%;" + str(warn) + ";" + str(crit) + ";" + str(sensor-10) + ";" + str(sensor+10)
	raise SystemExit(2)
