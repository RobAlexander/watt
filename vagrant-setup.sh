#!/bin/bash

# Run when provisioning a new vagrant box to setup and install the required software
echo "=watt="
apt-get update
apt-get upgrade -y

# Ampere (Mutation)
echo "==Ampere=="
cd /vagrant/ampere
echo "===NodeJS Setup==="
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs

echo "===Ampere Package==="
npm install --no-bin-links  # See https://github.com/npm/npm/issues/9901

# Volt (Run testers)
echo "==Volt=="
cd /vagrant/volt
echo "===PhantomJS==="
# Installing via apt-get is broken (https://github.com/ariya/phantomjs/issues/14376)
if [ -e /usr/bin/phantomjs ]
then
    echo "PhantomJS already installed"
else
    PHANTOM_VERSION=phantomjs-2.1.1-linux-x86_64
    apt-get install -y fontconfig
    wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_VERSION.tar.bz2
    bzip2 -d $PHANTOM_VERSION.tar.bz2
    tar -xvf $PHANTOM_VERSION.tar
    cp $PHANTOM_VERSION/bin/phantomjs /usr/bin/phantomjs
    rm -rf $PHANTOM_VERSION
    rm -f $PHANTOM_VERSION.tar
    rm -f $PHANTOM_VERSION.tar.bz2
fi

echo "===Volt Package==="
npm install --no-bin-links

# Tesla (Analyse results)
echo "==Tesla=="
echo "===Python3==="
apt-get install -y python3 python3-pip
