#!/bin/bash

if command -v unzip 2>&1 1>/dev/null
then
    echo "unzip already installed"
else
    apt-get install -y unzip
fi
