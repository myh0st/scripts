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
from ftplib import FTP

urllib3.disable_warnings()


def verify(site):
    HOST, port = site.split("/")[2].split(":")
    try:
        ftp = FTP()
        ftp.connect(HOST, int(port), timeout=2)
        ftp.login()  # 匿名登录

        # 切换到指定目录并列出文件
        ftp.cwd("/")
        directory_contents = ftp.nlst()  # 获取目录内容列表
        ftp.quit()
        return directory_contents
    except:
        #print(sys.exc_info())
        pass
    return ""

    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，匿名获取目录的内容为：", info)
    else:
        print("[-]漏洞不存在")
