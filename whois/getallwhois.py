#!/usr/bin/python 2.79
#-*- coding:utf-8 -*-

import re
import os
import sys
import time
import socket
import struct

globalitems = []
configdrct = {}

def getItems(a):
    items = []
    if int(a) > 96:
        sys.exit()
    obj = open("log.txt", 'r')
    for item in obj:
        if re.search("^"+a+"\.", item):
            items.append(item.strip())
    obj.close()
    return items

def getLogIpRange(ip):
    patt = "^"+ip.replace(".","\.")
    for item in globalitems:
        if re.search(patt, item):
            return item.strip()
    return False

def getData(ip, whoserver):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.connect((whoserver, 43))
    s.send(ip+" \r\n")
    data = ""
    while True:
         temp = s.recv(1024)
         if temp == "" or temp == None:
             break
         data = data + temp
    s.close()
    return data

def getWhois(ip):
    whoserver = getWhoSrv(ip)
    data = getData(ip, whoserver)
    #print data
    #sys.exit()
    if re.search("(NetRange|inetnum):\s+(\d+\.\d+.\d+\.\d+\s+-\s+\d+\.\d+.\d+\.\d+)", data):
        return data
    elif re.search("denied", data):
        time.sleep(300)
        data = getWhois(ip)
        return data
    elif re.search("No match", data):
        nextip = getcExtIp(ip)
        #print data
        data = getWhois(nextip) 
        return data
    else:
        time.sleep(200)
        data = getWhois(ip)
        return data
  
def getcExtIp(ip):
    a1,a2,a3,a4 = ip.split('.')
    if int(a3)+1 > 255 and int(a2) < 255:
        return a1+"."+str(int(a2)+1)+'.0.0'
    elif int(a2)+1 > 255:
        globalitems = getItems(str(int(a1)+1))
        #print globalitems
        return str(int(a1)+1)+".0.0.0"
    temp = a1+'.'+a2+"."+str(int(a3)+1)+'.0'
    return temp
    
def getbExtIp(ip):
    a1,a2,a3,a4 = ip.split('.')
    if int(a2)+1 > 255:
        globalitems = getItems(str(int(a1)+1))
        return str(int(a1)+1)+".0.0.0"
    temp = a1+'.'+str(int(a2)+1)+".0.0"
    return temp
    
def initConfig():
    for item in open("config.cnf"):
        key, value = item.strip().split("\t")
        configdrct[key] = value
    
def getWhoSrv(ip):
    key = ip.split(".")[0]
    return configdrct[key]
    
def readWhois():
    return codecs.open("3.txt", 'r', 'utf-8').read()
    
def writeWhois(filename, data):
    obj = open(filename, 'w')
    obj.write(data)
    obj.close()
    
def createForder():
    if not os.path.exists("logs"):
        os.mkdir("logs")
    
def ipToInt(ip):
    return socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip.replace(" ", ""))))[0])
    
def intToIp(num):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(num)))
    
def getIpRange(data):
    patt_iprange = "(NetRange|inetnum):\s+(\d+\.\d+.\d+\.\d+\s+-\s+\d+\.\d+.\d+\.\d+)"
    if re.search(patt_iprange, data):
        ipranges = re.findall(patt_iprange, data)
        #print re.findall(patt_iprange, data)
        if len(ipranges) == 1:
            return ipranges[0][1]
        else:
    	    return getSmallIpRange(ipranges)
    else:
        return False
    
def getIpRangeDiffer(iprange):
    startIpStr, endIpStr = iprange.split('-')
    startIpNum = ipToInt(startIpStr)
    endIpNum = ipToInt(endIpStr)
    differ = endIpNum - startIpNum
    return differ
    	
def getSmallIpRange(ipranges):
    differ = 0
    temp_iprange = ""
    for iprange in ipranges:
        if differ == 0:
            differ = getIpRangeDiffer(iprange[1])
            temp_iprange = iprange[1]
        else:
            temp_differ = getIpRangeDiffer(iprange[1])
            if differ > temp_differ:
                temp_iprange = iprange[1]
                differ = temp_differ
    return temp_iprange
	    	
def getNextIp(oldip, iprange):
    endIpStr = iprange.split('-')[1]
    if re.search("\d{1,3}\.\d{1,3}\.0\.0 \- \d{1,3}\.\d{1,3}\.255\.255", iprange):
        return getbExtIp(oldip)
    endIpNum = ipToInt(endIpStr)
    nextIpNum = endIpNum + 1
    nextIp = intToIp(nextIpNum)
    return nextIp

def judge(ip):
    iprange = getLogIpRange(ip)
    #print iprange
    #sys.exit()
    nextip = ip
    while True:
        if not iprange:
            return nextip
        else:
            nextip = getNextIp(ip)
            iprange = getLogIpRange(nextip)
    
def handle(ip):
    nextip = ip
    while True:
        try:
            whoisData = getWhois(nextip)
        except:
            time.sleep(5)
            continue
        iprange = getIpRange(whoisData)
        if iprange:
            writeWhois("logs/" + iprange, whoisData)
            nextip = getNextIp(nextip, iprange)
        else:
             time.sleep(5)
             continue            
            
def handle2(ip):
    globalitems = getItems(ip.split(".")[0])
    #print globalitems
    nextip = judge(ip)
    #print nextip
    #sys.exit()
    while True:
        try:
            whoisData = getWhois(nextip)
        except:
            time.sleep(5)
            continue
        iprange = getIpRange(whoisData)
        if iprange:
            writeWhois("logs/" + iprange, whoisData)
            tempip = getNextIp(nextip, iprange)
            nextip = judge(tempip)
        else:
             time.sleep(5)
             continue      
            
def process(ip):
    try:
        whoisData = getWhois(ip)
    except:
        time.sleep(5)
        process(ip)
    iprange = getIpRange(whoisData)
    print iprange
    if iprange:
        writeWhois("logs/" + iprange, whoisData)
        nextip = getNextIp(iprange)
        process(nextip)
    else:
        time.sleep(5)
        process(ip)
            
if __name__=="__main__":
    initConfig()
    #print getWhois("27.0.48.0")
    #print readWhois().decode("utf-8")
    #print getIpRange(readWhois().decode("utf-8"))
    #createForder()
    #process('36.9.41.0')
    #handle(sys.argv[1])
    #print getLogIpRange("0.0.0.0")
    #print judge(sys.argv[1])
    handle2(sys.argv[1])
    #globalitems = getItems("46")
    #print globalitems
    #print getcExtIp("46.255.255.0")
    
    #for i in range(1,225):
    #    print str(i) + ":\t" + str(len(getItems(str(i))))