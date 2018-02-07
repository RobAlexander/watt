#!/bin/bash

if command -v apache2ctl 2>&1 1>/dev/null
then
    echo "apache2 already installed"
else
    apt-get install -y apache2

    currentpath="$( cd "$(dirname "$0")" ; pwd -P )"
    portsconfpath=/etc/apache2/ports.conf
    rm -rf $portsconfpath
    ln -sf $currentpath/ports.conf $portsconfpath
    systemctl restart apache2
fi
