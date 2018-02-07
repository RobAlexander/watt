#!/bin/bash

ROOTPATH=$WATT_ROOT
SETUPPATH=$ROOTPATH/vagrant-setup
PACKAGEINSTALLER=$SETUPPATH/packages.sh

# Start by updating the box
echo "=Ubuntu="
$SETUPPATH/machine.sh

# AChecker
$PACKAGEINSTALLER achecker
