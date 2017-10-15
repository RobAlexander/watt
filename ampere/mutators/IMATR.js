"use strict";

var Mutator = require('../mutator');

function IMATR() {
    Mutator.call(this, "IMATR", "Remove Alt Tag from image");
}

IMATR.prototype = Object.create(Mutator.prototype);
IMATR.prototype.constructor = IMATR;

IMATR.prototype.findEligibleElementsInDocument = function(document) {
    return document.getElementsByTagName("img");
}

IMATR.prototype.mutateElement = function(element) {
    element.removeAttribute("alt");
    return element;
}

module.exports = new IMATR();
