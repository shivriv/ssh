create virtualenv with python-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r req.txt
pip install paramiko
python manage.py runserver 0.0.0.0:8080
http://192.168.56.105:8080/
http://192.168.56.105:8080/ssh_revoke
http://192.168.56.105:8080/ssh_create
create ,revoke user access  in bastion server and app_server

http://192.168.56.105:8080/ssh_create
data need to be passed
{"username":"tfs378",
"server_type":"bastion",
"ip":"192.168.56.105"
}

http://192.168.56.105:8080/ssh_create
data need to be passed
{"username":"tfs378",
"server_type":"app_server",
"ip":"192.168.56.106"
}
copy public key from bastion to app server in auth and create user before that


http://192.168.56.105:8080/ssh_revoke

{"username":"tfs378",
"server_type":"bastion",
"ip":"192.168.56.105"
}


http://192.168.56.105:8080/ssh_revoke

{"username":"tfs378",
"server_type":"app_server",
"ip":"192.168.56.105"
}
