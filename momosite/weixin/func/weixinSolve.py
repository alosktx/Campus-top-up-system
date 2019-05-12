import hashlib
import xml.etree.ElementTree as ET
import time
import requests
import json
import urllib
from django.http import HttpResponse

class weixinSolve:
    # python的构造方法,new一个对象时，自动启动该方法
    def __init__(self, token):
        # 初始化token
        self.token = token
        # 建立一个字典，里面存放xml格式的所有数据
        self.xml_dict = dict()
        
# =========================微信接口验证=============================
    # 进行与微信平台连接的签名验证
    # 参数signature, timestamp, nonce都是从服务器获取的
    def valid(self, signature, timestamp, nonce):
        # 进行微信规定的验证算法
        # 把token,timestamp,nonce放入列表中
        tmpList = [self.token, timestamp, nonce]
        # 对列表进行排序
        tmpList.sort()
        # 把排好序的列表，合并成字符串
        tmpStr = ''.join(tmpList)
        # 对字符串进行sha1加密
        hashStr = hashlib.sha1(tmpStr.encode()).hexdigest()
        # 数字签名判断,如果签名是对的，则为True
        if hashStr == signature:
            return True
        else:
            return False

# ============================微信消息处理主体方法===========================
    def responseMsg(self, webData):
        try:
            # 把传来的数据，做成xml树，把xml标签里的数据放进该树里
            xmlData = ET.fromstring(webData)
            
            # 上述xml类型的数据，放入self.xml_dict字典中
            # 从xml对象中，取出用户操作的类型
            msg_type = xmlData.find('MsgType').text
            # 获取微信公众账号ID
            self.xml_dict['ToUserName'] = xmlData.find('ToUserName').text
            # 获取微信用户端的用户名OpenID
            self.xml_dict['FromUserName'] = xmlData.find('FromUserName').text
            
            # 注意：tousername, fromusername, createtime,msgtype是什么类型事件都有
            # 消息类型独有：Content, MsgId
            # 事件类型独有：Event, EventKey
            # 而我们不清楚收到的是什么类型的操作,故而根据类型，读取xml标签内容
            
            
            # 如果类型是text,即表示用户发消息给平台
            if msg_type == 'text':
                # 获取用户发来的文本内容
                self.xml_dict['Content'] = xmlData.find('Content').text
                # 处理用户发来的消息，获取要发送的内容
                content = self.handleText()
                return content
            # 如果类型是event,即处理事件，如菜单点击，新关注的客户
            elif msg_type == 'event':
                # 获取事件类型
                self.xml_dict['Event'] = xmlData.find('Event').text
                self.xml_dict['EventKey'] = xmlData.find('EventKey').text
                content = self.handleEvent()
                return content
            else:
                content = "看来我要升级了"
                content = self.postText(content)
                return content
            
        except:         # 抛出异常
            content = "出问题了"
            content = self.postText(content)
            return content
# ========================微信消息处理功能实现方法===========================
    # 处理用户发消息操作的方法
    def handleText(self):
        # 获取用户发过来的消息, 去掉两边的空格或\n等
        keyword = self.xml_dict['Content']
        # 图灵聊天机器人,接入接口
        chaturl_1 = "http://www.tuling123.com/openapi/api?key=b1e21e4543ae43e2b6e4fde713bc008d"
        info = "&info='{%s}'"%keyword
        # 把空格用%20代替， url一般自动转空格为%20，但这是代码操作，没有自动转%20，会出错
        info = info.replace(' ', '%20')
        # 合并url
        chaturl = chaturl_1 + info
        # 获取当前url里的网页源码
        response = requests.get(chaturl)
        # 把网页源码加载成  json格式  的对象
        j = json.loads(response.text)
        # 从json对象中，提取出智能机器返回的话，然后作为平台输出的消息
        contentStr = j['text']

        # 把输出的消息，加个马甲，改装成微信规定的格式，用包装好的方法改装
        # 然后获取该格式
        resultStr = self.postText(contentStr)
        # 返回该格式
        return resultStr

    # 处理事件方法
    def handleEvent(self):
        contentStr = '没有触发任何事件，真的很奇怪哎!'
        event = self.xml_dict['Event']
        key = self.xml_dict['EventKey']

        # 当有新用户关注时
        if event == 'subscrib':
            contentStr = "感谢您的关注"
        # 当用户取消关注时，不发生任何事情
        elif event == 'unsubscribe':
            pass
        # 当用户点击菜单时, CLICK是我设置菜单点击返回一个事件值时，设置的, 一下key都是自定
        elif event == 'CLICK':
            # 点击联系方式时
            if key == 'phone':
                contentStr = "我的电话是17307402811"
            elif key == 'chongzhi':
                contentStr = "还在开发中..."
        else:
            contentStr = "还在开发中..."
            
        resultStr = self.postText(contentStr)
        return resultStr

# ============================微信信息发送功能实现方法===========================
    # 用于把文本消息发送到平台，参数：要发送的消息
    def postText(self, content):
        # 回复的xml模版
        # 构建消息回复xml格式的文本
        textTpl = '''<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%d</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        <FuncFlag>0</FuncFlag>
                    </xml>'''
        
        # 将xml格式文本格式化
        resultStr = textTpl%(self.xml_dict['FromUserName'], self.xml_dict['ToUserName'], int(time.time()), content)
        
        return resultStr

    
            
