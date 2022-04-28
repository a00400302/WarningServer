import base64
import json

import requests
from PIL import Image
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework.viewsets import ModelViewSet

from Warning.compress import Compress_img
from Warning.consumers import send_group_msg
from Warning.serializers import PushSerializer, WaringSerializer, UserSerializer
from Warning.models import PushUser, WarningHistory
from rest_framework import permissions
from django.contrib.auth.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PushViewSet(ModelViewSet):
    queryset = PushUser.objects.all()
    serializer_class = PushSerializer
    permission_classes = [permissions.IsAuthenticated]


class WaringViewSet(ModelViewSet):
    queryset = WarningHistory.objects.all()
    serializer_class = WaringSerializer
    permission_classes = [permissions.IsAuthenticated]


def changepwd(request):
    myresp = {}
    if request.method == 'POST':
        username = request.POST["username"]
        passworda = request.POST["passworda"]
        passwordb = request.POST["passwordb"]
        myresp['code'] = 1
        user = authenticate(username=username, password=passworda)

        if user is not None:
            if user.is_active:
                print("验证合法")
                user.set_password(passwordb)
                user.save()
                myresp['message'] = "成功"
            else:
                myresp['message'] = "用户未启用"
        else:
            myresp['message'] = "用户不存在"
        return JsonResponse(myresp, safe=False)
    else:
        myresp['code'] = 0
        return JsonResponse(myresp, safe=False)


def pushsave(request):
    req = json.loads(request.body)

    if not req.__contains__('data'):
        return HttpResponse("ok")
    count = 0
    for i in req['data']["algorithm_data"]["target_info"]:
        if i["name"] == "vehicle_becak":
            count += 1
            data = WarningHistory()
            data.imgBase = base64_to_img(req['pic_data'],"./a.jpg")
            data.save()
            send_group_msg("hello", {'asdf': "1123"})
    if count > 0:
        sendMessage()
    return HttpResponse("ok")



def base64_to_img(bstr, file_path):
    imgdata = base64.b64decode(bstr)
    file = open(file_path, 'wb')
    file.write(imgdata)
    file.close()
    compress = Compress_img('./a.jpg')
    compress.compress_img_PIL(way=1,show=False)
    bsfile = open('./result_a.jpg', 'rb')
    s = base64.b64encode(bsfile.read())
    return  str(s,'utf8')







def sendMessage():
    a = PushUser.objects.all()
    for i in a:
        data = {
            "userid": 50,
            "timestamp": 20120701231212,
            "sign": "4d4844683bc346b32f19e04a1f5711f6",
            "mobile": i.phone,
            "content": "尊敬的qq在ww发生ee报警，请尽快赶往现场处理！恢复通气前请先关闭炉具开关！【瓶安卫士】",
            # "content": "尊敬的"+i.name+",系统发生三轮车识别报警，请在平台查看【宇信科技】",
            "sendTime": "",
            "action": "send",
            "extno": "",
        }
        url = "http://112.74.59.69:8088/v2sms.aspx"
        r = requests.post(url, data=data)
        print(r.text)


