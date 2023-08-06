"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import re
import requests
from lxml import etree
from retrying import retry
import sys,os
sys.path.append(os.path.dirname(__file__))
from tools.user_agent import user_agent as u
import random

@retry()
def baidu_spider(keyword):
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&{}".format(keyword)
    data = {'wd':keyword}
    headers = u()
    #print(headers)

    r = requests.get(url, params=data,headers=headers)
    message = []
    print(r.url)
    content_list = etree.HTML(r.text)
    #print(content_list.xpath("//*//text()"))

    number = content_list.xpath('//div[@id="content_left"]/*')
    if len(number) == 0:
        baidu_spider(keyword)
    for i in range(len(number)-1):
        title = "".join(content_list.xpath('//*[@id="%d"]/h3//text()' % i))
        title = re.findall(r'\w+[\u4e00-\u9fa5]+\w+', title)

        text = "".join(content_list.xpath('//*[@id="%d"]/div[1]//text()' % i))
        text = re.findall(r'\w+[\u4e00-\u9fa5]+\w+', text)

        source = "".join(content_list.xpath('//*[@id="%d"]/div[2]//text()' % i))
        source= re.findall(r'\w+[\u4e00-\u9fa5]+\w+', source)

        if title == []:
            pass
        else:

            message.append(["标题: "+"".join(title),"内容:   "+"".join(text),"来源:    "+"".join(source)])
    if "罪" in keyword:
        for i in message:
            for i_ in i:
                if "中华人民共和国" in i_:
                    print(i[1])
                    return i[1]
    return "".join(random.choice(message))

#print(baidu_spider("强奸"))