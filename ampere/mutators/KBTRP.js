"use strict";

var Mutator = require('../mutator');

const jsdom = require("jsdom");
const { JSDOM } = jsdom;

function KBTRP() {
    Mutator.call(this, "KBTRP", "Add a keyboard trap to the page");
}

KBTRP.prototype = Object.create(Mutator.prototype);
KBTRP.prototype.constructor = KBTRP;

KBTRP.prototype.findEligibleElementsInDocument = function(document) {
    return document.getElementsByTagName("body");
}

KBTRP.prototype.mutateElement = function(element) {
    var field = new JSDOM("<!DOCTYPE html>").window.document.createElement("input");
    field.setAttribute("type", "text");
    field.setAttribute("onkeydown", "return false;");
    var label = new JSDOM("<!DOCTYPE html>").window.document.createElement("label");
    label.appendChild(new JSDOM("<!DOCTYPE html>").window.document.createTextNode("Field"));
    label.appendChild(field);
    var div = new JSDOM("<!DOCTYPE html>").window.document.createElement("div");
    div.setAttribute("role", "complementary");
    div.appendChild(label);
    element.appendChild(div);
    return element;
}

module.exports = new KBTRP();
