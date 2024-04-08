#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import pymysql


def verify(siteinfo):
    hostinfo, passinfo = siteinfo.split("/")[2].split("@")
    host, port = hostinfo.split(":")
    user, password = passinfo.split(":")
    conn = pymysql.connect(host=host, port=int(port), user=user,password=password,database="mysql",charset="utf8", connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("show databases;")
        return cur.fetchall()

    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询服务器所有数据库名称为：", info)
    else:
        print("[-]漏洞不存在")
