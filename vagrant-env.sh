export WATT_ROOT=/vagrant
if [ -e /report ]
then
    export REPORT_ROOT=/report
fi
source $WATT_ROOT/weber/env.sh
