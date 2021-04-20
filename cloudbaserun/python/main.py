import os
import hashlib
from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/')
# def hello_world():
#     return 'Hello World!'
# def handle():
#     signature = request.args.get("signature")  # 先获取加密签名
#     timestamp = request.args.get('timestamp')  # 获取时间戳
#     nonce = request.args.get("nonece")  # 获取随机数
#     echostr = request.args.get("echostr") # 获取随机字符串
#     token = "gzhtest" #自己设置的token
#     # 使用字典序排序（按照字母或数字的大小顺序进行排序）
#     list = [token, timestamp, nonce]
#     list.sort()

#     # 进行sha1加密
#     temp = ''.join(list)
#     sha1 = hashlib.sha1(temp.encode('utf-8'))
#     # map(sha1.update, list)
#     hashcode = sha1.hexdigest()
#     # 将加密后的字符串和signatrue对比，如果相同返回echostr,表示验证成功
#     print(hashcode +'---'+ signature)
#     if hashcode == signature:
#         return echostr
#     else:
#         return ""
def get(self):
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        # 按照文档提供的方式进行计算签名值,进行比对
        sign_list = ["gzhtest", timestamp, nonce]
        sign_list.sort()
        # 拼接字符串
        sign_temp_str = "".join(sign_list)
        # sha1加密,获取签名值
        sign_str = hashlib.sha1(sign_temp_str).hexdigest()
        # 验证请求是否来自微信服务器,比较自己生成的签名与微信签名,若相同则表示请求来自微信服务器
        if signature == sign_str:
            # 微信要求校验成功返回之前发送过来的echostr,原样返回即可, 接入成功
            return self.write(echostr)
        else:
            # 校验失败
            return ""
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
