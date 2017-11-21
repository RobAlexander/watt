#!/bin/bash

# aXe Speech testing script
#
# Passes all arguments to axe-phantomjs.js and adds -s flag
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

phantomjs ${DIR}/axe-phantomjs.js $1 $2 -s
