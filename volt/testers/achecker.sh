#!/bin/bash

# achecker testing script
#
# Passes all arguments to achecker.js
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

node ${DIR}/achecker.js $1 $2
