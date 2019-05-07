#!/bin/bash
echo "we are deleting user"
deluser --remove-home ${1}
if [ $? -eq 0 ]
then
    echo "User deleted"
fi

