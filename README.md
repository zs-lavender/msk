# MSK
多功能智慧码表

## 项目介绍
&nbsp;&nbsp;相较于市面上常见的自行车码表，本款多功能智慧码表在应用需求方面挖掘的更加深入，更加注重朋友、车队此类多人结伴出行的情况。不仅会包括一些运动基础功能，更新颖地会去实现当今市场上所没有的多码表语音通信、地图交互等功能，并将这些功能集中显示在相连的显示屏上。我们所设计的码表会更加强调交互性,这种交互不仅体现于自身与机器的交互,更存在于不同用户之间：所采用的多页面处理更加的智能化,简洁化以及生活化,让人更加赏心悦目；与好友组团出行以及信息通信等原创功能，则更加符合如今万物互联的时代大主题。

## 功能简述

+ 地图路线绘制：绘制用户的骑行路线
+ 多码表语音通信：多码表之间可以进行语音通话，以便骑友在骑行过程中进行实时沟通
+ 多码表地图绘制：展示骑行者的骑行轨迹，使用户能够在地图上看到骑友的位置
+ 运动状态检测：通过传感器检测用户的运动状态

## 工作流程
&nbsp;&nbsp;两个树莓派作为主要信息处理单元，利用py文件分别从GPS模块获取位置信息，从IMU模块获取运动姿态信息，通过socket将两个树莓派所获取信息进行共享，加工与整合，把信息合并后以字符串形式一同传递给绘制地图文件，进行位点标记，存储与轨迹绘制，在显示界面进行该地图展示即可。俩树莓派同时可以通过声卡进行声音采集，转换处理与播放，与命令行一同实现收发模式转换，达成半双工语音通信。

## 使用说明

将三个文件夹下载到本地

### 注意：文件中的绝对路径与ip要修改为本地路径与ip





