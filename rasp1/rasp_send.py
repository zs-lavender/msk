# coding: utf-8
# by maorio
# * 个人模式发送给显示端
import get_self_gps
import socket
import time

# 集成了Socket通信常用函数的类
class connect_Raspberry():
    def __init__(self,host,port):
        print("客户端开启")
        # 套接字接口
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置ip和端口

        try:
            self.mySocket.connect((host, port))  #连接到服务器
            print("连接到服务器")
        except:  #连接不成功，运行最初的ip
            print('连接RASP不成功')

    def send(self, gps):
        # 发送消息
        print('1',str(gps[0]), str(gps[1]))
        msg = str(gps[0]) + "#" + str(gps[1])
        # 编码发送
        self.mySocket.send(msg.encode("utf-8"))
        print("成功发送消息")

    def rev(self):
        # 接收消息
        msg = self.mySocket.recv(1024)
        msg = msg.decode('utf-8')
        # 返回确认消息
        print('接收到电脑发送的Ok', msg)
        return msg

    def close(self):
        # 关闭连接
        self.mySocket.close()
        print("与树莓派连接中断\n")
        exit()


# 设置ip和端口(IP为树莓派的IP地址)
myRaspConnection = connect_Raspberry('192.168.63.133', 6667)
print(get_self_gps.get_gps())
myRaspConnection.send(get_self_gps.get_gps())
while True:
    # 在接收到确认信息后再进行下一次发送
    if myRaspConnection.rev():
        time.sleep(1)
        myRaspConnection.send(get_self_gps.get_gps())
    

