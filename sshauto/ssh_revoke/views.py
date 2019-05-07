# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import os
import paramiko


from django.http import JsonResponse
from sshauto.settings import BASE_DIR
import json
import subprocess
# Create your views here.

script_loc = os.path.join(BASE_DIR, 'ssh_revoke', 'revoke_user.sh')
user='ec2-user'
key='/Users/rivigo/.ssh/riv_devops.pem'

def bastion(username,ip):
    USERNAME=username
    host=ip
    print(host)
    print(USERNAME)
    try:
        cmd = script_loc + ' ' + USERNAME
        res=subprocess.call(cmd, shell=True)
        if res == 0:
                print("cmd run")
        else:
               print("error in cmd")
               raise Exception('This is the exception you expect to handle')
    except Exception as e:
          status={}
          status['error']= 'ERROR in User revoke'
          status['response'] = 'try post method'
          print(json.dumps(status))
          raise Exception('This is the exception you expect to handle')


def app_server(username,ip):
    USERNAME=username
    host=ip
    print(USERNAME)
    print(ip)
    try:
        cmd = 'deluser --remove-home' + ' ' + USERNAME
        print(cmd)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, key_filename=key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for i in stdout:
            print(i)
            if i == 0:
                print("error in cmd")
                raise Exception('This is the exception you expect to handle')
            else:
                print("done cmd")
    except Exception as e:

        status={}
        status['error']= 'ERROR in User revoke'
        status['response'] = 'try post method'
        print(json.dumps(status))
        raise Exception('This is the exception you expect to handle')

dict={'bastion':bastion,'app_server':app_server}

def ssh_revoke(request):
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
        status['error']= 'ERROR in User del'
        status['response'] = 'try post method'
        return HttpResponse(json.dumps(status))

    status['status'] = 'SUCCESS'
    status['response'] = 'User deleted'
    status['username'] = username
    return HttpResponse(json.dumps(status))

