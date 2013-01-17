#!/usr/node/bin/node
/*
check_smarttemp.js
*/
var fs = require('fs');
var exec = require('child_process').exec;
var child;
var disks = [];
var totaltemp = 0;
var test = 0;

smartctlbin="/opt/custom/sbin/smartctl"

// Process disks from argv
function processargs() {
        process.argv.forEach(function (val, index, array) {
                if(index > 3) {
                        disks[index-4] = val;
                        if (fs.existsSync("/dev/rdsk/" + val) == false) {
                        	console.log("Disk /dev/rdsk/" + val + " does not exist");
                        	process.exit(3);
                        }
                };
		if(index == process.argv.length-1) {
			disktemps();
		};
        });
};

//Get temps from the disks usins smartctl
function disktemps() {
        for (i=0; i < disks.length; i++){
                child = exec(smartctlbin + " -a -d scsi /dev/rdsk/" + disks[i] + "|grep Current|awk '{print $4}'", function (error, stdout, stderr) {
                	totaltemp = totaltemp + parseInt(stdout);
			test++;
			
			if(disks.length == test) {
				gettemp();
			};
		});
        };
};

//Calculate the mean temp
function gettemp() {
	//Get warn and crit temps from argv
	warn = process.argv[2];
	crit = process.argv[3];

	// Check warn and crit values for errors etc.
	if ((/^\d*$/.test(warn) == false) ||  (/^\d*$/.test(crit) == false)) {
		console.log("Warning or critical value is not integer.");
		process.exit(3);
	}

	if (warn >= crit) {
		console.log("Warning value can't be bigger than or equal to crit value");
		process.exit(3);
	}

	//Calculate the mean temperature of the disks and write it to console. Raise proper exit value.
	totaltemp = totaltemp / disks.length;

	if(totaltemp < warn) {
		console.log("OK: Mean temp " + totaltemp + " C");
		process.exit(0);
	}
	else if(totaltemp > warn && totaltemp < crit) {
		console.log("WARNING: Mean temp " + totaltemp + " C");
		process.exit(1);
	}
	else {
		console.log("CRITICAL: Mean temp " + totaltemp + " C");
		process.exit(2);
	}
};

//Call the first function
processargs();
