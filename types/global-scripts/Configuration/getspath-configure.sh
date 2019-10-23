#!/bin/bash

set -e

path=$(ctx relationship target_node attributes path)

if [ "$path" != "" ]; then
   echo "Setting path -> $path"
   ctx relationship source_node attributes path = $path
fi