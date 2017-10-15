"use strict";

/* Written as a class using the standard ES5 method to maintain compatibility with software using
 * older specifications (such as PhantomJS)
 * See https://gist.github.com/remarkablemark/fa62af0a2c57f5ef54226cae2258b38d
 */

function Mutator(name, description) {
    this.name = name;
    this.description = description;
}

Mutator.prototype.eligibleElements = function(page) {
    return this.findEligibleElementsInDocument(page.window.document);
}

Mutator.prototype.mutate = function(element) {
    return this.mutateElement(element.cloneNode(true));
}

Mutator.prototype.findEligibleElementsInDocument = function(document) {
    return [];
}

Mutator.prototype.mutateElement = function(element) {
    return element;
}

module.exports = Mutator;
