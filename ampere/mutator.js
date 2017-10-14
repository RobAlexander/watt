"use strict";

class Mutator {
    constructor(name, description) {
        this.name = name;
        this.description = description;
    }

    eligibleElements(page) {
        return page.evaluate(this.findElementsPageContext);
    }

    mutate(element) {
        return this.mutateElement(element.cloneNode(true));
    }

    findElementsPageContext() {
        return [];
    }

    mutateElement(element) {
        return element;
    }
}
