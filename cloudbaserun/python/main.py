import os

from flask import Flask

app = Flask(__name__)

@app.route('/')

def check(request):
    wechat_data = request.GET
    signature = wechat_data['signature']
    timestamp = wechat_data['timestamp']
    nonce = wechat_data['nonce']
    echostr = wechat_data['echostr']
    token = 'gzhtest'
 
    check_list = [token, timestamp, nonce]
    check_list.sort()
    s1 = hashlib.sha1()
    s1.update(''.join(check_list).encode())
    hashcode = s1.hexdigest()
    print("handle/GET func: hashcode, signature:{0} {1}".format(hashcode, signature))
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse("")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)