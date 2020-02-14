#!/bin/vbash
source /opt/vyatta/etc/functions/script-template

configure
set nat source rule 100 outbound-interface eth1 
set nat source rule 100 translation address masquerade 

# TODO: not supported, consider ip_allocation: none

# set service dhcp-server shared-network-name dhcp1 authoritative enable
# set service dhcp-server shared-network-name dhcp1 subnet 27.8.0.0/16 default-router 27.8.0.1
# set service dhcp-server shared-network-name dhcp1 subnet 27.8.0.0/16 lease 3600
# set service dhcp-server shared-network-name dhcp1 subnet 27.8.0.0/16 start 27.8.16.100 stop 27.8.17.100

# set protocol static route 198.51.100.0/24 next-hop $dest1

declare -i i
i=1
r="start"
while [ $i -le 20 -a "$r" != "" ]
do
 varname1="net$i"
 varname2="dest$i"
 r="${!varname1}"
 d="${!varname2}"
 if [ "$r" != "" -a "$d" != "" ]; then
     echo -n "$i "
     echo set protocols static route $r next-hop $d
     set protocols static route $r next-hop $d
 fi

 i=$i+1
done

commit
save
exit