#!/bin/bash

set -e

hostname=$(ctx relationship target_node attributes hostname)

if [ "$hostname" != "" ]; then
   echo "Setting hostname -> $hostname"
   ctx relationship source_node attributes hostname = $hostname
fi