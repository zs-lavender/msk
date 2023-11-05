# coding: utf-8
# by maorio
# * 个人模式显示端接收消息
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl
import socket
import math

# 实时地图类
# * 内含初始化、生成HTML文件、解析信息和更新地图
class RealTimeMapApp(QMainWindow):
    def __init__(self):
        super(RealTimeMapApp, self).__init__()
        self.setWindowTitle('实时地图轨迹')
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.qwebengine = QWebEngineView(self)
        layout.addWidget(self.qwebengine)

        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)
        # 加载HTML
        self.qwebengine.setHtml(self.generate_map_html(),
                                baseUrl=QUrl.fromLocalFile('.'))

        self.new_point = None
        self.old_point = None
        self.old_label = None  # 用于保存旧点的经纬度标签对象

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(1000)  # 每秒更新一次地图

    def generate_map_html(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Real-time Map</title>
            <style>
                body, html, #map {
                    height: 100%;
                    margin: 0;
                }
            </style>
            <!-- 引入 Leaflet 的 CSS 和 JavaScript 文件 -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css">
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        </head>
        <body>
            <div id="map" style="width: 100%; height: 100vh;"></div>
            <script>
                var mymap = L.map('map').setView([39.962, 116.35], 18);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(mymap);
                var pathMarkers = L.layerGroup().addTo(mymap);

                var newMarkerIcon = L.icon({
                    iconUrl: 'C:/Users/23185/Desktop/gui/pic.png',  // 用于新的轨迹点（注意修改路径）
                    iconSize: [32, 32],
                    iconAnchor: [8, 8]
                });

                var oldMarkerOptions = {
                    radius: 5,
                    fillColor: 'blue',
                    color: 'blue',
                    fillOpacity: 1
                };

                var oldMarker;  // 声明在外部以持久保存旧点的图标对象

                function addPoint(lat, lng, speed, isNew) {
                    var latlng = new L.LatLng(lat, lng);
                    if (isNew) {
                        if (oldMarker) {
                            pathMarkers.removeLayer(oldMarker);  // 删除旧点的图标
                            mymap.removeLayer(oldLabel);  // 删除旧点的经纬度标签
                        }
                        oldMarker = L.marker(latlng, { icon: newMarkerIcon }).addTo(pathMarkers);
                        var label = L.divIcon({
                        className: 'label',
                        html: `<div style="white-space: nowrap; margin-left: 1em;">Lat: ${lat.toFixed(5)} Lng: ${lng.toFixed(5)}</div><div style="white-space: nowrap; margin-left: 1em;">Speed: ${speed.toFixed(3)}m/s</div>`
                        });
                        var newLabel = L.marker(latlng, { icon: label }).addTo(pathMarkers);
                        oldLabel = newLabel;  // 保存旧点的经纬度标签对象
                    } else {
                        var marker = L.circleMarker(latlng, oldMarkerOptions).addTo(pathMarkers);
                    }
                    mymap.panTo(latlng);
                }
            </script>
        </body>
        </html>
        """
        return html


    # 速度计算
    def haversine_distance(self, new, old):
        # 地球半径
        R = 6371 
        # 经纬度
        lat1 = math.radians(new[0])
        lon1 = math.radians(new[1])
        lat2 = math.radians(old[0])
        lon2 = math.radians(old[1])
        # 经纬度差
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # 公式
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        # 计算速度并转换单位
        return c * R * 1000

    # 更新地图
    def update_map(self):
        # print(self.get_gps(client))
        if self.get_gps(client).count("#") == 1:
            lat, lon = self.get_gps(client).split("#")
            new_point = [round(float(lat), 5), round(float(lon), 5)]
            if self.new_point is not None:
                self.old_point = self.new_point  # 保存上一个新点的坐标
            self.new_point = new_point

            if self.new_point != None and self.old_point != None:
                # 使用 JavaScript 添加新的轨迹点到地图上x
                javascript = f"addPoint({new_point[0]}, {new_point[1]}, {self.haversine_distance(new_point, self.old_point)}, true);"
                self.qwebengine.page().runJavaScript(javascript)

            if self.old_point is not None:
                # 使用 JavaScript 添加旧的轨迹点到地图上，并连接成线
                lineCoordinates = "[[" + \
                    f"{self.old_point[0]},{self.old_point[1]}], [{new_point[0]},{new_point[1]}]]"
                javascript = f"var line = L.polyline({lineCoordinates}, {{color: 'red'}}).addTo(mymap);"
                self.qwebengine.page().runJavaScript(javascript)
        else:
            pass
    
    # 接收消息并返回确认消息
    def get_gps(self, client):
        msg = 0
        msg = client.recv(1024)
        msg = msg.decode("utf-8")
        if msg != "":
            print(msg)
            client.send('Ok'.encode("utf-8"))
            print("读取完成, 并回复OK")
            return msg


global client

if __name__ == '__main__':
    print("服务开启")
    # 建立通信
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.63.133"
    port = 6667
    mySocket.bind((host, port))
    mySocket.listen(10)
    client = None
    while client == None:
        print("等待连接")
        client, address = mySocket.accept()
        print("新连接")
        print("IP is %s" % address[0])
        print("port is %d\n" % address[1])
        print(client)
    app = QApplication(sys.argv)
    win = RealTimeMapApp()
    win.show()
    sys.exit(app.exec_())
