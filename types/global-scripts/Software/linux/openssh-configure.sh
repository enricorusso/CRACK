#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

permitrootlogin=$(ctx node properties PermitRootLogin)
permitpassword=$(ctx node properties PasswordAuthentication)

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        # augeas
        if [ ! $(which augtool) ]; then
            while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

            if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
                apt update
            fi

            while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

            apt -y install augeas-tools
        fi

        augtool set /files/etc/ssh/sshd_config/PermitRootLogin $permitrootlogin
        augtool set /files/etc/ssh/sshd_config/PasswordAuthentication $permitpassword

        # remove history ;)
        rm -rf /root/.augeas/

        service sshd restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac