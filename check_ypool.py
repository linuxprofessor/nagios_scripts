#!/usr/bin/env python
# coding: utf-8
#
# Check the status and stats on ypool
#
# By Marcus Wilhelmsson
# marcus@nickebo.net
# https://www.nickebo.net
# Licence MIT
# Version 0.2

import string, argparse, urllib2, json

# Get miners info
def minerStatus():
	# Evaluate critical and warning value
	if (results.warning == None or results.critical == None):
		parser.print_help()
		raise SystemExit(3)
	if (int(results.critical) >= int(results.warning)):
		print "Critical can't be higher/equal than/to warning or warning/critical malformed"
		parser.print_help()
		raise SystemExit(3)

	try:
		# Get status of workers via API
		url = "http://ypool.net/api/live_workers?coinType=" + results.cointype + "&key=" + results.apikey
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		data = json.loads(response.read())

		# Loop through workers and store numbers of active workers in the variable status
		status = 0
		for item in data["connectedWorkers"]:
			status = status + 1
		status = int(status)
	except:
		print "Could not fetch status of miners"
		raise SystemExit(3)

	# Print status
	if (status <= int(results.critical)):
		print "CRITICAL: Miners: " + str(status) + "|miners=" + str(status)
		raise SystemExit(2)
	elif (status > int(results.critical) and status <= int(results.warning)):
		print "WARNING: Miners: " + str(status) + "|miners=" + str(status)
		raise SystemExit(1)
	else:
		print "OK: Miners: " + str(status) + "|miners=" + str(status)
		raise SystemExit(0)

# Personal stats
def personalStats():
	try:
		# Get personal stats via API
		url = "http://ypool.net/api/personal_stats?coinType=" + results.cointype + "&key=" + results.apikey
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		data = json.loads(response.read())
		print "OK: Balance: " + str(data['balance']) + " Unconfirmed balance: " + str(data['unconfirmedBalance']) + " Share Value Curr Round: " + str(data['shareValueCurrentRound']) + " Found blocks overall: " + str(data['foundBlocksOverall']) + "|balance=" + str(data['balance']) + ";unconfirmedBalance=" + str(data['unconfirmedBalance']) + ";shareValueCurrentRound=" + str(data['shareValueCurrentRound']) + ";foundBlocksOverall=" + str(data['foundBlocksOverall'])
	except:
		print "Could not fetch personal stats"
		raise SystemExit(3)
	raise SystemExit(0)

# Parse arguments
parser = argparse.ArgumentParser(description='Check statuses on ypool mining pool')
parser.add_argument('-C', action="store", dest="command", help='Command; minerstatus, personalstats')
parser.add_argument('-K', action="store", dest="apikey", help='Your API key')
parser.add_argument('-ct', action="store", dest="cointype", help='Coin Type, e.g. xpm, pts, etc.')
parser.add_argument('-w', action="store", dest="warning", help='Warning value')
parser.add_argument('-c', action="store", dest="critical", help='Critical value')
results = parser.parse_args()

# Check command argument
if(results.command == "minerstatus"):
	minerStatus()
elif(results.command == "personalstats"):
	personalStats()
else:
	print "Command not found"
	parser.print_help()
	raise SystemExit(3)

