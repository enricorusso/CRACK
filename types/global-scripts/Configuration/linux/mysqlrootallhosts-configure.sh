#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

password=$(ctx node attributes password)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        if [ "$password" != "" ]; then
            mysql -u root -p$password -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '$password';"
        else
            echo "Ooops! Password is empty :("
        fi
        
        sed -i "s/^bind-address/bind-address = * #/g" /etc/mysql/mysql.conf.d/mysqld.cnf

        service mysql restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac