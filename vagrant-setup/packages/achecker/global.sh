#!/bin/bash

function achecker_http ()
{
    curl -d "$1" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:9080/AChecker/install/install.php
}

achecker_root=/var/www/AChecker
achecker_var=/var/achecker
achecker_temp=$achecker_var/temp

if [ -e $achecker_root/index.php ]
then
    echo "AChecker already installed"
else
    mkdir -p $achecker_var
    wget https://github.com/inclusive-design/AChecker/archive/master.zip -O $achecker_var/achecker.zip
    unzip -o $achecker_var/achecker.zip -d $achecker_var
    mkdir -p $achecker_root
    mv -f $achecker_var/AChecker-master/* $achecker_root

    currentpath="$( cd "$(dirname "$0")" ; pwd -P )"
    cp $currentpath/config.inc.php $achecker_root/include/config.inc.php

    mkdir -p $achecker_temp
    chmod a+rwx $achecker_temp
    chmod a+rw $achecker_root/include/config.inc.php

    achecker_http "new_version=1.3&next=++Install++"
    achecker_http "action=process&step=1&new_version=1.3&submit=I+Agree"
    achecker_http "action=process&step=2&new_version=1.3&db_host=localhost&db_port=3306&db_login=root&db_password=qwerty&db_name=achecker&tb_prefix=AC_&submit=Next+%BB+"
    achecker_http "step=3&step2%5Bnew_version%5D=1.3&step2%5Bdb_host%5D=localhost&step2%5Bdb_port%5D=3306&step2%5Bdb_login%5D=root&step2%5Bdb_password%5D=qwerty&step2%5Bdb_name%5D=achecker&step2%5Btb_prefix%5D=AC_&submit=Next+%BB+"
    achecker_http "action=process&form_admin_password_hidden=d033e22ae348aeb5660fc2140aec35850c4da997&form_account_password_hidden=&step=3&step2%5Bnew_version%5D=1.3&step2%5Bdb_host%5D=localhost&step2%5Bdb_port%5D=3306&step2%5Bdb_login%5D=root&step2%5Bdb_password%5D=qwerty&step2%5Bdb_name%5D=achecker&step2%5Btb_prefix%5D=AC_&smtp=false&admin_username=admin&admin_password=&admin_email=admin%40admin.local&site_name=Web+Accessibility+Checker&email=admin%40admin.local&submit=+Next+%BB"
    achecker_http "step=4&copy_from=&get_file=TRUE&step2%5Bnew_version%5D=1.3&step2%5Bdb_host%5D=localhost&step2%5Bdb_port%5D=3306&step2%5Bdb_login%5D=root&step2%5Bdb_password%5D=qwerty&step2%5Bdb_name%5D=achecker&step2%5Btb_prefix%5D=AC_&step3%5Bform_account_password_hidden%5D=&step3%5Bsmtp%5D=false&step3%5Badmin_password%5D=&content_dir=%2Fvar%2Fachecker%2Ftemp&submit=+Next+%BB"
    achecker_http "action=process&step=5&step2%5Bnew_version%5D=1.3&step2%5Bdb_host%5D=localhost&step2%5Bdb_port%5D=3306&step2%5Bdb_login%5D=root&step2%5Bdb_password%5D=qwerty&step2%5Bdb_name%5D=achecker&step2%5Btb_prefix%5D=AC_&step3%5Bform_account_password_hidden%5D=&step3%5Bsmtp%5D=false&step3%5Badmin_password%5D=&step4%5Bcopy_from%5D=&step4%5Bget_file%5D=TRUE&step4%5Bcontent_dir%5D=%252Fvar%252Fachecker%252Ftemp%252F&submit=+Next+%BB+"

    mysql -u root -pqwerty -B --disable-column-names -e "SELECT web_service_id FROM achecker.AC_users WHERE login=\"admin\"" > $WATT_ROOT/acheckerid
fi
