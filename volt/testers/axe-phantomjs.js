#!/bin/phantomjs

// Code modified from https://github.com/dequelabs/axe-core/blob/develop/doc/examples/phantomjs/axe-phantom.js

/*global window, phantom */
const PATH_TO_AXE = '../node_modules/axe-core/axe.min.js';

var args = require('system').args;
var fs = require('fs');
var page = require('webpage').create();

if (args.length < 2) {
	console.log('axe-phantomjs.js <url> <output> [-s]');
	phantom.exit(1);
}
var speech = false;
if (args.length >= 4 && args[3] == "-s") {
	speech = true;
}

page.open(args[1], function (status) {
	// Check for page load success
	console.log(args[1]);
	if (status !== 'success') {
		console.log('Unable to access network');
		phantom.exit(2);
	}

	page.injectJs(PATH_TO_AXE);
	if (speech) {
		speechToScreen(page);
	}
	page.framesName.forEach(function(name) {
		page.switchToFrame(name);
		page.injectJs(PATH_TO_AXE);
		if (speech) {
			speechToScreen(page);			
		}
	});
	console.log("main");
	page.switchToMainFrame();
	page.evaluateAsync(function() {
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

	page.onCallback = function(msg) {
		if (args[2]) {
			fs.write(args[2], JSON.stringify(msg, null, '  '), 'w');
		} else {
			console.log(JSON.stringify(msg, null, '  '));
		}

		phantom.exit();
	};
});

function speechToScreen(pageObj) {
	pageObj.evaluate(function() {
		for (var i  = 0; i < document.styleSheets.length; i++) {
			for (var j = 0; j < document.styleSheets[i].rules.length; j++) {
				if ("media" in document.styleSheets[i].rules[j]) {
					switch (document.styleSheets[i].rules[j].media.mediaText) {
						case "screen":
							document.styleSheets[i].rules[j].media.mediaText = "speech";
							break;
						case "speech":
							document.styleSheets[i].rules[j].media.mediaText = "screen";
							break;
					}
				}
			}
		}
	});
}
