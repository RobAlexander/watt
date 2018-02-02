#!/bin/bash

if command -v node 2>&1 1>/dev/null
then
    echo "NodeJS already installed"
else
    curl -sL https://deb.nodesource.com/setup_6.x | bash -
    apt-get install -y nodejs
fi
