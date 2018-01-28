#!/bin/bash

SETUPPATH="$( cd "$(dirname "$0")" ; pwd -P )"

PACKAGESPATH=$SETUPPATH/packages

for package in "$@"
do
    if [ -d $PACKAGESPATH/$package ]
    then
        if [ -e $PACKAGESPATH/$package/require ]
        then
            while read req
            do
                $0 $req
            done <$PACKAGESPATH/$package/require
        fi

        echo "Installing $package"

        if [ -e $PACKAGESPATH/$package/global.sh ]
        then
            $PACKAGESPATH/$package/global.sh
        fi

        if [ -e $PACKAGESPATH/$package/local.sh ]
        then
            $PACKAGESPATH/$package/local.sh
        fi

        echo "Successfully installed $package"
    else
        echo "Package $package could not be found"
        exit 1
    fi
done
