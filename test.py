import requests




def sendMessage():

    url = "http://112.74.59.69:8088/v2sms.aspx"
    r = requests.post(url, data=data)
    print(r.text)

data = {
    "userid": 50,
    "timestamp": 20120701231212,
    "sign": "4d4844683bc346b32f19e04a1f5711f6",
    "mobile": 13326940714,
    "content": "尊敬的亮,系统发生三轮车识别报警，请在平台查看【宇信科技】",
    "sendTime": "",
    "action": "send",
    "extno": "",
}

sendMessage()