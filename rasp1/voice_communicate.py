# coding: utf-8
# by ljc
# * 语音通信
import subprocess
import multiprocessing


# 发送进程
def send_process(command):
    print("Currently on the send end")
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        print(line)

# 接收进程
def recv_process(command):
    print("Currently on the recv end")
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        print(line)

def card_get():
    p = subprocess.Popen('arecord -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        if len(line) > 60:
            for i in line:
                if i>48 and i<=57:
                    return i-48
                
if __name__ == "__main__":
    command1 = "arecord -D plughw:" + str(card_get()) + ",0 -t wav -f cd -r 8000 | nc 192.168.137.237 8888"
    command2 = "nc -l -p 8888 | aplay"
    # 定义进程
    send_proc = multiprocessing.Process(target=send_process,args = (command1,))
    recv_proc = multiprocessing.Process(target=recv_process,args = (command2,))
    recv_proc.start()
    # 接收模式还是发送模式
    while True:
        line = input("plz input your choice:\n")
        if line.lower() == "s":
            recv_proc.terminate()  
            send_proc = multiprocessing.Process(target=send_process,args = (command1,))
            send_proc.start()
            print("recv end closed, send end opened")

        elif line.lower() == "q":
            send_proc.terminate()  
            recv_proc = multiprocessing.Process(target=recv_process,args = (command2,))
            recv_proc.start()
            print("send end closed, recv end opened")

        else:
            print("plz input the right choice!")
