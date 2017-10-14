#!/bin/bash

# Run when provisioning a new vagrant box to setup and install the required software

apt-get update
apt-get upgrade -y

# Ampere (Mutation)
#apt-get install -y phantomjs
# Installing via apt-get is broken (https://github.com/ariya/phantomjs/issues/14376)
apt-get install -y fontconfig
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
bzip2 -d phantomjs-2.1.1-linux-x86_64.tar.bz2
tar -xvf phantomjs-2.1.1-linux-x86_64.tar
cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
