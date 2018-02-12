@ECHO OFF
SETLOCAL

echo WATT
:: Set variable for if there are errors
SET reqmiss=0

:: Check if vagrant is installed
where vagrant
IF %ERRORLEVEL% NEQ 0 CALL novagrant

:: Check if virtualbox is installed
IF NOT EXIST "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" CALL novbox

:: Handle missing requirements
IF %reqmiss% NEQ 0 GOTO reqnm

:: Bring up the box
vagrant up
IF %ERRORLEVEL% NEQ 0 GOTO vmerr

:: Launch the UI
start "" http://localhost:8080/
exit /B 0

:reqnm
echo Your system does not meet the requirements to run WATT
exit /B 1

:vmerr
echo WATT has not provisioned correctly and will be reset
vagrant destroy -f
exit /B 2

:: Functions
:novagrant
SET reqmiss=1
echo Vagrant is required to run WATT
echo Please visit https://www.vagrantup.com/downloads.html to obtain
EXIT /B 1

:novbox
SET reqmiss=1
echo VirtualBox is required to run WATT
echo Please visit https://www.virtualbox.org/wiki/Downloads to obtain
EXIT /B 1
