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

        apt -y install bind9

                echo "
include \"/etc/bind/rndc.key\";

controls {
        inet 127.0.0.1 port 953 allow { localhost; } keys { "rndc-key"; };
};
" >> /etc/bind/named.conf

        echo "Configuring named options"

    #    if [ "${forwarder}" != "" ]; then
        if [ "$forwarders" != "" ] && [ "$forwarders" != "null" ]; then
            sed -i "/^};/i forwarders { ${forwarder}; };" /etc/bind/named.conf.options
        fi
        sed -i "/^};/i allow-new-zones yes;" /etc/bind/named.conf.options

        systemctl restart bind9
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac