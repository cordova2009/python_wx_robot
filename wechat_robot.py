#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#authot yujunyi
import itchat
import urllib.request
import requests
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
        #图灵机器人api地址
        self.api_url = "http://www.tuling123.com/openapi/api"
        #图灵api请求key 需要到官网申请
        self.key = '3869ad1b82cc41ffa4757e7799c88609'
        #是否启用图灵机器人 0不启用  1启用
        self.chanenl = 0
        #是否启用自动回复 0不启用  1启用
        self.re_flag = 1
        #用户回复计数标识 
        self.user_re_poor = {}

    

    def tuling(self,msg):
        data = {'key':self.key,'info':msg['Text']}
        req = requests.post(self.api_url,data=data).text
        s = requests.session()
        s.keep_alive = False
        reply = json.loads(req)['text']
        return reply


bot = Robot()
# itchat.send(msg,toUserName = userName) ##发送信息给个人,data就是爬取的内容
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print(msg)
    return
    if re_flag == 1:
        if msg['Text'] == '1' and chanenl == 1 :
            itchat.send("机器人聊天模式已开启不必重复开启\n\n(回复0可关闭机器人聊天)!", msg['FromUserName'])
        elif msg['Text'] == '1' and not chanenl == 1:
            chanenl = 1
            itchat.send("机器人聊天模式开启,来畅快的聊天吧\n\n(回复0可关闭机器人聊天)!", msg['FromUserName'])
        elif msg['Text'] == '0' and chanenl == 1:
            chanenl = 0
            itchat.send("机器人聊天模式关闭!", msg['FromUserName'])
        elif msg['Text'] == 'gb' or msg['Text'] == '关闭' or msg['Text'] == '去掉' or msg['Text'] == '关闭回复':
            re_flag = 0
            chanenl = 0
            itchat.send("自动回复已关闭!\n\n回复kq或者开启可启用自动回复!", msg['FromUserName'])
        elif msg['Text'] != '1' and msg['Text'] != '0' and chanenl == 1:
            itchat.send("【tu机器人回复】"+tuling(msg), msg['FromUserName'])
        else:
            itchat.send("【自动回复】您好我现在有事不在，一会和你联系.\n\n回复1可开启机器人聊天!\n\n回复gb或者关闭可关闭自动回复!" , msg['FromUserName'])
    elif re_flag == 0:
        if msg['Text'] == 'kq' or msg['Text'] == '开启':
            re_flag = 1
            itchat.send("自动回复已开启!", msg['FromUserName'])
 


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    #获取自己的username
    myUserName = itchat.get_friends(update=True)[0]['UserName']
    print("登录用户",myUserName)
    itchat.run(True)
# itchat.run()
# group_text(msg)#发送信息到群

