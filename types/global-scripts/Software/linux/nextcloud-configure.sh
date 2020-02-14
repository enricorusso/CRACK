#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release
path=$(ctx node attributes path)

dbuser=$(ctx node properties db_username)
dbpass=$(ctx node properties db_password)
dbhost=$(ctx node properties db_host)
dbname=$(ctx node properties db_name)

admin_user=$(ctx node properties admin_user)
admin_password=$(ctx node properties admin_password)

ctx download-resource /tmp/nextcloud.conf global-scripts/Artifacts/nextcloud.conf

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

        apt -y install php-xml php-intl php-mbstring php-xmlrpc php-soap php-gd php-xml php-json php-imagick php-mysql php-mcrypt php-zip php-curl php-redis php-memcached

        #fi

        test -f /etc/nginx/sites-enabled/default && sed -i '/^#/!s/location \/ {/location \/ {\nrewrite ^ \/index.php;\n/g' /etc/nginx/sites-enabled/default
        test -f /etc/nginx/sites-enabled/default &&  mv /tmp/nextcloud.conf /etc/nginx/nextcloud.conf
        test -f /etc/nginx/sites-enabled/default && sed -i '/^#/!s/server {/server {\ninclude nextcloud.conf;\n/g' /etc/nginx/sites-enabled/default

        service php7.0-fpm restart
        test -f /etc/nginx/sites-enabled/default && service nginx restart

        cd $path
        curl -O https://download.nextcloud.com/server/releases/latest-14.tar.bz2
        tar xvfj latest-14.tar.bz2 --strip 1
        rm -f latest-14.tar.bz2

        echo "
<?php
\$CONFIG = array (
  'passwordsalt' => 'ILpmiy15d+fCRNA0QWTxnUysvs2qiJ',
  'secret' => 'QOPiRbdFFEHcPoAeRziFhtQ5WFvLuxf40Xs2A+3Td2MeQhWW',
  'trusted_domains' => 
  array (
    0 => '*',
  ),
  'datadirectory' => '$path/data',
  'dbtype' => 'mysql',
  'version' => '14.0.14.1',
  'overwrite.cli.url' => 'http://localhost',
  'dbname' => '$dbname',
  'dbhost' => '$dbhost',
  'dbport' => '',
  'dbtableprefix' => 'oc_',
  'mysql.utf8mb4' => true,
  'dbuser' => '$dbuser',
  'dbpassword' => '$dbpass',
  'instanceid' => 'och6cjb01ag0',
);        
        " > $path/config/config.php
        #mkdir /var/www/data
        chown -R www-data.www-data /var/www/html
        sudo -u www-data php occ  maintenance:install --database "mysql" --database-name "$dbname"  --database-user "$dbuser" --database-pass "$dbpass" --database-host="$dbhost" --admin-user "$admin_user" --admin-pass "$admin_password"
        sed -i '/^#/!s/localhost/*/g' /var/www/html/config/config.php
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac