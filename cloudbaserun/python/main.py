import os
import hashlib
from flask import Flask,request
import xmltodict

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
    pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
