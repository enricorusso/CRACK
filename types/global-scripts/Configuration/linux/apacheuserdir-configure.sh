#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

username=$(ctx node attributes user)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        a2enmod userdir
        path=$(eval echo ~${username}/public-html) 
        mkdir $path  
        chown $username $path 

        ctx node attributes path = $path

        apache2ctl restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac