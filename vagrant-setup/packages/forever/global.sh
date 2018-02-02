#!/bin/bash

if command -v forever 2>&1 1>/dev/null
then
    echo "Forever already installed"
else
    npm install forever -g
fi
