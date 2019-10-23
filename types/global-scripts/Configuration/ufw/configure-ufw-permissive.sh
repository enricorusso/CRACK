#!/bin/bash

set -e

masquerade_addresses=$(ctx -j node properties masquerade_addresses)
routes=$(ctx -j node properties routes)

echo $masquerade_addresses
echo $routes

if [ "$routes" != "" ] && [ "$routes" != "null" ]; then

r=$(echo $routes | python -c "$(cat << 'EOF'
import sys, json; 

for i in json.load(sys.stdin):
 print ("ip route add %s via %s," % (i.items()[0][1], i.items()[1][1]))
EOF
)")

IFS=,
echo $r | 
while read a
do
 echo $a
 sed -i "\$i $a" /etc/rc.local
 eval $a
done

fi

if [ "$masquerade_addresses" != "" ] && [ "$masquerade_addresses" != "null" ]; then

sed -i "/^COMMIT/a *nat\n:POSTROUTING ACCEPT [0:0]\n# nat rules\nCOMMIT" /etc/ufw/before.rules

m=$(echo $masquerade_addresses | python -c "$(cat << 'EOF'
import sys, json;

for i in json.load(sys.stdin):
 print ("%s," % (i))
EOF
)")

IFS=,
echo $m |
while read e
do
 echo "$e"
 in=$(ip a | grep ${e// } | cut -d' ' -f 11)
 sed -i "/^# nat rules/a -A POSTROUTING -o $in -j MASQUERADE" /etc/ufw/before.rules
done

fi

# default allow
ufw default allow outgoing
ufw default allow incoming
ufw default allow forward
        
ufw --force enable