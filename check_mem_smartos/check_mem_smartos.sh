#!/usr/bin/env bash
# Check free memory in SmartOS
# Regards the ARC as free memory
#
# Copyright Marcus Wilhelmsson
# License: MIT
#

# Get args
TEMP="getopt -o wch:"
while true; do
	case "$1" in
		-w) WARN="$2"; shift 2 ;;
		-c) CRIT="$2"; shift 2 ;;
		-h) HELP=true; shift ;;
		*) break ;;
	esac
done

# Function for getting and printing mem stats
getmemstats () {
	# Get stats
    declare -i pagesize=`pagesize`
	declare -i physpages=`kstat -p unix:0:system_pages:pagestotal | awk '{print $2}'`
    declare -i freepages=`kstat -p unix:0:system_pages:pagesfree | awk '{print $2}'`
    declare -i arcsize=`kstat -p zfs:0:arcstats:size | awk '{print $2}'`
    declare -i arcsizemb=$arcsize/1024/1024;

	# Convert stats to megabytes and percent
	declare -i totalmemorymb=$physpages*$pagesize/1024/1024
	declare -i freememorymb=$freepages*$pagesize/1024/1024+$arcsizemb
	declare -i usedmemorymb=$totalmemorymb-$freememorymb
	declare -i usedmempercent=`echo "$usedmemorymb*100/$totalmemorymb" | bc`
	declare -i freemempercent=100-$usedmempercent
	
	#Print monitoring info
	if [ $usedmempercent -lt $WARN ]; then
		echo -e "OK: Total mem: $totalmemorymb MB Free mem: $freememorymb ($freemempercent%) MB Used mem: $usedmemorymb ($usedmempercent%) MB|usedmempercent=$usedmempercent;$WARN;$CRIT"
		exit 0

	elif [ $usedmempercent -gt $WARN ] && [ $usedmempercent -lt $CRIT ] || [ $usedmempercent -eq $WARN ]; then
		echo -e "WARNING: Total mem: $totalmemorymb MB Free mem: $freememorymb ($freemempercent%) MB Used mem: $usedmemorymb ($usedmempercent%) B|usedmempercent=$usedmempercent;$WARN;$CRIT"
		exit 1

	elif [ $usedmempercent -gt $CRIT ] || [ $usedmempercent -eq $CRIT ]; then
		echo -e "WARNING: Total mem: $totalmemorymb MB Free mem: $freememorymb ($freemempercent%) MB Used mem: $usedmemorymb ($usedmempercent%) MB|usedmempercent=$usedmempercent;$WARN;$CRIT"
		exit 2
	else
		echo -e "ERROR"
		exit 3
	fi
}

# Print help
if [[ $HELP == true ]]; then
	echo "Check free/used memory in SmartOS"
	echo "Regards the ARC as free memory"
	echo
	echo "Copyright Marcus Wilhelmsson"
	echo "License: MIT"
	echo
	echo "Options:"
	echo "-w warning value of used memory in percent"
	echo "-c critical value of used memory in percent"
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

# Call function to get memory stats
getmemstats