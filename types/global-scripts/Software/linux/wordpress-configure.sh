#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

path=$(ctx node attributes path)

dbuser=$(ctx node properties db_username)
dbpass=$(ctx node properties db_password)
dbhost=$(ctx node properties db_host)
dbname=$(ctx node properties db_name)

url=$(ctx node properties url)
title=$(ctx node properties title)

admin_user=$(ctx node properties admin_user)
admin_password=$(ctx node properties admin_password)
admin_email=$(ctx node properties admin_email)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        # php-cli
        # if [ ! $(which php) ]; then
        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
            apt update
        fi

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        apt -y install php-mysql php php-curl mysql-client
        #fi

        cd /usr/local/bin
        curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
        chmod +x wp-cli.phar 
        mv wp-cli.phar /usr/local/bin/wp

        cd $path

        test -f index.html && mv index.html index.html.old

        wp core download --allow-root
        wp config create --dbname=$dbname --dbuser=$dbuser --dbpass=$dbpass --dbhost=$dbhost --allow-root
        #wp db create --allow-root
        wp core install --allow-root --url=$url --title=$title --admin_user=$admin_user --admin_password=$admin_password --admin_email=$admin_email
        wp post update 1 --post_title="Welcome to $title !" --post_content="Security is monkey business &#x1F435;" --allow-root
        chown www-data.www-data wp-config.php
        chmod 440 wp-config.php
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac