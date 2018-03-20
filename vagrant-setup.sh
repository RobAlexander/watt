#!/bin/bash

ROOTPATH=$WATT_ROOT
SETUPPATH=$ROOTPATH/vagrant-setup
PACKAGEINSTALLER=$SETUPPATH/packages.sh

# Start by updating the box
echo "=Ubuntu="
$SETUPPATH/machine.sh

# Run when provisioning a new vagrant box to setup and install the required software
echo "=watt="

# Ampere (Mutation)
echo "==Ampere=="
cd $WATT_ROOT/ampere
$PACKAGEINSTALLER nodejs

# Volt (Run testers)
echo "==Volt=="
cd $WATT_ROOT/volt
$PACKAGEINSTALLER phantomjs nodejs

# Tesla (Analyse results)
echo "==Tesla=="
cd $WATT_ROOT/tesla
$PACKAGEINSTALLER python3

# Weber (UI and Automation)
echo "==Weber=="
cd $WATT_ROOT/weber
$PACKAGEINSTALLER forever jenkins python3
echo "===Customise Jenkins==="
mkdir -p $JENKINS_HOME/users/admin
mkdir -p $JENKINS_HOME/jobs/WATT
mkdir -p $JENKINS_HOME/jobs/export
ln -sf $WATT_ROOT/weber/jenkins-config.xml $JENKINS_HOME/config.xml
ln -sf $WATT_ROOT/weber/jenkins-user.xml $JENKINS_HOME/users/admin/config.xml
ln -sf $WATT_ROOT/weber/jenkins-job.xml $JENKINS_HOME/jobs/WATT/config.xml
ln -sf $WATT_ROOT/weber/jenkins-export.xml $JENKINS_HOME/jobs/export/config.xml

# Ohm (Modelling)
echo "==Ohm=="
cd $WATT_ROOT/ohm
$PACKAGEINSTALLER epsilon ant
echo "===Customise Jenkins==="
mkdir -p $JENKINS_HOME/jobs/mutators
ln -sf $WATT_ROOT/ohm/jenkins-job.xml $JENKINS_HOME/jobs/mutators/config.xml
