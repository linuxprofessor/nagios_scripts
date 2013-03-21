#!/usr/bin/env bash
#
# Check CPU load on SmartOS
# Copyright Marcus Wilhelmsson
# License: MIT
#

#Get args
while getopts "w:c:" OPTION; do
	case "${OPTION}" in
		w)
			WARN=${OPTARG}
			;;
		c)
			CRIT=${OPTARG}
			;;
	esac
done

#Check if WARN is higher than CRIT
if [ ${WARN} -gt ${CRIT} ]; then
	echo -e "ERROR: Critical value -c must be higher than Warning -w"
	exit 3
fi

#Make sure args are int
if [[ ${WARN} != [0-9]* ]]; then
	echo -e "ERROR! Warning value -w is not an integer"
	exit 3

elif [[ ${CRIT} != [0-9]* ]]; then
	echo -e "ERROR! Critical value -c is not an integer"
	exit 3
fi

#Calculate current CPU load using mpstat
numcpus=`kstat -p unix:0:system_misc:ncpus| awk '{print $2}'`
total=0;for line in $(mpstat 1 2 |tail -n $numcpus |awk '{print $16}'); do total=`expr $total + $line`; done
cpupercent=$(expr 100 - `expr $total / $numcpus`)

#Print monitoring info
if [ ${cpupercent} -lt ${WARN} ]; then
	echo -e "OK: CPU load: ${cpupercent}%|CPUload=${cpupercent}%;${WARN};${CRIT}"
	exit 0

elif [ ${cpupercent} -gt ${WARN} ] && [ ${cpupercent} -lt ${CRIT} ] || [ ${cpupercent} -eq ${WARN} ]; then
	echo -e "WARNING: CPU load: ${cpupercent}%|CPUload=${cpupercent}%;${WARN};${CRIT}"
	exit 1

elif [ ${cpupercent} -gt ${CRIT} ] || [ ${cpupercent} -eq ${CRIT} ]; then
	echo -e "CRITCAL: CPU load: ${cpupercent}%|CPUload=${cpupercent}%;${WARN};${CRIT}"
	exit 2
else
	echo -e "ERROR"
	exit 3
fi
