#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

port=$(ctx node properties port)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        ctx node attributes path = "/var/www/html"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
            apt update
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        apt -y install apache2

        if [ "$port" != "80" ]; then
            echo "Change apache listen port to: $port"
            sed -i "s/Listen 80/Listen $port/" /etc/apache2/ports.conf
            service apache2 restart
        fi
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac