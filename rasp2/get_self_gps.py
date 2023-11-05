# coding: utf-8
# last modified:20230904
# * 获取自身的GPS位置
import serial
import re
from modules.converter_from_wgs84_to_gcj09 import *

utctime = ''
lat = ''
ulat = ''
lon = ''
ulon = ''
numSv = ''
msl = ''
cogt = ''
cogm = ''
sog = ''
kph = ''
gps_t = 0
self_gps = []

# 串口对象
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=3)

# 检查串口是否打开
if ser.isOpen():
    print("GPS Serial Opened! Baudrate=115200")
else:
    print("GPS Serial Open Failed!")

# 将经纬度信息转换成度
def Convert_to_degrees(in_data1, in_data2):
    print(in_data1, in_data2)
    len_data1 = len(in_data1)
    str_data2 = "%05d" % int(in_data2)
    temp_data = int(in_data1)
    symbol = 1
    if temp_data < 0:
        symbol = -1
    degree = int(temp_data / 100.0)
    str_decimal = str(in_data1[len_data1-2]) + str(in_data1[len_data1-1]) + str(str_data2)
    f_degree = int(str_decimal)/60.0/100000.0
    if symbol > 0:
        result = degree + f_degree
    else:
        result = degree - f_degree
    return result

# 读取并解析串口消息
def GPS_read():
    global utctime
    global lat
    global ulat
    global lon
    global ulon
    global numSv
    global msl
    global cogt
    global cogm
    global sog
    global kph
    global gps_t
    if ser.inWaiting():
        if ser.read(1) == b'G':
            if ser.inWaiting():
                if ser.read(1) == b'N':
                    if ser.inWaiting():
                        choice = ser.read(1)
                        if choice == b'G':
                            if ser.inWaiting():
                                if ser.read(1) == b'G':
                                    if ser.inWaiting():
                                        if ser.read(1) == b'A':
                                            #utctime = ser.read(7)
                                            GGA = ser.read(70)
                                            GGA_g = re.findall(r"\w+(?=,)|(?<=,)\w+", str(GGA))
                                            # print(GGA_g)
                                            if len(GGA_g) < 13:
                                                print("GPS no found")
                                                gps_t = 0
                                                return 0
                                            else:
                                                utctime = GGA_g[0]
                                                lat = Convert_to_degrees(str(GGA_g[2]), str(GGA_g[3]))
                                                lon = Convert_to_degrees(str(GGA_g[5]), str(GGA_g[6]))
                                                # trans = LonLatTransfer()
                                                # lon, lat = trans.WGS84_to_BD09(lon, lat)
                                                lon = str(lon)
                                                lat = str(lat)
                                                ulat = GGA_g[4]
                                                ulon = GGA_g[7]
                                                numSv = GGA_g[9]
                                                msl = GGA_g[12]+'.'+GGA_g[13]+GGA_g[14]
                                                #print(GGA_g)
                                                gps_t = 1
                                                return 1
                        elif choice == b'V':
                            if ser.inWaiting():
                                if ser.read(1) == b'T':
                                    if ser.inWaiting():
                                        if ser.read(1) == b'G':
                                            if gps_t == 1:
                                                VTG = ser.read(40)
                                                VTG_g = re.findall(r"\w+(?=,)|(?<=,)\w+", str(VTG))
                                                cogt = VTG_g[0]+'.'+VTG_g[1]+'T'
                                                if VTG_g[3] == 'M':
                                                    cogm = '0.00'
                                                    sog = VTG_g[4]+'.'+VTG_g[5]
                                                    kph = VTG_g[7]+'.'+VTG_g[8]
                                                elif VTG_g[3] != 'M':
                                                    cogm = VTG_g[3]+'.'+VTG_g[4]
                                                    sog = VTG_g[6]+'.'+VTG_g[7]
                                                    kph = VTG_g[9]+'.'+VTG_g[10]
                                            #print(kph)

# ! 方便其他模块调用
def get_gps():
    try:
        while True:
            if GPS_read():
                return float(lat), float(lon)
    except KeyboardInterrupt:
        ser.close()
        print("GPS serial Close!")


if __name__ == "__main__":
    try:
        while True:
            if GPS_read():
                print("*********************")
                print('UTC Time:'+utctime)
                print('Latitude:'+lat+ulat)
                print('Longitude:'+lon+ulon)
                print('Number of satellites:'+numSv)
                print('Altitude:'+msl)
                print('True north heading:'+cogt+'°')
                print('Magnetic north heading:'+cogm+'°')
                print('Ground speed:'+sog+'Kn')
                print('Ground speed:'+kph+'Km/h')
                print("*********************")
    except KeyboardInterrupt:
        ser.close()
        print("GPS serial Close!")
