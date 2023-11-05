# coding: utf-8
# by zs
# * 显示模块
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QProcess, QTimer
import subprocess
from PyQt5 import QtCore
from datetime import datetime
import requests
import sys


class mywindow1(QWidget):
    def __init__(self):
        super().__init__()
        self.mystack()
        self.init()

    def mystack(self):
        self.stacklayout = QStackedLayout()
        win2 = mywindow2()
        win3 = mywindow3()
        win4 = mywindow4()  # 新的窗口用于运行本地Python文件
        self.stacklayout.addWidget(win2)
        self.stacklayout.addWidget(win3)
        self.stacklayout.addWidget(win4)  # 将新的窗口添加到抽屉布局

    def init(self):
        container = QVBoxLayout()
        self.setFixedSize(800, 1000)
        widget = QWidget()
        widget.setLayout(self.stacklayout)

        btn1 = QPushButton('主页')
        btn1.clicked.connect(self.btn1_click)
        # 创建一个新的字体
        font = QFont()
        font.setPointSize(18)  # 设置字号
        font.setBold(True)     # 设置加粗
        font.setFamily("楷体")  # 设置字体
        # 设置按钮的字体
        btn1.setFont(font)
        btn2 = QPushButton('个人模式')
        btn2.clicked.connect(self.btn2_click)

        # 设置按钮的字体
        btn2.setFont(font)
        btn3 = QPushButton('小队模式')
        btn3.clicked.connect(self.btn3_click)

        btn3.setFont(font)
        # 添加显示北京时间的标签
        self.time_label = QLabel(self)
        container.addWidget(self.time_label)
        # 添加显示天气温度的标签
        self.weather_label = QLabel(self)
        container.addWidget(self.weather_label)
        container.addWidget(widget)
        container.addWidget(btn1)
        container.addWidget(btn2)
        container.addWidget(btn3)
        self.setLayout(container)
        # 用你的图片路径替换"path_to_your_image.jpg"
        background_pixmap = QPixmap("C:/Users/23185/Desktop/gui/back.jpg")
        background_brush = QBrush(background_pixmap)
        palette = QPalette()
        palette.setBrush(QPalette.Window, background_brush)
        self.setPalette(palette)
        button_style = "background-color: transparent;color:white"  # 将按钮的背景设置为透明
        btn1.setStyleSheet(button_style)
        btn2.setStyleSheet(button_style)
        btn3.setStyleSheet(button_style)

    def btn1_click(self):
        self.stacklayout.setCurrentIndex(0)
        self.update_beijing_time()

    def btn2_click(self):
        self.stacklayout.setCurrentIndex(1)

    def btn3_click(self):
        self.stacklayout.setCurrentIndex(2)  # 切换到第三个窗口，即新的窗口

    def update_beijing_time(self):
        # 获取当前北京时间
        beijing_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        font = QFont()
        font.setItalic(True)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setText(f'北京时间: {beijing_time}')

    def update_weather_info(self):
        try:
            # 使用OpenWeatherMap API获取北京天气信息
            api_key = 'fef968708d9e9f030941fc0120079b13'  # 替换为您的API密钥
            city = 'Beijing'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

            response = requests.get(url)
            data = response.json()

            if 'main' in data and 'temp' in data['main']:
                temperature = data['main']['temp']
                font = QFont()
                font.setItalic(True)
                self.weather_label.setFont(font)
                self.weather_label.setStyleSheet("color: white;")
                self.weather_label.setText(f'北京温度: {temperature}°C')
            else:
                self.weather_label.setText('无法获取天气信息')
        except Exception as e:
            print("获取天气信息时发生错误:", str(e))


class mywindow2(QWidget):
    def __init__(self):
        super().__init__()
        layout1 = QVBoxLayout()
        label = QLabel('码赛客')
        font = QFont()
        font.setPointSize(24)  # 设置字号
        font.setBold(True)     # 设置加粗
        font.setFamily("楷体")  # 设置字体
        label.setStyleSheet("color: white;")
        label.setFont(font)
       # layout1.addStretch(1)
        layout1.addWidget(label)
       # layout1.addStretch(1)
        layout1.setAlignment(label, QtCore.Qt.AlignHCenter)
        self.setLayout(layout1)


class mywindow3(QWidget):
    def __init__(self):
        super().__init__()
        layout1 = QVBoxLayout()
        self.setLayout(layout1)
        self.run_python_file_button1 = QPushButton('开始个人冒险', self)
        self.run_python_file_button1.clicked.connect(
            self.run_local_python_file_man)
        button_style = "background-color: transparent;color:white"  # 将按钮的背景设置为透明
        self.run_python_file_button1.setStyleSheet(button_style)
        font = QFont()
        font.setPointSize(18)  # 设置字号
        font.setBold(True)     # 设置加粗
        font.setFamily("楷体")  # 设置字体
        # 设置按钮的字体
        self.run_python_file_button1.setFont(font)
        layout1.addWidget(self.run_python_file_button1)

    def run_local_python_file_man(self):
        try:
            file_path = "./test.py"
            subprocess.Popen(["python", file_path])
        except Exception as e:
            print("发生错误:", str(e))


class mywindow4(QWidget):  # 新的窗口用于运行本地Python文件
    def __init__(self):
        super().__init__()
        layout1 = QVBoxLayout()
        self.setLayout(layout1)

        self.run_python_file_button = QPushButton('开始团队冒险', self)
        self.run_python_file_button.clicked.connect(
            self.run_local_python_file_all)
        button_style = "background-color: transparent;color:white"  # 将按钮的背景设置为透明
        self.run_python_file_button.setStyleSheet(button_style)
        font = QFont()
        font.setPointSize(18)  # 设置字号
        font.setBold(True)     # 设置加粗
        font.setFamily("楷体")  # 设置字体
        # 设置按钮的字体
        self.run_python_file_button.setFont(font)
        layout1.addWidget(self.run_python_file_button)
        # self.run_python_file_button12 = QPushButton('开始通话', self)
        # self.run_python_file_button12.clicked.connect(self.run_local_python_file_allmansound)
       # layout1.addWidget(self.run_python_file_button12)

    def run_local_python_file_all(self):
        self.run_local_python_file_allman()
        self.run_local_python_file_allmansound()

    def run_local_python_file_allman(self):
        try:
            file_path = "./testtry2.py"
            subprocess.Popen(["python", file_path])
        except Exception as e:
            print("发生错误:", str(e))

    def run_local_python_file_allmansound(self):
        try:
            file_path = "C:/Users/Administrator/Desktop/say.py"
            subprocess.Popen(["python", file_path])
        except Exception as e:
            print("发生错误:", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mywindow1()
    w.show()
    # 使用定时器每秒更新一次北京时间
    timer = QTimer()
    timer.timeout.connect(w.update_beijing_time)
    timer.timeout.connect(w.update_weather_info)
    timer.start(1000)  # 1000毫秒 = 1秒
    sys.exit(app.exec_())
