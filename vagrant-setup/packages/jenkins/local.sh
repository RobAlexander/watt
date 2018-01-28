#!/bin/bash

if [ -e jenkins.war ]
then
    echo "Jenkins alredy installed"
else
    wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war
fi
