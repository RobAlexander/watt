#!/bin/phantomjs

/* Ampere (HTML and CSS Mutation script)
 *
 * Performs HTML and CSS mutations on .html files
 */

"use strict";

require('../common/common'); // Used to patch in some common extra functionality
var system = require('system'), fs = require('fs'), webpage = require('webpage');

var ampereName = "Ampere";
var ampereVersion = "0.0.1";
var ampereDirectory = fs.workingDirectory;
if (!ampereDirectory.endsWith(ampereName.toLowerCase())) {
    ampereDirectory += fs.separator + ampereName.toLowerCase();
}
var generatedPagesDirectory = "run" + fs.separator + "pages";

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
} else {
    options.page = fs.absolute(options.page);
}
options.mutations.forEach(function(element) {
    if (!checkMutatorExists(element)) {
        console.error(element + " mutator not found");
        phantom.exit(2);
    }
}, this);

// Load the base page
var page = webpage.create();
page.open("file:///" + options.page, function(status) {
    if (status !== 'success') {
        console.error("Unable to load page");
        phantom.exit(2);
    } else {
        // Mutate according to mutators specified
        options.mutations.forEach(function(mutationOperator) {
            var mutator = require('./mutators/' + mutationOperator);
            console.log("Performing mutations with " + mutator.name);
            var mutants = mutatePage(page, mutator, (options.options.indexOf('s') != -1 ? 1 : Infinity));
            
            for(var i = 0; i < mutants.length; i++) {
                fs.makeTree(generatedPagesDirectory);
                fs.write(page.url.split("/").pop().split(".")[0] + "." + mutationOperator + "." + i + ".html", mutants[i].content, 'w');
            }
        }, this);

        phantom.exit(0);
    }
});


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
    for (i = i; i < args.length; i++) {
        mutations.push(args[i]);
    }

    return {options: options, page: page, mutations: mutations};
}

function checkMutatorExists(mutator) {
    var path = ampereDirectory + fs.separator + "mutators" + fs.separator + mutator + ".js";
    return fs.exists(path);
}

function mutatePage(page, mutator, limit) {
    if (limit === undefined) {
        limit = Infinity;
    }

    var matches = mutator.eligibleElements(page);
    console.log("Found " + matches.length + " possible mutation" + ((matches.length != 1) ? "s" : ""));

    var mutants = [];
    for (var i = 0; i < Math.min(matches.length, limit); i++) {
        console.log("Mutating eligible element " + i);

        var match = matches[i];
        console.log("a");
        var revert = page.evaluate(function(match) {
            return match.cloneNode(true);
        }, match);
        console.log("a");
        var mutated = mutator.mutate(match);
        console.log("a");

        // Place the mutated code into the page
        page.evaluate(function() {
            var parent = match.parentNode;
            parent.replaceChild(mutated, match);
        });
        console.log("a");

        // Clone the page
        var mutantTree = page.evaluate(function() {
            return document.documentElement.cloneNode(true);
        });
        var mutantPage = webpage.create();
        mutantPage.evaluate(function() {
            document.replaceChild(mutantPage, document.documentElement);
        });
        console.log("a");

        mutants.push(mutantPage);

        // Revert the mutation
        page.evaluate(function() {
            var parent = mutated.parentNode;
            parent.replaceChild(match, mutated);
        });
        console.log("a");
    }

    return mutants;
}
