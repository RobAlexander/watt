#!/bin/bash

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
