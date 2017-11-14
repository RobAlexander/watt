#!/usr/bin/nodejs

'use strict';

const child_process = require('child_process');
const vnu = require('vnu-jar');
const fs = require('fs');

child_process.exec(`java -jar ${vnu} --format json --exit-zero-always ${process.argv[2]}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`exec error: ${error}`);
        process.exit(1);
    }
    var output = JSON.parse(stderr);
    var data = {"violations": []};
    output['messages'].forEach(function(element) {
        if (element['type'] == "error") {
            data['violations'].push({
                "message": element['message'],
                "id": "invalid",
                "help": "",
                "helpUrl": "",
                "nodes": [
                    {"html": element['extract']}
                ]
            });
        }
    });
    fs.writeFileSync(process.argv[3], JSON.stringify(data), 'utf8');
    process.exit(0);
});
