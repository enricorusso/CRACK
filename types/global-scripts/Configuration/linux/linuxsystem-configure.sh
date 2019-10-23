#!/bin/bash

set -e

hostname=$(ctx node properties hostname)
domain=$(ctx node properties domain)
dns=$(ctx -j node properties dns)

ID="unknown"
test -f /etc/os-release && source /etc/os-release

echo -n "Distro: "
case $ID in
    ubuntu|debian|kali)
        echo "ubuntu/debian"

        if [ "$proxy_url" != "" ]; then
            echo "Proxy: $proxy_url"
            export http_proxy="$proxy_url"
            export https_proxy="$proxy_url"
        fi

        echo dns: $dns
        echo hostname: $hostname
        echo domain: $domain

        # while fuser /var/{lib/{dpkg,apt/lists},cache/apt/archives}/lock >/dev/null 2>&1; do echo "dpkg database is locked."; sleep 10; done

        # if [ $(stat -c %y /var/lib/apt/periodic/update-success-stamp | cut -d' ' -f 1) != $(date +%Y-%m-%d) ]; then
        #     apt update
        # fi

        if [ "$dns" != "" ] && [ "$dns" != "null" ]; then

            d=$(echo ${dns//[\[\]\",]})

            echo $d, $n

            n=$(grep -n -m1 address /etc/network/interfaces | cut -d: -f 1)
            if [ "$domain" != "" ] && [ "$domain" != "null" ]; then
                sed -i "${n}i\ dns-nameservers ${d}\n dns-search $domain" /etc/network/interfaces
            else
                sed -i "${n}i\ dns-nameservers ${d}" /etc/network/interfaces
            fi

            if [ "$ID" == "kali" ]; then
                mv /etc/resolv.conf /etc/resolv.conf.orig
                echo "nameserver $d" >> /etc/resolv.conf 
                echo "domain $domain" >> /etc/resolv.conf
            fi
        fi

        if [ "$hostname" != "" ] && [ "$hostname" != "null" ]; then
            mv /etc/hostname /etc/hostname.orig
            echo $hostname > /etc/hostname
            hostnamectl set-hostname $hostname
        fi

        echo $(hostname -I | cut -d\  -f1) $(hostname) | sudo tee -a /etc/hosts
        sudo service networking restart
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac