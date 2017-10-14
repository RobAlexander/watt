# Website Accessibility Tester Tester (WATT)

Developed as part of a final year project at the University of York which attempts to test the reliability of website accessibility testing tools using mutation testing.

This tool can only generate and test mutants which are well formed HTML and CSS.  No attempt is made to handle invalid HTML or CSS.

## Components

### Ampere

Webpage mutator written as a series of scripts which are used by PhantonJS to apply mutations to a reference webpage.

Reference pages are stored within the `ampere/pages` folder.  Pages which are to be used in mutation testing, which include copies of the original pages and pages with the specified mutations applied are stored in the `run\pages` directory.

Mutators are stored in the `ampere/mutators` directory.  Mutators are stored with the mutation operator name as the filename and conform to the mutator specification.
