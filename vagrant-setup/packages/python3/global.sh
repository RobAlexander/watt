#!/bin/bash

if command -v python3 2>&1 1>/dev/null
then
    echo "Python3 already installed"
else
    apt-get install -y python3 python3-pip
    pip3 install --upgrade pip
fi
