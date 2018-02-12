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

Interfaces to testing tools are stored in `volt\testers`.  Any code or binaries required beyond this must be installed either by the volt `package.json` or in the global `vagrant-setup.sh`.

A second virtual machine called BRANCHNAME-achecker is setup for use with AChecker since it has different system requirements to the rest of the system.

### Tesla

Scripts to take outputs from mutation testing tools and generate basic mutation statistics from them.

(FUTURE this should be able to do much more advanced data analytics than it can currently, and should really become some whole system which can allow some nice interactive analysis (such as Jupyter, or something slightly less overkilly))

### Weber

Runs some nice interfaces to allow automatic testing to take place.  A Web UI is brought up on port `8080` and a Jenkins server on port `8081`, accessible on both the host and the vagrant development machine.

The Web UI allows viewing of previously run jobs (currently listing only the 50 most recent but URL access to any), including displaying analysis results at appropriate points.  All data is retrieved from Jenkins. (FUTURE this should handle new jobs, running jobs and failed jobs and offer some sort of live updating)

Jenkins can be used to trigger jobs by running a parameterised build of the `WATT` job.  There is no checking if parameters are correct. Login using username and password `admin`. (FUTURE Jenkins should be in the background only and not exposed to the host machine)

### Ohm

Stores a metamodel for mutation operators and generates the requisite files and folders needed to power the operations.

### Joule

Renders PNG versions of pages in Base64.

### Henry

Bash script which removes any intermediary files in the recommended locations above.

## Running

To run navigate to the root of the repository and run `vagrant up`, assuming both Vagrant and a virtualisation provider (such as VirtualBox) are installed.  To allow networking to be set up correctly between the VMs you may need administrator access to your machine, or be able to enter a local administrators credentials when prompted.  Weber will be available on the ports described above once the VMs have provisioned themselves.  Open a web browser pointed at http://localhost:8080/ to complete the setup.

Once setup is complete select "New Job" from within the UI to configure a test run and start testing.  Results will be displayed once testing is complete and can be explored within the UI and individual files downloaded.  See the `weber.py` file for a full view of the available endpoints.

### Reloading config

If changes to the config file, or any file referenced from it, are made outside of the UI then the configuration must be reloaded by going to the config screen and selecting the "Reload Configuration" option.

## Security

Everything uses very weak passwords (in some cases none at all) so should never be given external facing access.  Whilst the damage that could be done by one of th VMs being exposed to the internet is limited files in the synced directories it is still far better not to give it any at all.
