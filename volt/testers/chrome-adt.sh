#!/bin/bash

# accessibility-developer-tools testing script
#
# Passes all arguments to chrome-adt.js
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

phantomjs ${DIR}/chrome-adt.js $1 $2
