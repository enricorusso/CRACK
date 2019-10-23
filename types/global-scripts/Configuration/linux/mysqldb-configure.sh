#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

password=$(ctx node attributes password)
dbname=$(ctx node properties dbname)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        #if [ "$password" != "" ]; then
        until service mysql status 2>&1>/dev/null; do echo "Waiting MySQL...."; sleep 1; done
        mysqladmin -u root -p$password create $dbname
        # else
        #     echo "Ooops! Password is empty :("
        #fi
        
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac
