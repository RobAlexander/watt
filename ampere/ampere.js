#!/bin/phantomjs

/* Ampere (HTML and CSS Mutation script)
 *
 * Performs HTML and CSS mutations on .html files
 */

"use strict";

require('../common/common'); // Used to patch in some common extra functionality
var system = require('system'), fs = require('fs');

var ampereName = "Ampere";
var ampereVersion = "0.0.1";
var ampereDirectory = fs.workingDirectory;
if (!ampereDirectory.endsWith(ampereName.toLowerCase())) {
    ampereDirectory += "/" + ampereName.toLowerCase();
}

console.log(ampereName + " " + ampereVersion);

var options = parseOptions(system.args);
if (options === false) {
    console.log("Usage: " + system.args[0] + " [-s] <page> [<mutation> ..]");
    console.log("    -s: Only apply mutation to the first matching mutation instance");
    phantom.exit(1);
}
if (!fs.exists(options.page)) {
    console.error("Page " + options.page + " not found");
    phantom.exit(2);
}
options.mutations.forEach(function(element) {
    if (!checkMutatorExists(element)) {
        console.error(element + " mutator not found");
        phantom.exit(2);
    }
}, this);

phantom.exit(0);


function parseOptions(args) {
    if (args.length <= 2) {
        return false;
    }
    var options = [], page, mutations=[];
    var i = 1;
    // Options
    while (args[i].startsWith('-')) {
        options.push(args[i].substring(1));
        i++;
    }
    // Page
    page = args[i];
    i++;
    // Mutations
    for(i = i; i < args.length; i++) {
        mutations.push(args[i]);
    }

    return {options: options, page: page, mutations: mutations};
}

function checkMutatorExists(mutator) {
    var path = ampereDirectory + "/mutators/" + mutator + ".json";
    return fs.exists(path);
}
