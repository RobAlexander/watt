"use strict";

var Mutator = require('../mutator');

function STLRM() {
    Mutator.call(this, "STLRM", "Remove Skip to Links");
}

STLRM.prototype = Object.create(Mutator.prototype);
STLRM.prototype.constructor = STLRM;

STLRM.prototype.findEligibleElementsInDocument = function(document) {
    var skipTo = [];
    var links = document.getElementsByTagName("a");
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (link.textContent.toLowerCase().startsWith("skip to")) {
            skipTo.push(link);
        }
    }
    return skipTo;
}

STLRM.prototype.mutateElement = function(element) {
    element.removeAttribute("href");
    return element;
}

module.exports = new STLRM();
