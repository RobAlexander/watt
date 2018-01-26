#!/bin/bash

# Run when starting a vagrant box, regardless of provisioning state
echo "Starting Jenkins server"
cd $WATT_ROOT/weber
forever start -c bash jenkins.sh
forever start -c python3 weber.py $WATT_ROOT/config.json
