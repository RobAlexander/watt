#!/bin/bash

# vnu testing script
#
# Passes all arguments to vnu.js
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

node ${DIR}/vnu.js $1 $2
