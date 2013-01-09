# Various Nagios scripts created by me
====================

Plugins
-------

### check_cpuload

Check the CPU load in SmartOS global zone

    ~ $ ./check_cpuload -w [warning] -c [critical]
    OK: CPU load: 15%

### check_cputemp_freebsd.py

Check the CPU temperature in FreeBSD

    ~ $ ./check_cputemp_freebsd.py -C [core] -w [warning] -c [critical]
    OK: CPU Temperature: 49 C