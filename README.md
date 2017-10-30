# Website Accessibility Tester Tester (WATT)

Developed as part of a final year project at the University of York which attempts to test the reliability of website accessibility testing tools using mutation testing.

This tool can only generate and test mutants which are well formed HTML and CSS.  No attempt is made to handle invalid HTML or CSS.

## Components

### Ampere

Webpage mutator written as a set of NodeJS scripts which are used to apply mutations to a reference webpage.

Reference pages are stored within the `ampere/pages` directory.  Pages which are to be used in mutation testing, which include copies of the original pages and pages with the specified mutations applied are stored in the `run/pages` directory.

Mutators are stored in the `ampere/mutators` directory.  Mutators are stored with the mutation operator name as the filename and conform to the mutator specification.

### Volt

Runs tests against all pages (original and mutants) to generate reports (FUTURE and modifies into a standard format to allow analysis).

Results are stores in the `run/results` directory.

Interfaces to testing tools are stored in `volt\testers`.  Any code or binaries required beyond this must be installed either by the volt `package.json` or in the global `vagrant-setup.sh`.  (FUTURE tools will be able to set-up based on testing specification)

### Tesla

Scripts to take outputs from mutation testing tools and generate basic mutation statistics from them.

(FUTURE this should be able to do much more advanced data analytics than it can currently, and should really become some whole system which can allow some nice interactive analysis (such as Jupyter, or something slightly less overkilly))

### Weber

Runs some nice interfaces to allow automatic testing to take place.  A Web UI is brought up on port `8080` and a Jenkins server on port `8081`, accessible on both the host and the vagrant development machine.

The Web UI allows viewing of previously run jobs (currently listing only the 50 most recent but URL access to any), including displaying analysis results at appropriate points.  All data is retrieved from Jenkins. (FUTURE this should handle new jobs, running jobs and failed jobs and offer some sort of live updating)

Jenkins can be used to trigger jobs by running a parameterised build of the `WATT` job.  There is no checking if parameters are correct. Login using username and password `admin`.  (FUTURE something really, really should be done to give it a reasonable security setup when the server is initialised)

### Joule

Renders PNG versions of pages in Base64.

### Henry

Bash script which removes any intermediary files in the recommended locations above.

## Running

To run navigate to the root of the repository and run `vagrant up`, assuming both Vagrant and a virtualisation provider (such as VirtualBox) are installed.  Weber will be available on the ports described above.
