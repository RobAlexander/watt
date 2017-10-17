#!/bin/node

/* Ampere (HTML Mutation script)
 *
 * Performs HTML mutations on .html files
 */

"use strict";

require('../common/common'); // Used to patch in some common extra functionality
var fs = require('fs'), path = require("path"), child_process = require("child_process");

var voltName = "Volt";
var voltVersion = "0.0.1";
var voltDirectory = process.cwd();
if (!voltDirectory.endsWith(voltName.toLowerCase())) {
    voltDirectory += path.sep + voltName.toLowerCase();
}
var resultsDirectory = "run" + path.sep + "results";

console.log(voltName + " " + voltVersion);

var options = parseOptions(process.argv);
if (options === false) {
    console.log("Usage: " + process.argv[1] + " <pages> [<tester> ..]");
    process.exit(1);
}
if (!fs.statSync(options.pages).isDirectory()) {
    console.error("Pages directory " + options.pages + " not found");
    process.exit(2);
} else {
    options.pages = path.resolve(options.pages);
}
options.testers.forEach(function(element) {
    if (!checkTesterExists(element)) {
        console.error(element + " tester not found");
        process.exit(2);
    }
}, this);

// Build page list
const checksum = require("checksum");
var pagesData = "", pagesFile = path.join(resultsDirectory, "pages.lst");
fs.readdirSync(options.pages).forEach(page => {
    if (!fs.statSync(path.join(options.pages, page)).isDirectory()) {
        pagesData += page + " " + checksum(fs.readFileSync(path.join(options.pages, page), "utf8")) + "\n";
    }
});
makeDirectoryTree(resultsDirectory);
fs.writeFile(pagesFile, pagesData);

var serverPort = 5000;
var server = child_process.exec("node " + path.join(voltDirectory, "server.js") + " " + options.pages + " " + serverPort);

setTimeout(function() {
    // Run each tester
    options.testers.forEach(tester => {
        var testerDirectory = path.join(resultsDirectory, tester);
        makeDirectoryTree(testerDirectory);
        console.log("Running tests with " + tester);
        pagesData.split("\n").forEach(pageData => {
            if (pageData !== "") {
                child_process.execSync(path.join(voltDirectory, "testers", tester + ".sh") + " http://localhost:" + serverPort + "/" + pageData.split(" ")[0] + " " + path.join(testerDirectory, pageData.split(" ")[0] + ".json"));
            }
        });
        console.log("Completed tests with " + tester);
    });

    server.kill();
    process.exit(0);
}, 5000);

function parseOptions(args) {
    if (args.length < 4) {
        return false;
    }
    var pages, testers=[];
    var i = 2; // NodeJS args contain both the node executable and the script name
    // Pages
    pages = args[i];
    i++;
    // Testers
    for (i = i; i < args.length; i++) {
        testers.push(args[i]);
    }

    return {pages: pages, testers: testers};
}

function checkTesterExists(tester) {
    var testerPath = voltDirectory + path.sep + "testers" + path.sep + tester + ".sh";
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
