import base64
import socket
import threading
import json
import requests
from watchdog.observers import Observer
from watchdog.events import *


def dispose_client_request(tcp_client_1, tcp_client_address):
    # 5 循环接收和发送数据
    while True:
        recv_data = tcp_client_1.recv(4096)
        # 6 有消息就回复数据，消息长度为0就是说明客户端下线了
        if recv_data:
            try:
                checkData(recv_data.decode('utf-8'))
            except Exception as e:
                print(e)  # send_data = "消息已收到，正在处理中...".encode()  # tcp_client_1.send(send_data) # 发送数据
        else:
            tcp_client_1.close()
            break


start = "##"
end = "&&"


isFtping = False

def checkData(data):
    print(data)
    data_len = int(data.split('QN')[0].replace("##", ""))
    split = data[6:data_len + 6]
    split = split.replace("&&", "")
    split = split.replace("CP=", "")
    data_list = split.split(";")
    map = {}
    for i in data_list:
        map[i.split("=")[0]] = i.split("=")[1]
    url = ""
    with open("config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        url = load_dict["url"]
    try:
        requests.post(url + "environment/", json=map)
    except Exception as e:
        print(e)


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            image = open(event.src_path, 'rb')
            s = base64.b64encode(image.read())
            data = {'pic_data': s.decode('utf-8')}
            with open("config.json", 'r') as load_f:
                load_dict = json.load(load_f)
                url = load_dict["url"]
            try:
                requests.post(url + "humanwarning/", json=data)
            except Exception as e:
                print(e)

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:

            print("file modified:{0}".format(event.src_path))


if __name__ == '__main__':
    # 1 创建服务端套接字对象
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 2 绑定端口
    with open("config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        ip = load_dict["ip"]
        port = load_dict["port"]
        url = load_dict["url"]
        tcp_server.bind((ip, port))
    # 3 设置监听
    tcp_server.listen(128)
    # 4 循环等待客户端连接请求（也就是最多可以同时有128个用户连接到服务器进行通信）

    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "./image", True)
    observer.start()
    try:
        while True:
            tcp_client_1, tcp_client_address = tcp_server.accept()
            # 创建多线程对象
            thd = threading.Thread(target=dispose_client_request, args=(tcp_client_1, tcp_client_address))
            # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
            thd.setDaemon(True)
            # 启动子线程对象
            thd.start()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
