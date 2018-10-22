#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#authot yujunyi
import itchat
import urllib.request
import requests
import datetime
import random
import string
import json
import os
import re
from urllib.parse import quote
from aip import AipSpeech


#伪装成谷歌浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
#创建opener对象
opener = urllib.request.build_opener()
#添加报文头
opener.addheaders = [headers]
#将operner添加为全局
urllib.request.install_opener(opener)

#百度语音识别配置类
class  BaiduSpeech(object):
    """docstring for  Speech"""
    def __init__(self):
        """ 你的 app_id AK SK """
        self.app_id = 'your'
        self.api_key = 'your'
        self.secret_key = 'your'

    #将文字转为语音文件
    def text_2_voice(self,text):
        city = text[0:3] or random.randint(0,9)
        st = datetime.datetime.now().strftime('%Y%m%d')
        filename = 'weather_%s%s.mp3'%(city,st)
        filename = quote(filename,safe=string.printable)
        #判断是否已经生成这个文件
        if os.path.exists(filename):
            return filename
        else:
            aipSpeech = AipSpeech(self.app_id, self.api_key, self.secret_key)
            #详细接口参数介绍见百度语音
            result = aipSpeech.synthesis(text, 'zh', 1, {
                'vol': 5,
            })
            if not isinstance(result,dict):
                
                with open(filename,'wb') as f:
                    f.write(result)
                    return filename
        return None


class Robot(object):
    """docstring for Robot"""
    def __init__(self):

        #天气查询接口
        self.wh_url ="http://tianqi.moji.com/api/redirect/"
        #天气城市搜索接口
        self.c_url ="http://tianqi.moji.com/api/citysearch/"

        self.joke_url = "http://www.qiushibaike.com/hot/page/"
        #当前页数
        self.page = 1
        #当前序号
        self.num = 1


    # 根据名称获取这个城市天气查询的url
    def get_city_url(self,city_name):
        #  构造查询相应城市天气的url  
        url = self.c_url + city_name
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
        return None

    def get_weather(self,msg):
        city = msg.Text[-4:-2]
        url = None

        if city:
            url = self.get_city_url(city)
        else:
            city = msg['User']['City']
            if city:
                url = self.get_city_url(city)
        #获取url数据
        if not url:
            city = city or "深圳"
            return "我还不知道%s的天气"%city
        else:
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
                    print("joke:",str(self.num),":",j)
                    self.num += 1
                    self.page += 1
                    j = j.replace("<span>","").replace("</span>","")
                    #处理换行
                    j = re.compile('\n+').sub('\n',j)
                    return re.compile('<br\s*?/?>').sub('\n',j)
            self.page += 1


bot = Robot()
speech = BaiduSpeech()
# itchat.send(msg,toUserName = userName) ##发送信息给个人,data就是爬取的内容
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if '笑话' in msg['Text']:
        itchat.send(bot.talk_joke(), msg['FromUserName'])
    elif '天气' in msg['Text']:
        text = bot.get_weather(msg)
        if text:
            file = speech.text_2_voice(text)
            if file:
                itchat.send_file(file, msg['FromUserName'])
            else:
                itchat.send("api接口错误", msg['FromUserName'])
        else:
            itchat.send("未查询到相应天气信息", msg['FromUserName'])
   

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    #获取自己的username
    myUserName = itchat.get_friends(update=True)[0]['UserName']
    print("登录用户",myUserName)
    itchat.run(True)
