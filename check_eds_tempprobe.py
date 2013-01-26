#!/usr/bin/python
# coding: utf-8
#
# Check the temperature probes on EDS 1-wire server
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# http://www.nickebo.net
# Licence GPLv2
# Version 0.1

import string, sys, os, argparse, urllib2, xml
from xml.dom.minidom import parseString

# Parse arguments
parser = argparse.ArgumentParser(description='Check temperature probes on EDS 1-wire server')
parser.add_argument('-H', action="store", dest="hostname", help='1-wire server hostname')
parser.add_argument('-p', action="store", dest="probe", type=int, help='Probe number, starting with 0')
parser.add_argument('-w', action="store", dest="warn", type=int, help='Warning temperature')
parser.add_argument('-c', action="store", dest="crit", type=int, help='Critical temperature')
results = parser.parse_args()

# Store parsed arguments in variables and make sure they're not empty
warn = results.warn
crit = results.crit
probe = results.probe
if (warn == None or crit == None or probe == None):
	parser.print_help()
	raise SystemExit()
if (crit <= warn):
	print "Critical temperature can't be less or equal to warning temperature"
	parser.print_help()
	raise SystemExit()

#Connect to the 1-wire server
hostname = results.hostname
try:
	file = urllib2.urlopen('http://' + hostname + '/details.xml')
except:
	print "Could not connect to " + hostname
	raise SystemExit(3)

#Read the XML file and close it
data = file.read()
file.close()

#Parse XML
try:
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('Temperature')[probe].toxml()
	sensor = float(xmlTag.replace('<Temperature Units="Centigrade">','').replace('</Temperature>',''))
except:
	print "Error reading 1-wire probe"
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
