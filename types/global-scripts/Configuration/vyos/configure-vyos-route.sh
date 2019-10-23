#!/bin/vbash
source /opt/vyatta/etc/functions/script-template

destination=$(ctx node properties destination)
address=$(ctx node properties address)

echo "route: $destination -> $address"

configure 

if [ "$destination" != "" ] && [ "$destination" != "null" ] &&  [ "$address" != "" ] && [ "$address" != "null" ]; then
    set protocols static route $destination next-hop $address
fi

commit
save