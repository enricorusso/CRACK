#!/bin/bash

# set -e

props=$(ctx -j relationship properties props)

if [ "$props" != "" ]; then
   props=$(echo ${props//[\[\]\"]})

   for p in `echo ${props//[\[\]\"]} | tr ',' '\n' | tr -d ' '`
   do

    if v=$(ctx relationship target_node attributes $p) ; then
       echo "Setting attribue $p -> $v (from attribute)"
    else
       v=$(ctx relationship target_node properties $p)
       echo "Setting attribue $p -> $v (from property)"
    fi

    ctx relationship source_node attributes $p = $v
   done
fi