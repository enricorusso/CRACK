#!/bin/bash

set -e


username=$(ctx node properties username)
password=$(ctx node properties password)
home=$(ctx node properties home)
groups=$(ctx -j node properties groups)

echo "Creating user $username"

if  id $username; then
    echo "User $username exists"
else
    echo "Creating user $username"
    # TODO: if a group with the same name exists it fails..
    if [ "$home" != "" ]; then
        useradd -d $home -m $username
    else
        useradd -m $username
        home=$(getent passwd $username | cut -d: -f6)
    fi
fi

if [ "$password" != "" ]; then
    echo "Setting $username password to $password"
    echo "$username:$password" | chpasswd
fi

if [ "$groups" != "" ] && [ "$groups" != "null" ]; then
    g=$(echo ${groups//[\[\]\",]})

    echo "groups: $g"
    usermod -G $g $username
fi

ctx node attributes username = $username
