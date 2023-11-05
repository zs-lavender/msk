# coding: utf-8
# by maorio
# * 小队模式显示端接收消息
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl
import socket


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

        self.new_point1 = None
        self.old_point1 = None
        self.new_point2 = None
        self.old_point2 = None
        self.old_label1 = None  # 用于保存旧点的经纬度标签对象
        self.old_label2 = None

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

                var oldMarker1;  // 声明在外部以持久保存第一个旧点的图标对象
                var oldMarker2;  // 声明在外部以持久保存第二个旧点的图标对象

                function addPoint(lat, lng, isNew, index) {
                    var latlng = new L.LatLng(lat, lng);
                    if (isNew) {
                        if (index === 1) {
                            if (oldMarker1) {
                                pathMarkers.removeLayer(oldMarker1);  // 删除第一个旧点的图标
                                mymap.removeLayer(oldLabel1);  // 删除第一个旧点的经纬度标签
                            }
                            oldMarker1 = L.marker(latlng, { icon: newMarkerIcon }).addTo(pathMarkers);
                            var label = L.divIcon({
                                className: 'label',
                                html: `<div style="white-space: nowrap; margin-left: 1em;">Lat: ${lat.toFixed(7)} Lng: ${lng.toFixed(7)}</div>`
                            });
                            var newLabel = L.marker(latlng, { icon: label }).addTo(pathMarkers);
                            oldLabel1 = newLabel;  // 保存第一个旧点的经纬度标签对象
                        } else {
                            if (oldMarker2) {
                                pathMarkers.removeLayer(oldMarker2);  // 删除第二个旧点的图标
                                mymap.removeLayer(oldLabel2);  // 删除第二个旧点的经纬度标签
                            }
                            oldMarker2 = L.marker(latlng, { icon: newMarkerIcon }).addTo(pathMarkers);
                            var label = L.divIcon({
                                className: 'label',
                                html: `<div style="white-space: nowrap; margin-left: 1em;">Lat: ${lat.toFixed(7)} Lng: ${lng.toFixed(7)}</div>`
                            });
                            var newLabel = L.marker(latlng, { icon: label }).addTo(pathMarkers);
                            oldLabel2 = newLabel;  // 保存第二个旧点的经纬度标签对象
                        }
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
    

    # 更新地图
    def update_map(self):
        if self.get_gps(client).count("&&") == 1:
            gps1, gps2 = self.get_gps(client).split("&&")
            lat1, lon1 = gps1.split("#")
            lat2, lon2 = gps2.split("#")
            new_point1 = [round(float(lat1), 5), round(float(lon1), 5)]
            new_point2 = [round(float(lat2), 5), round(float(lon2), 5)]

            if self.new_point1 is not None:
                self.old_point1 = self.new_point1  # 保存上一个新点的坐标
            self.new_point1 = new_point1

            if self.new_point2 is not None:
                self.old_point2 = self.new_point2  # 保存上一个新点的坐标
            self.new_point2 = new_point2

            # 使用 JavaScript 添加新的轨迹点到地图上
            javascript1 = f"addPoint({new_point1[0]}, {new_point1[1]}, true, 1);"
            self.qwebengine.page().runJavaScript(javascript1)

            if self.old_point1 is not None:
                # 使用 JavaScript 添加旧的轨迹点到地图上，并连接成线
                lineCoordinates1 = "[[" + \
                    f"{self.old_point1[0]},{self.old_point1[1]}], [{new_point1[0]},{new_point1[1]}]]"
                javascript1 = f"var line = L.polyline({lineCoordinates1}, {{color: 'red'}}).addTo(mymap);"
                self.qwebengine.page().runJavaScript(javascript1)

            # 使用 JavaScript 添加新的轨迹点到地图上
            javascript2 = f"addPoint({new_point2[0]}, {new_point2[1]}, true, 2);"
            self.qwebengine.page().runJavaScript(javascript2)

            if self.old_point2 is not None:
                # 使用 JavaScript 添加旧的轨迹点到地图上，并连接成线
                lineCoordinates2 = "[[" + \
                    f"{self.old_point2[0]},{self.old_point2[1]}], [{new_point2[0]},{new_point2[1]}]]"
                javascript2 = f"var line = L.polyline({lineCoordinates2}, {{color: 'blue'}}).addTo(mymap);"
                self.qwebengine.page().runJavaScript(javascript2)
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
    # 建立通信
    print("服务开启")
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.137.1"
    port = 2581
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
