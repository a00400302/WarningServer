import base64
import json
import os

import requests
from PIL import Image
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files import File
from django.http import JsonResponse
from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from Warning.consumers import send_group_msg
from Warning.models import PushUser, WarningHistory
from Warning.serializers import PushSerializer, WaringSerializer, UserSerializer
from .filters import WaringFilter


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
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器
    filter_class = WaringFilter
    ordering_fields = ['time', ]
    ordering = ['time']


def changepwd(request):
    var = permissions.IsAuthenticated()
    permission = var.has_permission(request, None)
    myresp = {}
    if permission:
        myresp['message'] = "错误"
        if request.method == 'POST':
            username = request.POST.get('username', None)
            passworda = request.POST.get("passworda", None)
            passwordb = request.POST.get("passwordb", None)
            if passwordb is not None and passworda is not None and username is not None:
                user = authenticate(username=username, password=passworda)
                if user is not None:
                    if user.is_active:
                        user.set_password(passwordb)
                        user.save()
                        myresp['code'] = 200
                        myresp['message'] = "修改成功"
                    else:
                        myresp['code'] = 100
                        myresp['message'] = "用户未激活"
                else:
                    myresp['code'] = 101
                    myresp['message'] = "用户名或密码错误"
            else:
                myresp['code'] = 102
                myresp['message'] = "参数错误"
        else:
            myresp['code'] = 103
            myresp['message'] = "请求方式错误"
    else:
        myresp['code'] = 104
        myresp['message'] = "权限错误"
    return JsonResponse(myresp, safe=False)


def camerapushsave(request):
    myresp = {}
    try:
        req = json.loads(request.body)
        if not req.__contains__('pic_data'):
            myresp['code'] = 102
            myresp['message'] = "参数错误"
            return JsonResponse(myresp, safe=False)
        datas = req['pic_data']
        if datas.__contains__('data:image'):
            datas = datas.split(',')[1]
        save_warning(datas, 2)
        send_group_msg("hello", {'asdf': "1123"})
        send_message(2)
        myresp['code'] = 200
        myresp['message'] = "保存成功"
        return JsonResponse(myresp, safe=False)
    except Exception as e:
        print(e)
        myresp['code'] = 500
        myresp['message'] = "保存失败"
        return JsonResponse(myresp, safe=False)


def pushsave(request):
    myresp = {}
    try:
        req = json.loads(request.body)
        if not req.__contains__('data'):
            myresp['code'] = 102
            myresp['message'] = "参数错误"
            return JsonResponse(myresp, safe=False)
        count = 0
        # for i in req['data']["algorithm_data"]["target_info"]:
        #     if i["name"] == "vehicle_becak":
        count += 1
        save_warning(req['pic_data'], 1)
        send_group_msg("hello", {'asdf': "1123"})
        # if count > 0:
        #     myresp['code'] = 200
        #     myresp['message'] = "保存成功"
        #     send_message(1)
        # else:
        #     myresp['code'] = 101
        #     myresp['message'] = "没有找到对应的数据"
        return JsonResponse(myresp, safe=False)
    except Exception as e:
        print(e)
        myresp['code'] = 500
        myresp['message'] = "保存失败"
        return JsonResponse(myresp, safe=False)


# 警告保存
def save_warning(baseString, warning_type):
    # 大图File
    img_data = base64.b64decode(baseString)
    string_ = baseString[(baseString.__len__() - 11):baseString.__len__()]
    big_img = open('./' + string_ + '.jpg', 'wb')
    big_img.write(img_data)
    big_img.close()
    # 小图base64
    small_img = base64_to_img(baseString, "./smallTemp.png")
    data = WarningHistory()
    data.bigImg = File(open('./' + string_ + '.jpg', 'rb'))
    data.imgBase = small_img
    data.type = warning_type
    data.save()
    os.remove('./' + string_ + '.jpg')


# base64转图片
def base64_to_img(bstr, file_path):
    imgdata = base64.b64decode(bstr)
    file = open(file_path, 'wb')
    file.write(imgdata)
    file.close()
    compress(file_path)
    bsfile = open(file_path, 'rb')
    s = base64.b64encode(bsfile.read())
    bsfile.close()
    os.remove(file_path)
    return str(s, 'utf8')


# 压缩
def compress(param):
    im = Image.open(param)
    (x, y) = im.size  # 读取图片尺寸（像素）
    x_1 = 165  # 定义缩小后的标准宽度
    y_1 = int(y * x_1 / x)  # 计算缩小后的高度
    out = im.resize((x_1, y_1), Image.ANTIALIAS)  # 改变尺寸，保持图片高品质
    out.save(param)


def send_message(warning_type):
    a = PushUser.objects.all()
    for i in a:
        content = ""
        if warning_type == 1:
            content = "尊敬的" + i.name + ",系统发生三轮车识别报警，请在平台查看【宇信科技】"
        elif warning_type == 2:
            content = "尊敬的" + i.name + ",系统发生行人识别报警，请在平台查看【宇信科技】"

        if i.enable:
            data = {
                "userid": 50,
                "timestamp": 20120701231212,
                "sign": "4d4844683bc346b32f19e04a1f5711f6",
                "mobile": i.phone,
                "content": content,
                "sendTime": "",
                "action": "send",
                "extno": "",
            }
            url = "http://112.74.59.69:8088/v2sms.aspx"
            r = requests.post(url, data=data)
            print(r.text)
