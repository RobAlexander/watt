#!/bin/node

/* Ampere (HTML Mutation script)
 *
 * Performs HTML mutations on .html files
 */

"use strict";

require('../common/common'); // Used to patch in some common extra functionality
var fs = require('fs'), path = require("path"), jsdom = require("jsdom");
const { JSDOM } = jsdom;

var ampereName = "Ampere";
var ampereVersion = "0.0.1";
var ampereDirectory = __dirname;
if (!ampereDirectory.endsWith(ampereName.toLowerCase())) {
    ampereDirectory += path.sep + ampereName.toLowerCase();
}

console.log(ampereName + " " + ampereVersion);

const argv = require('yargs')
             .command('pages <dir> <output>', 'Mutate all pages in a directory', (yargs) => {
                 yargs
                 .positional('dir', {describe: "The directory containing pages to mutate"})
                 .positional('output', {describe: "The directory to save mutants to"})
             })
             .command('$0 <page> <output>', 'Mutate a page', (yargs) => {
                 yargs
                 .positional('page', {describe: "The page to mutate"})
                 .positional('output', {describe: "The directory to save mutants to"})
             })
             .options('mutators', {
                 alias: 'm',
                 array: true,
                 requiresArg: true,
                 description: "Mutators to be applied"
             })
             .option('single', {
                 alias: 's',
                 default: false,
                 description: "Only apply the mutant in the first available position"
             })
             .argv;

argv.mutators.forEach(function(element) {
    if (!checkMutatorExists(element)) {
        console.error(element + " mutator not found");
        process.exit(2);
    }
}, this);

var generatedPagesDirectory = argv.output;

var pagesList = [];
if (argv.dir) {
    fs.readdirSync(argv.dir).forEach(page => {
        var pagePath = path.join(argv.dir, page);
        if (!fs.statSync(pagePath).isDirectory()) {
            pagesList.push(pagePath);
        }
    });
} else {
    pagesList = [argv.page]
}

var totalMutants = 0;


pagesList.forEach(pagePath => {
    console.log("Working with page " + pagePath);

    // Load the base page
    var page = new JSDOM(fs.readFileSync(pagePath, "utf8"), {runScripts: "outside-only"});

    // Mutate according to mutators specified
    argv.mutators.forEach(function(mutationOperator) {
        var mutator = require('./mutators/' + mutationOperator);
        console.log("Performing mutations with " + mutator.name);
        var mutants = mutatePage(page, mutator, (argv.single ? 1 : Infinity));

        makeDirectoryTree(generatedPagesDirectory);
        var originalPageName = pagePath.split(path.sep).pop().split(".")[0];
        fs.writeFileSync(path.join(generatedPagesDirectory, originalPageName + ".html"), page.serialize());
        for (var i = 0; i < mutants.length; i++) {
            var fileName = originalPageName + "." + mutationOperator + "." + i + ".html";

            // Replace the page document with the mutant's to ensure we maintain the doctype when serializing
            //page.window.document.replaceChild(mutants[i].window.document.documentElement, page.window.document.documentElement);

            fs.writeFileSync(path.join(generatedPagesDirectory, fileName), mutants[i].serialize());
            totalMutants++;
        }
    }, this);
});

console.log(totalMutants + " mutants generated");
process.exit(0);


function checkMutatorExists(mutator) {
    var mutatorPath = path.join(ampereDirectory,  "mutators", mutator + ".js");
    return fs.existsSync(mutatorPath);
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

function mutatePage(page, mutator, limit) {
    if (limit === undefined) {
        limit = Infinity;
    }

    var matches = mutator.eligibleElements(page).length;
    console.log("Found " + matches + " possible mutation" + ((matches != 1) ? "s" : ""));

    var mutants = [];
    for (var i = 0; i < Math.min(matches, limit); i++) {
        console.log("Mutating eligible element " + i);

        // Clone the page
        //var mutantTree = page.window.document.documentElement.cloneNode(true);
        var mutantPage = new JSDOM(page.serialize());
        //mutantPage.window.document.replaceChild(mutantTree, mutantPage.window.document.documentElement);

        var match = mutator.eligibleElements(mutantPage)[i]; // The match needs to be regenerated since we've cloned the page
        var mutated = mutator.mutate(match);

        // Place the mutated code into the page
        var parent = match.parentNode;
        parent.replaceChild(mutated, match);

        // Store cloned page
        mutants.push(mutantPage);
    }

    return mutants;
}
