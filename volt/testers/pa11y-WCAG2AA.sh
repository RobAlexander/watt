#!/bin/bash

# pa11y (HTML_CS) testing script
#
# Passes all arguments to htmlcs-pa11y.js with conformance level specified
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

node ${DIR}/htmlcs-pa11y.js $1 $2 WCAG2AA
