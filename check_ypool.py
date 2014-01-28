#!/usr/bin/env python
# coding: utf-8
#
# Check the status of your miners on ypool
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# https://www.nickebo.net
# Licence MIT
# Version 0.1

import string, sys, os, argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Check miner(s) status on ypool')
parser.add_argument('-K', action="store", dest="apikey", help='Your API key')
parser.add_argument('-ct', action="store", dest="cointype", help='Coin Type, e.g. xpm, pts, etc.')
parser.add_argument('-w', action="store", dest="warning", help='Warning value')
parser.add_argument('-c', action="store", dest="critical", help='Critical value')
results = parser.parse_args()

# Get miners info
try:
	status = str(os.popen('curl -s -S "http://ypool.net/api/live_workers?coinType=' + results.cointype + '&key=' + results.apikey + '"|json_reformat|grep workerId|wc -l').read())
	status = int(status)
except:
	print "Could not fetch status of miners"
	raise SystemExit(3)

# Print status
if (status <= int(results.critical)):
	print "CRITICAL: Miners: " + str(status) + ";miners=" + str(status)
	raise SystemExit(2)
elif (status > int(results.critical) and status <= int(results.warning)):
	print "WARNING: Miners: " + str(status) + ";miners=" + str(status)
	raise SystemExit(1)
else:
	print "OK: Miners: " + str(status) + ";miners=" + str(status)
	raise SystemExit(0)
