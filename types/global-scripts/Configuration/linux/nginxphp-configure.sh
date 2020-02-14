#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

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

        while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        apt -y install php-fpm php-pgsql php-mysql php-curl php-gd

        sed -i 's/index.html /index.html index.php /g' /etc/nginx/sites-enabled/default
        sed -i 's/^server {/server {\nlocation ~ \.php$ {\n fastcgi_pass unix:\/var\/run\/php\/php7.0-fpm.sock;\n include snippets\/fastcgi-php.conf;\n}/g' /etc/nginx/sites-enabled/default
		
        service nginx restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac