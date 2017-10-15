"use strict";

function Mutator(name, description) {
    this.name = name;
    this.description = description;
}

Mutator.prototype.eligibleElements = function(page) {
    return page.evaluate(this.findElementsPageContext());
}

Mutator.prototype.mutate = function(element) {
    return this.mutateElement(element.cloneNode(true));
}

Mutator.prototype.findElementsPageContext = function() {
    return [];
}

Mutator.prototype.mutateElement = function(element) {
    return element;
}

module.exports = Mutator;
