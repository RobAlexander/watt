#!/usr/bin/phantomjs

const PATH_TO_ADT = "../node_modules/accessibility-developer-tools/dist/js/axs_testing.js";

var page = require('webpage').create(),
    args = require('system').args,
    fs = require('fs');

page.settings.webSecurityEnabled = false;  // Allow better iframe access

if (args.length < 2) {
	console.log('chrome-adt.js <url> <output>');
	phantom.exit(1);
}

page.open(args[1], function(status) {
    console.log(args[1]);
    if (status !== 'success') {
		console.log('Unable to access network');
		phantom.exit(2);
    }
    
    page.evaluate(function() {
        // if target website has an AMD loader, remove it
        if (typeof define !== 'undefined' && define.amd) {
            define.amd = false;
        }
    });
    
    page.injectJs(PATH_TO_ADT);
    var report = page.evaluate(function() {
        var results = axs.Audit.run();
        var data = {"violations": [], "passes": [], "incomplete": [], "inapplicable": []};

        // return results;

        results.forEach(function(result) {
            var resultObject = {
                "description": result['rule'].heading,
                "id": result['rule'].name,
                "nodes": [],
                "help": "",
                "helpUrl": result['rule'].url,
                "impact": result['rule'].severity
            };

            if (result['elements']) {
                result['elements'].forEach(function(element) {
                    resultObject.nodes.push({
                        "html": element.outerHTML,
                    });
                });
            }

            switch (result['result']) {
                case 'PASS':
                    data['passes'].push(resultObject);
                    break;
                case 'FAIL':
                    data['violations'].push(resultObject);
                    break;
                default:
                    data['inapplicable'].push(resultObject);
                    break;
            }
        });

        return data;
    });
    
    if (args[2]) {
        fs.write(args[2], JSON.stringify(report, null, '  '), 'w');
    } else {
        console.log(JSON.stringify(report, null, '  '));
    }

    phantom.exit();
});
