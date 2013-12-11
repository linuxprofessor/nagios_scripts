#!/usr/bin/env bash
#
# Check CPU load on OS X
# Copyright Marcus Wilhelmsson
# License: MIT
#

# Check if iostat is installed
if [ ! `which iostat` ]; then
	echo "iostat not found"
	exit 0
fi

# Get args
TEMP="getopt -o wch:"
while true; do
	case "$1" in
		-w ) WARN="$2"; shift 2 ;;
		-c ) CRIT="$2"; shift 2 ;;
		-h ) HELP=true; shift ;;
		* ) break ;;
	esac
done

# Function for monitoring
monitor () {
	# Calculate current CPU load using iostat
	# Count twice, iostat always report 95% idle on the first count
	# Compensate for more than one mounted disk (i.e. disk0, disk1)
	getcol=$(iostat|head -1|wc -w)
	getcol=$(expr $getcol - 2)
	getcol=$(($getcol * 3))
	total=$(/usr/sbin/iostat -c 2|tail -1|awk '{print $'`echo $getcol`'}')
	cpupercent=$(expr 100 - `expr $total`)

	# Print monitoring info
	if [ $cpupercent -lt $WARN ]; then
		echo -e "OK: CPU load: $cpupercent%|CPUload=$cpupercent%;$WARN;$CRIT"
		exit 0

	elif [ $cpupercent -gt $WARN ] && [ $cpupercent -lt $CRIT ] || [ $cpupercent -eq $WARN ]; then
		echo -e "WARNING: CPU load: $cpupercent%|CPUload=$cpupercent%;$WARN;$CRIT"
		exit 1

	elif [ $cpupercent -gt $CRIT ] || [ $cpupercent -eq $CRIT ]; then
		echo -e "CRITCAL: CPU load: $cpupercent%|CPUload=$cpupercent%;$WARN;$CRIT"
		exit 2
	else
		echo -e "ERROR"
		exit 3
	fi
}

# Print help
if [[ $HELP == true ]]; then
	echo "Check CPU load in OS X using iostat"
	echo "Copyright Marcus Wilhelmsson"
	echo "License: MIT"
	echo
	echo "Options:"
	echo "-w warning value in percent"
	echo "-c critical value in percent"
	echo "-h print this text"
	echo
	exit 0
fi

# Make sure args for WARN and CRIT are int
if [[ $WARN != [0-9]* ]]; then
	echo -e "ERROR! Warning value -w is not an integer"
	exit 3

elif [[ $CRIT != [0-9]* ]]; then
	echo -e "ERROR! Critical value -c is not an integer"
	exit 3
fi

# Check if WARN is higher than CRIT
if [ $WARN -gt $CRIT ]; then
	echo -e "ERROR: Critical value -c must be higher than Warning -w"
	exit 3
fi

# Run monitor function
monitor

