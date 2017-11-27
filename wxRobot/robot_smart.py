#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import itchat
import os
import re
import shutil
import time
from functions import get_functions, get_example, AUTO_REPLAY
from threading import Timer

from itchat.content import *

# KEY = '8edce3ce905a4c1dbb965e6b35c3834d'
KEY = 'b545f73ce82c45f5b63f3f4b20e6f4a9'


def get_response(msg):
    # 构造发送给图灵机器人服务器的数据
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(api_url, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        text = r.get('text')
        url = r.get('url', None)
        if url is not None:
            return text + '\n' + url
        else:
            return text
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except IOError:
        # 将会返回一个None
        return


def is_msg_from_myself(msgFromUserName):
    # 检查消息发送方是否为自己
    global myName
    return myName == msgFromUserName


# # 注册文本消息回复函数
# @itchat.msg_register(itchat.content.TEXT)
# def tuling_reply(msg):
#     global autoReplyFlag, timerSet, noReply, t  # 状态标志位
#     print(msg['Text'])
#     if is_msg_from_myself(msg['FromUserName']):
#         print("Replied!!")
#         autoReplyFlag = False
#         noReply = False
#         try:
#             t.cancel()
#             print("Timer Canceled")
#             timerSet = False
#         except:
#             pass
#         return None
#
#     if autoReplyFlag:
#         # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
#         default_reply = 'I received: ' + msg['Text']
#         # 如果图灵Key出现问题，那么reply将会是None
#         reply = get_response(msg['Text'])
#         # a or b的意思是，如果a有内容，那么返回a，否则返回b
#         # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
#         return '小K: ' + reply or '小K: ' + default_reply
#     else:
#         noReply = True
#         if not timerSet:
#             # if time.time()-noReplyStartTime >= 120:
#             print("Timer setting")
#             t = Timer(12, send_busy_status, [msg['FromUserName']])
#             t.start()
#             timerSet = True
#

def send_busy_status(user_name):
    global noReply, autoReplyFlag, timerSet
    print("Timer Working!")
    if noReply:
        content = "您好,我是主人的机器人小K\n注意:以'小K:'\t开头的都是自动回复的哦(^o^)\n"
        off_auto = r'如果不希望小K自动回复请在消息前面加上@符号' + '\n'
        functions = '您可以回复: #所有功能 来查看小K的功能\n'
        if AUTO_REPLAY:
            itchat.send(content + functions + off_auto, user_name)
        autoReplyFlag = True
        timerSet = False


#
# @itchat.msg_register([PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
# def text_reply(msg):
#     if msg['Type'] == 'Text':
#         reply_content = msg['Text']
#     elif msg['Type'] == 'Picture':
#         reply_content = r"图片: " + msg['FileName']
#     elif msg['Type'] == 'Card':
#         reply_content = r" " + msg['RecommendInfo']['NickName'] + r" 的名片"
#     elif msg['Type'] == 'Map':
#         x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,
#                                                                                                                     2,
#                                                                                                                     3)
#         if location is None:
#             reply_content = r"位置: 纬度->" + x.__str__() + " 经度->" + y.__str__()
#         else:
#             reply_content = r"位置: " + location
#     elif msg['Type'] == 'Note':
#         reply_content = r"通知"
#     elif msg['Type'] == 'Sharing':
#         reply_content = r"分享"
#     elif msg['Type'] == 'Recording':
#         reply_content = r"语音"
#     elif msg['Type'] == 'Attachment':
#         reply_content = r"文件: " + msg['FileName']
#     elif msg['Type'] == 'Video':
#         reply_content = r"视频: " + msg['FileName']
#     else:
#         reply_content = r"消息"
#
#     friend = itchat.search_friends(userName=msg['FromUserName'])
#     itchat.send(r"Friend:%s -- %s    "
#                 r"Time:%s    "
#                 r" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), reply_content),
#                 toUserName='filehelper')
#
#     itchat.send(r"小K已经收到你在【%s】发送的消息【%s】主人稍后回复。" % (time.ctime(), reply_content),
#                 toUserName=msg['FromUserName'])


# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    # print(msg)
    if msg['isAt']:
        content_message = msg['Content']
        print(content_message)
        start_at = content_message.find('\u2005')
        if start_at == -1:
            start_at = 0
        print(start_at)
        content = content_message[start_at:]
        print(content)
        # 'Content': '@阿宝\u2005宝宝真棒',
        smart_reply = '@' + msg['ActualNickName'] + ' ' + get_response(content) + '\n___[From__小K]'
        print(smart_reply)
        if AUTO_REPLAY:
            itchat.send(smart_reply, msg['FromUserName'])

            #  itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


# {msg_id:(msg_from,msg_to,msg_time,msg_time_touser,msg_type,msg_content,msg_url,msg_from_user_name)}
msg_dict = {}


# ClearTimeOutMsg用于清理消息字典，把超时消息清理掉
# 为减少资源占用，此函数只在有新消息动态时调用
def clear_timeout_msg():
    if msg_dict.__len__() > 0:
        for msgid in list(msg_dict):  # 由于字典在遍历过程中不能删除元素，故使用此方法
            if time.time() - msg_dict.get(msgid, None)["msg_time"] > 130.0:  # 超时两分钟
                item = msg_dict.pop(msgid)
                # print("超时的消息：", item['msg_content'])
                # 可下载类消息，并删除相关文件
                if item['msg_type'] == "Picture" \
                        or item['msg_type'] == "Recording" \
                        or item['msg_type'] == "Video" \
                        or item['msg_type'] == "Attachment":
                    print("要删除的文件：", item['msg_content'])
                    os.remove(item['msg_content'])


# 将接收到的消息存放在字典中，当接收到新消息时对字典中超时的消息进行清理
# 没有注册note（通知类）消息，通知类消息一般为：红包 转账 消息撤回提醒等，不具有撤回功能
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS])
def revocation(msg):
    mytime = time.localtime()  # 这儿获取的是本地时间
    # 获取用于展示给用户看的时间 2017/03/03 13:23:53
    msg_time_touser = mytime.tm_year.__str__() \
                      + "/" + mytime.tm_mon.__str__() \
                      + "/" + mytime.tm_mday.__str__() \
                      + " " + mytime.tm_hour.__str__() \
                      + ":" + mytime.tm_min.__str__() \
                      + ":" + mytime.tm_sec.__str__()
    msg_from_user_name = msg['FromUserName']
    msg_id = msg['MsgId']  # 消息ID
    msg_time = msg['CreateTime']  # 消息时间
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 消息发送人昵称
    msg_type = msg['Type']  # 消息类型
    msg_content = None  # 根据消息类型不同，消息内容不同
    msg_url = None  # 分享类消息有url
    # 图片 语音 附件 视频，可下载消息将内容下载暂存到当前目录
    wx_msg_text = msg['Text']
    if msg['Type'] == 'Text':

        msg_content = wx_msg_text

        global autoReplyFlag, timerSet, noReply, t  # 状态标志位
        print(wx_msg_text)
        if is_msg_from_myself(msg['FromUserName']):
            print("Replied!!")
            autoReplyFlag = False
            noReply = False
            try:
                t.cancel()
                print("Timer Canceled")
                timerSet = False
            except:
                pass
            return None

        if autoReplyFlag:
            # 查看功能
            if wx_msg_text == '所有功能':
                return '您可以使用下列功能:\n' + get_functions()
            elif wx_msg_text[:1] == r'#':
                return get_example(wx_msg_text[1:])
            elif wx_msg_text[:1] == r'@':
                print('do nothing')
            else:
                # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
                default_reply = 'I received: ' + wx_msg_text
                # 如果图灵Key出现问题，那么reply将会是None
                reply = get_response(wx_msg_text)
                # a or b的意思是，如果a有内容，那么返回a，否则返回b
                # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
                if AUTO_REPLAY:
                    return '小K: ' + reply or '小K: ' + default_reply
        else:
            noReply = True
            if not timerSet:
                # if time.time()-noReplyStartTime >= 120:
                print("Timer setting")
                t = Timer(12, send_busy_status, [msg['FromUserName']])
                t.start()
                timerSet = True

    elif msg['Type'] == 'Picture':
        msg_content = msg['FileName']

        try:
            # 下载图片
            wx_msg_text(msg['FileName'])
        except OSError:
            ''
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,
                                                                                                                    2,
                                                                                                                    3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = wx_msg_text
        msg_url = msg['Url']
    elif msg['Type'] == 'Recording':
        msg_content = msg['FileName']
        wx_msg_text(msg['FileName'])
    elif msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        wx_msg_text(msg['FileName'])
    elif msg['Type'] == 'Video':
        msg_content = msg['FileName']
        wx_msg_text(msg['FileName'])
    elif msg['Type'] == 'Friends':
        msg_content = wx_msg_text

    # friend = itchat.search_friends(userName=msg['FromUserName'])
    # itchat.send(r"Friend:%s -- %s    "
    #             r"Time:%s    "
    #             r" Message:%s" % (friend['NickName'], friend['RemarkName'], msg_time_touser, msg_content),
    #             toUserName='filehelper')

    if msg['Type'] != 'Text':
        if AUTO_REPLAY:
            itchat.send("小K已收到您的消息,主人稍后回复!\n\t时间: %s\n\t内容: %s" % (msg_time_touser, msg_content),
                        toUserName=msg['FromUserName'])

    # 更新字典
    # {msg_id:(msg_from,msg_time,msg_time_touser,msg_type,msg_content,msg_url)}
    msg_dict.update(
        {msg_id: {"msg_from": msg_from, "msg_time": msg_time, "msg_time_touser": msg_time_touser, "msg_type": msg_type,
                  "msg_content": msg_content, "msg_url": msg_url, "msg_from_user_name": msg_from_user_name}})
    # 清理字典
    clear_timeout_msg()


# 收到note类消息，判断是不是撤回并进行相应操作
@itchat.msg_register([NOTE])
def save_msg(msg):
    # print(msg)
    # 创建可下载消息内容的存放文件夹，并将暂存在当前目录的文件移动到该文件中
    if not os.path.exists("Revocation"):
        os.mkdir("Revocation")
    if re.search(r"\<replacemsg\>\<\!\[CDATA\[.*撤回了一条消息\]\]\>\<\/replacemsg\>", msg['Content']) is not None:

        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)

        old_msg = msg_dict.get(old_msg_id, {})

        # print(old_msg_id, old_msg)

        msg_send = r'您的好友：' \
                   + old_msg.get('msg_from', '') \
                   + r"  在 [" + old_msg.get('msg_time_touser', '') \
                   + r"], 撤回了一条 [" + old_msg['msg_type'] + "] 消息, 内容如下:" \
                   + old_msg.get('msg_content', '')
        if old_msg['msg_type'] == "Sharing":
            msg_send += r", 链接: " + old_msg.get('msg_url', '')
        elif old_msg['msg_type'] == 'Picture' \
                or old_msg['msg_type'] == 'Recording' \
                or old_msg['msg_type'] == 'Video' \
                or old_msg['msg_type'] == 'Attachment':
            msg_send += r", 存储在当前目录下Revocation文件夹中"

        # print('************' + old_msg['msg_content'])

        itchat.send(msg_send, toUserName='filehelper')  # 将撤回消息的通知以及细节发送到文件助手
        if AUTO_REPLAY:
            itchat.send('小K : 还想撤回 ? too naive!!! 消息已经保存存啦' + r'[偷笑]',
                        toUserName=old_msg.get('msg_from_user_name'))  # 将撤回消息的通知以及细节发送到文件助手
        try:
            shutil.move(old_msg['msg_content'], "Revocation")
        except IOError:
            print('move error')
        msg_dict.pop(old_msg_id)

        clear_timeout_msg()


# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login()

autoReplyFlag, timerSet, noReply = False, False, False
t = 0  # 定义全局变量t, 用作触发器使用，此行甚是丑陋；怎么才能更优雅呢？请大神指点。
myName = itchat.get_friends(update=True)[0]['UserName']
itchat.run()
