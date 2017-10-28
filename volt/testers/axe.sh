#!/bin/bash

# aXe testing script
#
# Passes all arguments to axe-phantomjs.js
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

phantomjs ${DIR}/axe-phantomjs.js $1 $2
