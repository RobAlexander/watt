#!/bin/bash

if command -v php-cli 2>&1 1>/dev/null
then
    echo "php already installed"
else
    apt-get install -y php5 libapache2-mod-php5 php5-mcrypt php5-cli php5-mysql
    systemctl restart apache2
fi
