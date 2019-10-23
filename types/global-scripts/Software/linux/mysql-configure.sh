#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

password=$(ctx node properties password)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
            apt update
        fi

        debconf-set-selections <<< "mysql-server mysql-server/root_password password $password"
        debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $password"

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        apt -y install mysql-server

        # set UTF8 support
        echo "
[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
        " > /etc/mysql/mysql.conf.d/utf8.cnf

        service mysql restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac