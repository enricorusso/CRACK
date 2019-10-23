#!/bin/vbash
source /opt/vyatta/etc/functions/script-template

masquerade_addresses=$(ctx -j node properties masquerade_addresses)
routes=$(ctx -j node properties routes)

echo $masquerade_addresses
echo $routes

configure 

if [ "$routes" != "" ] && [ "$routes" != "null" ]; then

r=$(echo $routes | python -c "$(cat << 'EOF'
import sys, json; 

for i in json.load(sys.stdin):
 print ("set protocols static route %s next-hop %s," % (i.items()[0][1], i.items()[1][1]))
EOF
)")

IFS=,
echo $r | 
while read a
do
 echo $a
 eval $a
done

fi

echo "masquerade: $masquerade_addresses"

if [ "$masquerade_addresses" != "" ] && [ "$masquerade_addresses" != "null" ]; then

m=$(echo $masquerade_addresses | python -c "$(cat << 'EOF'
import sys, json;

for i in json.load(sys.stdin):
 print ("%s," % (i))
EOF
)")

declare -i rn
rn=100
IFS=,
echo $m |
while read e
do
 echo "$rn $e"
 in=$(ip a | grep ${e// } | cut -d' ' -f 11)
 set nat source rule $rn outbound-interface $in
 set nat source rule $rn translation address masquerade
 echo set nat source rule $rn outbound-interface $in
 echo set nat source rule $rn translation address masquerade
 rn=$rn+1
done

fi

commit
save