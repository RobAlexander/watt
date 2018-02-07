#!/bin/bash

if command -v mysql 2>&1 1>/dev/null
then
    echo "MySQL already installed"
else
    echo mysql-server mysql-server/root_password password qwerty | debconf-set-selections
    echo mysql-server mysql-server/root_password_again password qwerty | debconf-set-selections
    apt-get install -y mysql-server
fi
