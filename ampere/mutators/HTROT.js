"use strict";

var Mutator = require('../mutator');

const jsdom = require("jsdom");
const { JSDOM } = jsdom;

function HTROT() {
    Mutator.call(this, "HTROT", "Rotate heading tag values (1 becomes 6, 2 becomes 1, etc)");
}

HTROT.prototype = Object.create(Mutator.prototype);
HTROT.prototype.constructor = HTROT;

HTROT.prototype.findEligibleElementsInDocument = function(document) {
    return [].slice.call(document.getElementsByTagName("h1")).concat(
        [].slice.call(document.getElementsByTagName("h2")),
        [].slice.call(document.getElementsByTagName("h3")),
        [].slice.call(document.getElementsByTagName("h4")),
        [].slice.call(document.getElementsByTagName("h5")),
        [].slice.call(document.getElementsByTagName("h6"))
    );
}

HTROT.prototype.mutateElement = function(element) {
    var headingLevel = parseInt(element.tagName.charAt(1)) - 1;
    if (headingLevel === 0) headingLevel = 6;
    var newElem = new JSDOM("<!DOCTYPE html>").window.document.createElement("h" + headingLevel);
    for (var i = 0; i < element.attributes.length - 1; i++) {
        newElem.setAttribute(element.attributes[i].name, element.attributes[i].value);
    }
    newElem.innerHTML = element.innerHTML;
    return newElem;
}

module.exports = new HTROT();
