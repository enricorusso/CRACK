#!/bin/bash

set -e

ID="unknown"
test -f /etc/os-release && source /etc/os-release

ctx download-resource /tmp/sample-zone global-scripts/Artifacts/sample-zone

name=$(ctx node attributes hostname)
ip_address=$(ctx node attributes address)
domain_name=$(ctx node properties name)
records=$(ctx -j node properties records)
forwarders=$(ctx -j node properties forwarders)

echo "records: $records"
echo "forwarders: $forwarders"

echo -n "Distro: "
case $ID in
    ubuntu|debian)
        echo "ubuntu/debian"

        if [ "$forwarders" != "" ] && [ "$forwarders" != "null" ]; then
            echo "===> Forward zone ${domain_name}"

            forwarders=$(echo ${forwarders//[\[\]\"]} | tr ',' ';')
            echo "zone ${domain_name} {type forward; forward only; forwarders { ${forwarders}; }; };" >> /etc/bind/named.conf.local

            systemctl restart bind9
        else
            if ! z=$(host -avl ${domain_name}); then
               echo "===> Add zone ${domain_name}"

               cat /tmp/sample-zone | hostname=${name} domain=${domain_name} ip=${ip_address} envsubst '$hostname $domain $ip' > /var/cache/bind/${domain_name}
               rndc addzone ${domain_name} "{type master; file \"${domain_name}\"; allow-update {key \"rndc-key\";};};"
            else
               echo "===> Using existing zone ${domain_name}"
            fi
        fi

        systemctl restart bind9

        sleep 5

        until service bind9 status 2>&1>/dev/null; do echo "Waiting BIND...."; sleep 1; done

        if [ "$forwarders" == "" ] || [ "$forwarders" == "null" ]; then
            echo $records
            if [ "$records" != "" ]; then
r=$(echo $records | python -c "$(cat << 'EOF'
import sys, json; 

for i in json.load(sys.stdin):
 print ("update add %s %s IN %s %s," % (i['name'], i['ttl'], i['type'], i['value']))
EOF
)")
            fi

            # set +e

            IFS=,
            echo $r | 
            while read a
            do
            
                h=$(echo $a | cut -d' ' -f 1-3)
                k=$(echo $a | cut -d' ' -f 4-)

                echo "${h}.${domain_name} ${k}"

                echo "server 127.0.0.1
                zone ${domain_name}
                ${h}.${domain_name} ${k}
                send
                quit
                " | nsupdate -d -k /etc/bind/rndc.key         
            done
        fi
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac