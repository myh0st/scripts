#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
from pymongo import MongoClient


def verify(site):
    ip = site.split("/")[2].split(":")[0]
    try:
        client = MongoClient(ip,27017,connectTimeoutMS=1000,socketTimeoutMS=1000,waitQueueTimeoutMS=1000)
        try:
            serverInfo = client.server_info()
        except:
            pass
        client.close()
        return serverInfo
    except:
        pass

    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询服务器信息为：", info)
    else:
        print("[-]漏洞不存在")
