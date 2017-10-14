class IMAT extends Mutator("IMATR", "Remove Alt Tag from image") {
    findElementsPageContext() {
        return document.getElementsByTagName("img");
    }

    mutateElement(element) {
        element.removeAttribute("alt");
        return newElem;
    }
}
