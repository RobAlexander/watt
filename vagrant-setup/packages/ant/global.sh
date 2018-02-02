#!/bin/bash

if command -v ant 2>&1 1>/dev/null
then
    echo "Ant already installed"
else
    apt-get install -y ant
fi
