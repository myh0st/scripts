#!/usr/bin/env python
#coding:utf-8
from scapy.all import *
import subprocess
import re
import threading

def zombies_scan(zombie_ip):
	rep1 = sr1(IP(dst=zombie_ip)/TCP(flags='SA'),timeout=2)
	send(IP(dst=zombie_ip)/TCP(flags='SA'))
	rep2 = sr1(IP(dst=zombie_ip)/TCP(flags='SA'),timeout=2)
	if rep2[IP].id == (rep1[IP].id+2):
		print "[*]" + zombie_ip + " is Incremental!"
		target_ip = raw_input("input the target_ip :")
		port_scan(target_ip, zombie_ip)
	else:
		print "[*]" + zombie_ip + "is not Incremental!\n"



def host_scan():
	net = raw_input("\ninput the current Network :")
	cmd = "nmap -T4 -sn " + net
	#print cmd
	host = subprocess.Popen(cmd ,shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = host.communicate()
	#print out
	for i in out.split('\n'):
		try:
			r = re.match('Nmap+\s+scan+\s+report+\s+for+\s+\d+\S+',i)
			#print r.group()
			#r.group().split(' ')[4]
			t = threading.Thread(target = zombies_scan, args = (r.group().split(' ')[4],))
			t.start()
			t.join()
		except:
			pass

	

def port_scan(target_ip,zombie_ip):
	print "------begin to scan target_ip!-------"
	for port in range(1,100):
		try:
			start = sr1(IP(dst=zombie_ip)/TCP(flags='SA',dport=port),timeout=2)
			send(IP(src=zombie_ip,dst=target_ip)/TCP(flags='S',dport=port))
			end = sr1(IP(dst=zombie_ip)/TCP(flags='SA'),timeout=2)
			if end[IP].id == (start[IP].id + 2):
				print "[*]" + target_ip + ':' + port + "is open"
		except:
			pass



	

if __name__ == "__main__":
	print "--------Welcome To Use Zombies_scan---------"
	print "0.scan to find the available zombies, then scan."
	print "1.input a target_ip and zombie_ip to scan."
	choice = raw_input("\nPlease input your choice :")
	#choice = '0'
	if choice == '0':
		host_scan()

	elif choice == '1':
		target_ip = raw_input("The target_ip :")
		zombie_ip = raw_input("The zombie_ip :")
		port_scan(target_ip,zombie_ip)

	else:
		print "your input is wrong, please try again!"
		exit()








