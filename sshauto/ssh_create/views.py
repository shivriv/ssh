# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import os
from django.http import JsonResponse
from sshauto.settings import BASE_DIR
import json
import paramiko
import subprocess
# Create your views here.
script_loc = os.path.join(BASE_DIR, 'ssh_create', 'create_user.sh')
user='ec2-user'
key='/Users/rivigo/.ssh/riv_devops.pem'

def bastion(username,ip):
    USERNAME=username
    host=ip
    print(host)
    print(USERNAME)
    try:
        status={}
        cmd = script_loc + ' ' + USERNAME
        res=subprocess.call(cmd, shell=True)
        status['respone']= res
        status['status']= 'error'
        if res == 0:
                print("cmd run")
        else:
               print("error in cmd")
               return HttpResponse(json.dumps(status))
    except Exception as e:

        status={}
        status['error']= 'ERROR in User creation'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    status = {}
    status['response'] = 'bastion'
    status['value'] = username
    print(json.dumps(status))

def app_server(username,ip):
    USERNAME = username
    host = ip
    print(USERNAME)
    print(ip)
    try:
        cmd1 = 'adduser' + ' ' + USERNAME
        cmd2 = 'scp /home/' + '' + USERNAME + '/.ssh/id_rsa.pub' + ' ' + 'ec2@' + '' + ip + '' + ':/home/' + '' + USERNAME + '' + '/.ssh/auth.key'
        print(cmd1)
        print(cmd2)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, key_filename=key)
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        for i in stdout:
            print(i)
            if i == 0:
                print("error in cmd")
            else:
                print("done cmd1")
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        for i in stdout:
            print(i)
            if i == 0:
                print("error in cmd")
            else:
                print("done cmd2")


    except Exception as e:

        status={}
        status['error']= 'ERROR in User creation'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    status = {}
    status['response'] = 'app_server'
    status['value'] = username
    print(json.dumps(status))

dict={'bastion':bastion,'app_server':app_server}

def ssh_create(request):
    status = {}
    if request.method != 'POST':
        status['status'] = 'error'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    try:
        data = json.loads(request.body)
        print(request.body)
        username = data["username"]
        server_type = data["server_type"]
        ip = data["ip"]

    except Exception as e:
        status = {}
        status['error'] = 'ERROR provide all field'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    try:
        dict[server_type](username,ip)

    except Exception as e:

        status={}
        status['error']= 'ERROR in User creation'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    status['status'] = 'SUCCESS'
    status['response'] = 'User created'
    status['username'] = username
    return HttpResponse(json.dumps(status))

