#!/bin/bash

if [ -e epsilon-1.4-kitchensink.jar ]
then
    echo "Epsilon already installed"
else
    wget http://mirrors.nic.cz/eclipse/epsilon/jars/epsilon-1.4-kitchensink.jar
fi
