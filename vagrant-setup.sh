#!/bin/bash

# Run when provisioning a new vagrant box to setup and install the required software
echo "=watt="
apt-get update
apt-get upgrade -y

# Ampere (Mutation)
echo "==Ampere=="
cd /vagrant/ampere
echo "===NodeJS Setup==="
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs

echo "===Ampere Package==="
npm install --no-bin-links  # See https://github.com/npm/npm/issues/9901

# Volt (Run testers)
echo "==Volt=="
cd /vagrant/volt
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
cd /vagrant/weber
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
mkdir -p /var/jenkins/users/admin
mkdir -p /var/jenkins/jobs/WATT
ln -sf /vagrant/weber/jenkins-config.xml /var/jenkins/config.xml
ln -sf /vagrant/weber/jenkins-user.xml /var/jenkins/users/admin/config.xml
ln -sf /vagrant/weber/jenkins-job.xml /var/jenkins/jobs/WATT/config.xml
ln -sf /vagrant/weber/env.sh /etc/profile.d/weber.sh

echo "===Weber Package==="
pip3 install -r requirements.txt

# Ohm (Modelling)
echo "==Ohm=="
cd /vagrant/ohm
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
mkdir -p /var/jenkins/jobs/mutators
ln -sf /vagrant/ohm/jenkins-job.xml /var/jenkins/jobs/mutators/config.xml
