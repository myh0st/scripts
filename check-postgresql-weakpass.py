#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import psycopg2


def verify(siteinfo):
    hostinfo, passinfo = siteinfo.split("/")[2].split("@")
    host, port = hostinfo.split(":")
    user, password = passinfo.split(":")
    conn = psycopg2.connect(database="postgres", user=user, 
                        password=password, host=host, 
                        port=port)
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        return cur.fetchall()

    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，查询服务器信息为：", info)
    else:
        print("[-]漏洞不存在")
