#!/bin/bash

set -e

password=$(ctx relationship target_node properties password)

if [ "$password" != "" ]; then
   echo "Setting password -> $password"
   ctx relationship source_node attributes password = $password
fi