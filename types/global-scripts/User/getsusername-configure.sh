#!/bin/bash

set -e

duser=$(ctx relationship target_node attributes username)
dattr=$(ctx relationship name)

if [ "$duser" != "" ]; then
   echo "Setting $dattr -> $duser"
   ctx relationship source_node attributes $dattr = $duser
fi