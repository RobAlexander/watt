#!/bin/bash

# Run when starting a vagrant box, regardless of provisioning state
source /etc/profile.d/weber.sh

echo "Starting Jenkins server"
cd /vagrant/weber
forever start -c bash jenkins.sh
forever start -c python3 weber.py /vagrant/config.json
