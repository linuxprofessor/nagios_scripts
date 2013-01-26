#!/usr/node/bin/node
/*

 check_smarttemp.js - Nagios plugin for checking mean disk temperatures on SmartOS using smartmontools

 # ./check_smarttemp.js [warning] [critical] [zpool]

 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License, Version 1.0 only
 * (the "License").  You may not use this file except in compliance
 * with the License.
 *
 * You can obtain a copy of the license at http://opensource.org/licenses/CDDL-1.0
 *
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file.
 *
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 *
 * Copyright (c) 2013, Marcus Wilhelmsson. All rights reserved.
 *
 */

var fs = require('fs');
var exec = require('child_process').exec;
var child;
var disks = [];
var totaltemp = 0;
var test = 0;
var counter = 0;

// Location of the smartctl binary. This binary is NEEDED for the script to work.
smartctlbin="/opt/custom/sbin/smartctl"

// Process disks from zpool given in argv
function processargs() {
	process.argv.forEach(function (val, index, array) {
		if(index == 4) {
			child = exec("/usr/sbin/zpool status " + process.argv[index] + "|grep ONLINE|grep c|awk '{print $1}'", function (error, stdout, stderr) {
				disks = stdout.split("\n");
				disks.pop();
				disktemps();
			});
		};
	});
};

// Get temps from the disks usins smartctl
function disktemps() {
	for (i=0; i < disks.length; i++){
		child = exec(smartctlbin + " -a -d scsi /dev/rdsk/" + disks[i] + "|grep Current|awk '{print $4}'", function (error, stdout, stderr) {
			totaltemp = totaltemp + parseInt(stdout);
			counter++;
			if(disks.length == counter) {
				gettemp();
			};
		});
	};
};

// Calculate the mean temp
function gettemp() {
	//Get warn and crit temps from argv
	warn = parseInt(process.argv[2]);
	crit = parseInt(process.argv[3]);

	// Check warn and crit values for errors etc.
	if ((/^\d*$/.test(warn) == false) ||  (/^\d*$/.test(crit) == false)) {
		console.log("Warning or critical value is not integer.");
		process.exit(3);
	}

	if (warn >= crit) {
		console.log("Warning value can't be bigger than or equal to crit value");
		process.exit(3);
	}

	// Calculate the mean temperature of the disks and write it to console. Raise proper exit value.
	totaltemp = totaltemp / disks.length;

	if(totaltemp < warn) {
		console.log("OK: Mean temp " + totaltemp + " C|Temperature=" + totaltemp + ";" + warn + ";" + crit + ";" + (warn - 5) + ";" + (crit + 5));
		process.exit(0);
	}
	else if(totaltemp > warn && totaltemp < crit) {
		console.log("WARNING: Mean temp " + totaltemp + " C|Temperature=" + totaltemp + ";" + warn + ";" + crit + ";" + (warn - 5) + ";" + (crit + 5));
		process.exit(1);
	}
	else {
		console.log("CRITICAL: Mean temp " + totaltemp + " C|Temperature=" + totaltemp + ";" + warn + ";" + crit + ";" + (warn - 5) + ";" + (crit + 5));
		process.exit(2);
	}
};

// Call the first function
processargs();
