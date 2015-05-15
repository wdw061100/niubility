# -*- coding: utf-8 -*-
import os 
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from werobot.robot import werobot
from werobot.session.saekvstorage import SaeKVDBStorage
from douban_client import DoubanClient
from douban import *

session_storage = SaeKVDBStorage()

robot = werobot.WeRoBot(token="freesz", enable_session=True,
                        session_storage=session_storage)

client = DoubanClient(API_KEY, API_SECRET, REDIRECT_URI, SCOPE)

@robot.text
def last(message, session):
    if message.content == u'大牛' or message.content == u'书名' or message.content == u'豆瓣':
        session['last'] = message.content
        
@robot.filter("大牛")
def person(message, session):
    return "大牛列表,请输入TED牛人序号, 待完成"
  
@robot.filter("书名")
def bookname(message, session):
    return "请输入书名"

# 豆瓣oauth2鉴权   
@robot.filter("豆瓣")
def douban(message, session):
    session['code'] = 0
    code  = session.get('code', 0)
    # todo finish check time
    if (0 == code):
        print client.authorize_url
        return client.authorize_url
    else:
        return "auth ok " + code

@robot.text
def auth(message, session):
    last  = session.get('last', 0)
    print message.content
    if last == u"豆瓣":
        print message.content
        session['code'] = 0
        client.auth_with_code(message.content)
        print client.token_code
        if '' != client.token_code:
            session['code'] = message.content
            return "auth ok  " + message.content
        else:
            return "auth failed, please check the code"

@robot.text
def book(message, session):
    last  = session.get('last', 0)
    print message.content
    if last == u"书名":
        code  = session.get('code', 0)
        if (0 == code):
            return "请输入'豆瓣'完成授权"
        else:
     
        # client.book.search(q, tag, start, count)  
        # ret = client.book.search(message.content, 0, 0, 3)
        #print ret
            return "开始豆瓣查询,待完成"

@robot.text
def session_times(message, session):
    count = session.get("count", 0) + 1
    session["count"] = count
    return "请输入'大牛','书名', 你累计发了 %s 条消息" % count

@robot.subscribe
def subscribe(message):
        return "Weclome to niubility! 输入'大牛','书名',有惊喜哦！"


