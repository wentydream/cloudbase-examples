import os
import hashlib
from flask import Flask,request
import xml.etree.ElementTree as ET
import time
import requests

app = Flask(__name__)

@app.route('/')
def get_request(): # 接受微信发送的GET请求
    signature = request.args.get("signature")  # 先获取加密签名
    timestamp = request.args.get('timestamp')  # 获取时间戳
    nonce = request.args.get("nonce")  # 获取随机数
    echostr = request.args.get("echostr") # 获取随机字符串
    token = "gzhtest" #自己设置的token
    # 使用字典序排序（按照字母或数字的大小顺序进行排序）
    list = [token, timestamp, nonce]
    list.sort()

    # 进行sha1加密
    temp = ''.join(list)
    sha1 = hashlib.sha1(temp.encode('utf-8'))
    hashcode = sha1.hexdigest()
    # 将加密后的字符串和signatrue对比，如果相同返回echostr,表示验证成功
    if hashcode == signature:
        return echostr
    else:
        return ""

@app.route('/', methods=["POST"])
def post_request():
    msg_xml_str = request.data
    if not msg_xml_str:
        return "success"
    # 解析消息
    msg_xml_dict_all = ET.fromstring(msg_xml_str)
    # 获取消息类型, 消息内容等信息
    msg_type = msg_xml_dict_all.find('MsgType').text
    # 需要回复的信息内容字典
    response_dict = dict()
    response_dict['ToUserName'] = msg_xml_dict_all.find('FromUserName').text
    response_dict['FromUserName'] = msg_xml_dict_all.find('ToUserName').text
    response_dict['CreateTime'] = int(time.time())
    response_dict['MsgType'] = "text"
    # 需要回复的信息模板
    response_xml_str = """<xml>
                            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                            <CreateTime>{CreateTime}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{Content}]]></Content>
                        </xml>"""
    # 当msg_type消息类型的值为event时, 表示该消息类型为推送消息, 例如微信用户 关注公众号(subscribe),取消关注(unsubscribe)
    if msg_type == "event":
        # 事件推送消息
        msg_event = msg_xml_dict_all.find('Event').text
        if msg_event == "subscribe":
            # 用户关注公众号, 回复感谢信息
            response_dict["Content"] = "欢迎" + response_dict['ToUserName'] + "，感谢您的关注!"
            response_xml_str = response_xml_str.format(**response_dict)
            return response_xml_str
    elif msg_type == "text":
        # 文本消息, 获取消息内容, 用户发送 哈哈, 回复 呵呵
        msg_body = msg_xml_dict_all.find('Content').text
        # 文本消息，获取天气
        if msg_body.find("天气") >= 0:
            if msg_body == "天气":
                rep = (requests.get('https://www.tianqiapi.com/free/day?appid=93511519&appsecret=mwIdNr9z')).json()
            else:
                city = msg_body.replace("天气","")
                rep = (requests.get('https://www.tianqiapi.com/free/day?appid=93511519&appsecret=mwIdNr9z&city=' + city)).json()

            if "errmsg" in rep:
                response_dict["Content"] = rep['errmsg']
            else:
                response_dict["Content"] =('城市：{}\n天气：{}\n温度：{}\n高温：{}\n低温：{}\n风力：{}\n风向：{}\n风速：{}\n风力等级：{}\n空气质量：{}'
                    .format(rep['city'],rep['wea'],rep['tem']+'°C',rep['tem_day']+'°C',rep['tem_night']+'°C',rep['win_speed'],rep['win'],
                    rep['win_meter'],rep['win_speed'],rep['air']))
            return response_xml_str.format(**response_dict)
    # 其他一律回复 success
    return "success"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
