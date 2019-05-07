#!/bin/bash
echo "we are adding user"
echo ${1}
echo "creating user if not in server"
/usr/bin/id ${1} 2>/dev/null
if [ $? -eq 0 ]
then
    echo "User already present"
else
     useradd -c "new user" -m -s /bin/bash ${1}
     mkdir /home/$1/.ssh/
     chown -R ${1}:${1} /home/$1/.ssh/
     ssh-keygen -f /home/$1/.ssh/id_rsa -t rsa -N '' -q
     chown -R ${1}:${1} /home/$1/.ssh/
     echo "user created"
fi
