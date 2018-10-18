#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#authot yujunyi
import itchat
import urllib.request
import requests
from urllib.parse import quote
import string
import json
import re

#伪装成谷歌浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
#创建opener对象
opener = urllib.request.build_opener()
#添加报文头
opener.addheaders = [headers]
#将operner添加为全局
urllib.request.install_opener(opener)

class Robot(object):
    """docstring for Robot"""
    def __init__(self):

        #天气地址
        self.wh_url ="http://tianqi.moji.com/api/redirect/"

        self.joke_url = "http://www.qiushibaike.com/hot/page/"
        #当前页数
        self.page = 1
        #当前序号
        self.num = 1


    # 搜索这个城市
    def search_city(self,city_name):
        #  构造查询相应城市天气的url  
        url = "http://tianqi.moji.com/api/citysearch/%s"%city_name
        url = quote(url,safe=string.printable)
        text = urllib.request.urlopen(url).read().decode("UTF-8","ignore")
        # 异常捕获
        try:
            # 通过上面的url获取城市的id
            city_id = json.loads(text).get('city_list')[0].get('cityId')
            # 通过城市id获取城市天气
            city_url = self.wh_url + str(city_id)
            return city_url
        except:
            print('获取城市错误')

    def get_weather(self,msg):
        city = msg.Text[-4:-2]
        url = ""

        if city:
            url = self.search_city(city)
        else:
            city = msg['User']['City']
            if city:
                url = self.search_city(city)
        #获取url数据
        if url:
            data = urllib.request.urlopen(url,timeout=10).read().decode("UTF-8","ignore")
            #定义正则
            pat ='(<meta name="description" content=")(.*?)(">)'
            # print("内容:%s/n",data)
            res = re.search(pat,data).group(2)
            # print("内容:%s/n",res)

            # users = itchat.search_friends(name=u'沈阳')
            # userName = users[0]['UserName']#获取username
            print("内容:%s/n",res)
            return res.replace("墨迹天气","芋头")

    def talk_joke(self):
        #匹配笑话的正则表达式
        rule_joke = r'<div class="content">((?:.|[\r\n])*?)</div>'
        #限制条数  
        while self.page < 30 :
            url = self.joke_url + str(self.page)
            try:
                req = urllib.request.urlopen(url).read().decode("UTF-8","ignore")
            except:
                print("url open error!!!")
                continue
            jokes = re.compile(rule_joke).findall(req)
            if not jokes:
                continue
            for j in jokes:
                if 'contentForAll' in j or not j:
                    continue
                else:
                    print("笑话",str(self.num),":",j)
                    self.num += 1
                    self.page += 1
                    j = j.replace("<span>","").replace("</span>","")
                    #处理换行
                    j = re.compile('\n+').sub('\n',j)
                    return re.compile('<br\s*?/?>').sub('\n',j)
            self.page += 1


bot = Robot()
# itchat.send(msg,toUserName = userName) ##发送信息给个人,data就是爬取的内容
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if '笑话' in msg['Text']:
        itchat.send(bot.talk_joke(), msg['FromUserName'])
    elif '天气' in msg['Text']:
        itchat.send(bot.get_weather(msg), msg['FromUserName'])
   

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    #获取自己的username
    myUserName = itchat.get_friends(update=True)[0]['UserName']
    print("登录用户",myUserName)
    itchat.run(True)
