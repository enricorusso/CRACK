#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

port=$(ctx node properties port)

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

        apt -y install unzip libnet-ssleay-perl libauthen-pam-perl libauthen-pam-perl libauthen-pam-perl libio-pty-perl apt-show-versions libapt-pkg-perl

        cd /tmp

        # curl -O https://netcologne.dl.sourceforge.net/project/webadmin/webmin/1.941/webmin_1.941_all.deb
        wget https://sourceforge.net/projects/webadmin/files/webmin/1.941/webmin_1.941_all.deb/download -O webmin_1.941_all.deb

        dpkg -i webmin_1.941_all.deb

        rm webmin_1.941_all.deb
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac