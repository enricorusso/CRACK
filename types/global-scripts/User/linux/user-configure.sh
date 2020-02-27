#!/bin/bash

set -e


username=$(ctx node properties username)
password=$(ctx node properties password)
home=$(ctx node properties home)
groups=$(ctx -j node properties groups)

echo "Creating user $username"

ID="unknown"
test -f /etc/os-release && source /etc/os-release

echo -n "Distro: "
case $ID in
    alpine)
        if  id $username; then
            echo "User $username exists"
        else
            echo "Creating user $username"
            # TODO: if a group with the same name exists it fails..
            if [ "$home" != "" ]; then
                adduser -h $home $username -D
            else
                adduser $username -D
                home=$( getent passwd $username | cut -d: -f6)
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
        ;;
    ubuntu|debian|kali)
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
        ;;
    *)
        echo "distro $ID not supported :("
        ;;
esac