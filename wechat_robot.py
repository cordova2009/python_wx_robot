#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#authot yujunyi
import pypinyin
import itchat
import urllib.request
import requests
import json
import re


url ="https://tianqi.moji.com/weather/china/guangdong/shenzhen"

jokeUrl = "http://www.qiushibaike.com/hot/page/"
#当前页数
page = 1
num = 1
#是否启用图灵机器人 0不启用  1启用
chanenl = 0
#是否启用自动回复 0不启用  1启用
reFlag = 1

#伪装成谷歌浏览器
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
#创建opener对象
opener = urllib.request.build_opener()
#添加报文头
opener.addheaders = [headers]
#将operner添加为全局
urllib.request.install_opener(opener)


def talk_joke(jokeUrl):
    global page
    global num
    #匹配笑话的正则表达式
    rule_joke = r'<div class="content">((?:.|[\r\n])*?)</div>'
    while page < 50 :
        jokeUrl = jokeUrl + str(page)
        try:
            req = urllib.request.urlopen(jokeUrl).read().decode("UTF-8","ignore")
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
                print("笑话"+str(num)+":",j)
                num += 1
                page += 1
                j = j.replace("<span>","").replace("</span>","")
                #处理换行
                j = re.compile('\n+').sub('\n',j)
                return re.compile('<br\s*?/?>').sub('\n',j)
        page += 1




def group_text(msg):
    group = itchat.get_chatrooms(update=True)
    from_user = ''
    to_group = ''
    for g in group:
        if g['NickName'] == '一家人':
            to_group = g['UserName']
            break
    if to_group.strip():
        itchat.send(msg,to_group)
# 不带声调的(style=pypinyin.NORMAL)
def hp(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s



def get_weather(url,msg):
    province = msg['User']['Province']
    city = msg['User']['City']

    if province and city:
        url = url.replace("guangdong",hp(province)).replace("shenzhen",hp(city))
        print(url)
    #获取url数据
    data = urllib.request.urlopen(url).read().decode("UTF-8","ignore")
    print("内容:%s/n",data)
    #定义正则
    pat ='(<meta name="description" content=")(.*?)(">)'
    # print("内容:%s/n",data)
    res = re.search(pat,data).group(2)
    # print("内容:%s/n",res)

    
    # users = itchat.search_friends(name=u'沈阳')
    # userName = users[0]['UserName']#获取username
    return res.replace("墨迹天气","芋头")

def tuling(msg):
    api_url = "http://www.tuling123.com/openapi/api"
    data = {'key':'3869ad1b82cc41ffa4757e7799c88609','info':msg['Text']}
    req = requests.post(api_url,data=data).text
    s = requests.session()
    s.keep_alive = False
    reply = json.loads(req)['text']
    return reply

# itchat.send(msg,toUserName = userName) ##发送信息给个人,data就是爬取的内容
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    global chanenl
    global reFlag
    if msg['Text'] in '天气预报':
        itchat.send(get_weather(url,msg), msg['FromUserName'])
    elif '笑话' in msg['Text']:
        itchat.send(talk_joke(jokeUrl), msg['FromUserName'])
    elif reFlag == 1:
        if msg['Text'] == '1' and chanenl == 1 :
            itchat.send("机器人聊天模式已开启不必重复开启\n\n(回复0可关闭机器人聊天)!", msg['FromUserName'])
        elif msg['Text'] == '1' and not chanenl == 1:
            chanenl = 1
            itchat.send("机器人聊天模式开启,来畅快的聊天吧\n\n(回复0可关闭机器人聊天)!", msg['FromUserName'])
        elif msg['Text'] == '0' and chanenl == 1:
            chanenl = 0
            itchat.send("机器人聊天模式关闭!", msg['FromUserName'])
        elif msg['Text'] == 'gb' or msg['Text'] == '关闭' or msg['Text'] == '去掉' or msg['Text'] == '关闭回复':
            reFlag = 0
            chanenl = 0
            itchat.send("自动回复已关闭!\n\n回复kq或者开启可启用自动回复!", msg['FromUserName'])
        elif msg['Text'] != '1' and msg['Text'] != '0' and chanenl == 1:
            itchat.send("【tu机器人回复】"+tuling(msg), msg['FromUserName'])
        else:
            itchat.send("【自动回复】您好我现在有事不在，一会和你联系.\n\n回复1可开启机器人聊天!\n\n回复gb或者关闭可关闭自动回复!" , msg['FromUserName'])
    elif reFlag == 0:
        if msg['Text'] == 'kq' or msg['Text'] == '开启':
            reFlag = 1
            itchat.send("自动回复已开启!", msg['FromUserName'])
       


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    #获取自己的username
    myUserName = itchat.get_friends(update=True)[0]['UserName']
    print("登录用户",myUserName)
    itchat.run(True)
# itchat.run()
# group_text(msg)#发送信息到群

