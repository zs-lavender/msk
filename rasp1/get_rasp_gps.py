# created on 9.4
# to get data of raspiberry's GPS
# by maorio
# -*- coding:utf-8 -*-
import socket

 
# ! 方便其它模块调用
# * 参数 客户端
# * 返回 接收到的信息
# * 接收其他树莓派发送的消息并解析，返回一个确认消息给发送端
def get_gps(client):
        msg = 0
        msg = client.recv(1024)
        msg = msg.decode("utf-8")
        if msg != "":
            print("rasp",msg)
            message = msg.split("#")
            client.send('OK'.encode('utf-8'))
            return tuple(message)
    
    
if __name__ == "__main__":
    # 套接字
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # IP地址和端口
    host = "192.168.137.100"
    port = 1234
    mySocket.bind((host, port))
    # 支持最多连接数
    mySocket.listen(10)
    
    client = None
    while client == None:
        print("等待连接")
        client, address = mySocket.accept()
        print("新连接")
        print("IP is %s" % address[0])
        print("port is %d\n" % address[1])
        print(client)
    while True:
        get_gps(client)
    mySocket.close()


