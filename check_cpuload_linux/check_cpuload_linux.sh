#!/usr/bin/env bash
#
# Check CPU load on Linux
# Requires 'sysstat' package installed
# Copyright Marcus Wilhelmsson
# License: MIT
#

#Check if mpstat is installed
if [ ! `which mpstat` ]; then
	echo "Install sysstat package to get mpstat"
	exit 0
fi

#Get args
TEMP="getopt -o iawch:"
while true; do
	case "$1" in
		-i ) TYPE=individual; shift ;;
		-a ) TYPE=average; shift ;;
		-w ) WARN="$2"; shift 2 ;;
		-c ) CRIT="$2"; shift 2 ;;
		-h ) HELP=true; shift ;;
		* ) break ;;
	esac
done

#Function for average monitoring
average () {
	numcpus=`cat /proc/cpuinfo |grep processor|wc -l`
	#Calculate current CPU load using mpstat
	total=0;for line in $(mpstat -u -P ALL 1 2|grep -v Average|sed -e '/^$/d'|tail -n $numcpus|sed -e '/^$/d'|awk '{print $12}'|awk -F. '{print $1}'); do total=`expr $total + $line`; done
	cpupercent=$(expr 100 - `expr $total / $numcpus`)

	#Print monitoring info
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

#Function for individual monitoring
individual () {
	numcpus=`cat /proc/cpuinfo |grep processor|wc -l`
	#Calculate current CPU load using mpstat
	for line in $(mpstat -u -P ALL 1 2|grep -v Average|sed -e '/^$/d'|tail -n $numcpus|awk '{print $12}'|awk -F. '{print $1}'); do
		line=$(expr 100 - $line)
		#Set a status that stays at the value from the most heavily loaded core
		if [ $line -lt $WARN ]; then
			if [[ $status != "WARNING" ]] && [[ $status != "CRITICAL" ]]; then
				status="OK"
			fi
		elif [ $line -gt $WARN ] && [ $line -lt $CRIT ] || [ $line -eq $WARN ]; then
			if [[ $status != "CRITICAL" ]]; then
				status="WARNING"
			fi
		elif [ $line -gt $CRIT ] || [ $line -eq $CRIT ]; then
			status="CRITICAL"
		else
			echo -e "ERROR"
			exit 3
		fi
		#Add all core loads to a variable
		total="$total $line"
	done

	#Print monitoring info
	i=0
	print1="$status: CPU load:"
	for coreload in $total
	do
		print1="$print1 Core$i=$coreload%"
		print2="$print2 Core$i=$coreload%;$WARN;$CRIT;;"
		let i+=1
	done

	echo "$print1|$print2"
	case "$status" in
		OK) exit 0; shift;;
		WARNING) exit 1; shift;;
		CRITICAL) exit 2; shift;;
		*) exit 3;
	esac
}

#Print help
if [[ $HELP == true ]]; then
	echo "Check CPU load in Linux using mpstat included in sysstat"
	echo "Copyright Marcus Wilhelmsson"
	echo "License: MIT"
	echo
	echo "Options:"
	echo "-i individual monitoring of each CPU core OR -a average monitoring of all CPU cores"
	echo "-w warning value in percent"
	echo "-c critical value in percent"
	echo "-h print this text"
	echo
	exit 0
fi

#Make sure args for WARN and CRIT are int
if [[ $WARN != [0-9]* ]]; then
	echo -e "ERROR! Warning value -w is not an integer"
	exit 3

elif [[ $CRIT != [0-9]* ]]; then
	echo -e "ERROR! Critical value -c is not an integer"
	exit 3
fi

#Check if WARN is higher than CRIT
if [ $WARN -gt $CRIT ]; then
	echo -e "ERROR: Critical value -c must be higher than Warning -w"
	exit 3
fi

#Check what type of monitoring is desired
if [[ $TYPE == average ]]; then
	average
elif [[ $TYPE == individual ]]; then
	individual
else
	echo -e "Please choose average (-a) or individual (-i) monitoring"
	exit 0
fi
