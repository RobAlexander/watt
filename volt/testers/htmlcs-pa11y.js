#!/bin/node

// Runs HTMLCS to specified accuracy level and saves results to file in aXe format

const pa11y = require('pa11y');
const fs = require('fs');

var test = pa11y({
    standard: process.argv[4]
});

test.run(process.argv[2], function (error, results) {
    if (error) {
        console.log(error);
        process.exit(1);
    }

    var data = {"violations": [], "passes": [], "incomplete": [], "inapplicable": []};

    results.forEach(result => {
        var resultObject = {
            "message": result['message'],
            "id": result['code'],
            "nodes": [{
                "html": result['context'],
                "target": result['selector']
            }],
            "help": "",
            "helpUrl": "",
            "impact": result['type']
        };

        switch (result.type) {
            case 'error':
            case 'warning':
                data['violations'].push(resultObject);
                break;
            case 'notice':
                data['incomplete'].push(resultObject);
                break;
        }
    });

    fs.writeFileSync(process.argv[3], JSON.stringify(data), 'utf8');
    process.exit(0);
});
