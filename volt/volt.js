#!/bin/node

/* Volt (HTML Tester script)
 *
 * Runs HTML testers against .html files
 */

"use strict";

require('../common/common'); // Used to patch in some common extra functionality
var fs = require('fs'), path = require("path"), child_process = require("child_process");

// Basic config
var voltName = "Volt";
var voltVersion = "0.0.1";
var voltDirectory = __dirname;
if (!voltDirectory.endsWith(voltName.toLowerCase())) {
    voltDirectory += path.sep + voltName.toLowerCase();
}

console.log(voltName + " " + voltVersion);

// Argument parsing
const argv = require('yargs')
            .command('$0 <pages> <results>', 'Run tests against a set of pages', (yargs) => {
                yargs
                .positional('pages', {describe: "The pages to test"})
                .positional('results', {describe: "The directory to save results in"})
            })
            .options('testers', {
                alias: 't',
                array: true,
                requiresArg: true,
                description: "Testers to be run"
            })
            .argv;

var pages = argv.pages;
var resultsDirectory = argv.results;

// Find the pages directory
if (!fs.statSync(pages).isDirectory()) {
    console.error("Pages directory " + pages + " not found");
    process.exit(2);
} else {
    pages = path.resolve(pages);
}
// Check all specified testers can be found
argv.testers.forEach(function(element) {
    if (!checkTesterExists(element)) {
        console.error(element + " tester not found");
        process.exit(2);
    }
}, this);

// Build page list
const checksum = require("checksum");
var pagesData = "", pagesFile = path.join(resultsDirectory, "pages.lst");
fs.readdirSync(pages).forEach(page => {
    if (!fs.statSync(path.join(pages, page)).isDirectory()) {
        pagesData += page + " " + checksum(fs.readFileSync(path.join(pages, page), "utf8")) + "\n";  // Store page nam and a checksum
    }
});
makeDirectoryTree(resultsDirectory);
fs.writeFile(pagesFile, pagesData);

// Start page server
var serverPort = 8090;
var server = child_process.exec("node " + path.join(voltDirectory, "server.js") + " " + pages + " " + serverPort);

setTimeout(function() { // Give the server a few seconds to start working
    // Run each tester
    argv.testers.forEach(tester => {
        var testerDirectory = path.join(resultsDirectory, tester);
        makeDirectoryTree(testerDirectory);
        console.log("Running tests with " + tester);
        // Timing data array
        var timingData = {};
        // Call the tester for each page
        pagesData.split("\n").forEach(pageData => {
            if (pageData !== "") {
                var pageName = pageData.split(" ")[0];
                console.log("Testing page " + pageName);

                var startTime = Date.now();
                child_process.execSync(path.join(voltDirectory, "testers", tester + ".sh") + " http://192.168.50.100:" + serverPort + "/" + pageName + " " + path.join(testerDirectory, pageData.split(" ")[0] + ".json"));
                timingData[pageName] = Date.now() - startTime;
            }
        });
        saveTimingData(timingData, tester, resultsDirectory);
        console.log("Completed tests with " + tester);
    });

    // Shut child process down
    server.kill();
    process.exit(0);
}, 5000);


function checkTesterExists(tester) {
    var testerPath = path.join(voltDirectory, "testers", tester + ".sh");
    return fs.existsSync(testerPath);
}

function makeDirectoryTree(directoryPath) {
    var parts = directoryPath.split(path.sep);
    var curPath = "";
    for (var i = 0; i < parts.length; i++) {
        curPath += parts[i] + path.sep;
        var exists = false;
        try {
            exists = fs.statSync(curPath).isDirectory();
        } catch(e) {}
        if (!exists) {
            fs.mkdirSync(curPath);
        }
    }
}

function saveTimingData(timingData, testerName, resultsPath) {
    var finalPath = path.join(resultsPath, testerName + ".json");
    fs.writeFileSync(finalPath, JSON.stringify(timingData));
}
