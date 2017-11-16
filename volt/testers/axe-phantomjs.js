#!/bin/phantomjs

// Code reused from https://github.com/dequelabs/axe-core/blob/develop/doc/examples/phantomjs/axe-phantom.js

/*global window, phantom */
const PATH_TO_AXE = '../node_modules/axe-core/axe.min.js';

var args = require('system').args;
var fs = require('fs');
var page = require('webpage').create();

if (args.length < 2) {
	console.log('axe-phantomjs.js accepts 2 arguments, the URL to test and output file');
	phantom.exit(1);
}

page.open(args[1], function (status) {
	// Check for page load success
	console.log(args[1]);
	if (status !== 'success') {
		console.log('Unable to access network');
		phantom.exit(2);
	}

	page.injectJs(PATH_TO_AXE);
	page.framesName.forEach(function (name) {
		page.switchToFrame(name);
		page.injectJs(PATH_TO_AXE);
	});
	page.switchToMainFrame();
	page.evaluateAsync(function () {
		const AXE_OPTIONS = {
			"rules": {
				"heading-order": {"enabled": true},
				"href-no-hash": {"enabled": true},
				"label-title-only": {"enabled": true},
				"region": {"enabled": true},
				"skip-link": {"enabled": true}
			}
		};

		/*global axe */
		axe.run(document, AXE_OPTIONS, function (err, results) {
			if (err)  {
				throw err;
			}
			window.callPhantom(results);
		});
	});

	page.onCallback = function (msg) {
		if (args[2]) {
			fs.write(args[2], JSON.stringify(msg, null, '  '), 'w');
		} else {
			console.log(JSON.stringify(msg, null, '  '));
		}

		phantom.exit();
	};
});
