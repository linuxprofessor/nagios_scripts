# Various Nagios scripts created by me
====================

Plugins
-------

### check_cpuload

Check the CPU load in SmartOS global zone

    ~ $ ./check_cpuload [-i|-a] -w [warning] -c [critical]
    OK: CPU load: 15%

### check_cputemp_freebsd.py

Check the CPU temperature in FreeBSD

    ~ $ ./check_cputemp_freebsd.py -C [core] -w [warning] -c [critical]
    OK: CPU Temperature: 49 C

### check_cputemp_mac.py

Check the CPU temperature in OS X
Requires Temperature Monitor by Marcel Bresink Software-Systeme

    ~ $ ./check_cputemp_mac.py -w [warning] -c [critical]
    OK: CPU Temperature: 46 C

### check_eds_humidityprobe.py

Check humidity probes on EDS 1-wire server

    ~ $ ./check_eds_humidityprobe.py -H [hostname] -p [probe number] -w [warning] -c [critical]
    OK: Humidity: 38.43 %

### check_eds_tempprobe.py

Check temp probes on EDS 1-wire server

    ~ $ ./check_eds_tempprobe.py -H [hostname] -p [probe number] -w [warning] -c [critical]
    OK: Temperature: 5.0 C

### check_hdd_temp.py

Check the temperature of hard drives and calculate a mean value
Requires smartmontools and privileges to check the disk temperatures

    ~ $ ./check_hdd_temp.py -w [warning] -c [critical] [disks to check]
    OK: Temperature: 38 C

### check_smarttemp.js

Check the temperature of hard drives and calculate a mean value
Requires smartmontools and privileges to check the disk temperatures

    ~ $ ./check_smarttemp.js [warning temp] [critical temp] [zpool]
    OK: Mean temp: 40 C
