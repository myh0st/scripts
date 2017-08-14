#!/usr/bin/python 2.79
#-*- coding:utf-8 -*-

import re
import os
import sys
import time
import socket
import struct

configdrct = {}

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
    
def initConfig():
    for item in open("config.cnf"):
        key, value = item.strip().split("\t")
        configdrct[key] = value
    
def getWhoSrv(ip):
    key = ip.split(".")[0]
    return configdrct[key]

def writeLog(ip, filename):
    obj = open(filename, 'a')
    obj.writelines(ip+"\n")
    obj.close()
    
def writeData(data, filename):
    obj = open("logs/" + filename, "w")
    obj.write(data)
    obj.close()

def writefData(data, filename):
    obj = open("flogs/" + filename, "w")
    obj.write(data)
    obj.close()

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
    
def whois(ip):
    server = getWhoSrv(ip)
    try:
        data = getData(ip, server)
        iprange = getIpRange(data)
        if iprange:
            writeData(data, iprange)
        else:
            if re.search("limit", data) or re.search("access", data):
                time.sleep(5)
                whois(ip)
            elif re.search("inetnum", data):
                writefData(data, ip)
            elif re.search("\s+(\d+\.\d+.\d+\.\d+\s+-\s+\d+\.\d+.\d+\.\d+)", data):
                writeLog(ip, "other.txt")
            else:
                writeLog(ip, "failed.txt")
    except:
        writeLog(ip, "except.txt")
        
def printwhois(ip):
    server = getWhoSrv(ip)
    data = getData(ip, server)
    print data
    iprange = getIpRange(data)
    if iprange:
        writeData(data, iprange)
    else:
        if re.search("limit", data) or re.search("access", data):
            time.sleep(5)
            printwhois(ip)
        elif re.search("inetnum", data):
            writefData(data, ip)
        elif re.search("\s+(\d+\.\d+.\d+\.\d+\s+-\s+\d+\.\d+.\d+\.\d+)", data):
            writeLog(ip, "other.txt")
        else:
            writeLog(ip, "failed.txt")
    
def whoisFile(filename):
    for ip in open(filename):
        whois(ip.strip())
        time.sleep(1)
    
if __name__=="__main__":
    #print getWhois("220.18.156.5")
    #whois("220.15.215.5")
    if len(sys.argv) != 2:
        print "[-]usage: python " + sys.argv[0] + " ip( or filename)"
        sys.exit()
    initConfig()
    if os.path.exists(sys.argv[1]):
        whoisFile(sys.argv[1])
    else:
        printwhois(sys.argv[1])
        #getData(sys.argv[1], "whois.arin.net")