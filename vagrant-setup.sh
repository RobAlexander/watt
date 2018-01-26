#!/bin/bash

# Start by updating the box
echo "=Ubuntu="
apt-get update
apt-get upgrade -y

# Run when provisioning a new vagrant box to setup and install the required software
echo "=watt="

# Ampere (Mutation)
echo "==Ampere=="
cd $WATT_ROOT/ampere
echo "===NodeJS Setup==="
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs

echo "===Ampere Package==="
npm install --no-bin-links  # See https://github.com/npm/npm/issues/9901

# Volt (Run testers)
echo "==Volt=="
cd $WATT_ROOT/volt
echo "===PhantomJS==="
# Installing via apt-get is broken (https://github.com/ariya/phantomjs/issues/14376)
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

echo "===Volt Package==="
npm install --no-bin-links

# Tesla (Analyse results)
echo "==Tesla=="
echo "===Python3==="
apt-get install -y python3 python3-pip
pip3 install --upgrade pip

# Weber (UI and Automation)
echo "==Weber=="
cd $WATT_ROOT/weber
echo "===Forever==="
npm install forever -g

echo "===JDK==="
apt-get install -y default-jdk

echo "===Jenkins==="
if [ -e jenkins.war ]
then
    echo "Jenkins alredy installed"
else
    wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war
fi
mkdir -p $JENKINS_HOME/users/admin
mkdir -p $JENKINS_HOME/jobs/WATT
ln -sf $WATT_ROOT/weber/jenkins-config.xml $JENKINS_HOME/config.xml
ln -sf $WATT_ROOT/weber/jenkins-user.xml $JENKINS_HOME/users/admin/config.xml
ln -sf $WATT_ROOT/weber/jenkins-job.xml $JENKINS_HOME/jobs/WATT/config.xml
#ln -sf $WATT_ROOT/weber/env.sh /etc/profile.d/weber.sh

echo "===Weber Package==="
pip3 install -r requirements.txt

# Ohm (Modelling)
echo "==Ohm=="
cd $WATT_ROOT/ohm
echo "===Epsilon==="
if [ -e epsilon-1.4-kitchensink.jar ]
then
    echo "Epsilon already installed"
else
    wget http://mirrors.nic.cz/eclipse/epsilon/jars/epsilon-1.4-kitchensink.jar
fi

echo "===Ant==="
apt-get install -y ant

echo "===Jenkins==="
mkdir -p $JENKINS_HOME/jobs/mutators
ln -sf $WATT_ROOT/ohm/jenkins-job.xml $JENKINS_HOME/jobs/mutators/config.xml
