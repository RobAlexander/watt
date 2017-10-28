#!/bin/bash

# Run when starting a vagrant box, regardless of provisioning state

echo "Starting Jenkins server"
cd /vagrant/weber
forever start -c bash ./jenkins.sh
