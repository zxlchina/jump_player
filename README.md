# jump_player
# 功能
自动玩微信“跳一跳”的python工具
# 基本原理
* 利用adb获取屏幕信息
* 利用python下opencv库的模板匹配、边缘提取、水漫法提取跳跃的起点、终点坐标
* 计算跳跃的像素距离，再将其转化为按压时间
* 最后通过adb控制手机运动。

这里重点说下第二步骤，获取起点、终点坐标

**1、模板匹配，获得小人的位置，做固定偏移即可得到起点，如图红星所示**
![Aaron Swartz](https://github.com/zxlchina/jump_player/blob/master/508CDF03-EAA6-4952-B387-61A95E577729.png)

**2、边缘提取，从上往下扫描，得到顶点坐标**
![Aaron Swartz](https://github.com/zxlchina/jump_player/blob/master/9E7D0C46-81B1-44F4-B808-F45FF99D6C9B.png)

**3、对边缘做扩散，防止有小的缝隙，并得到顶点向下偏移一定值的种子坐标，如图红星所示**
![Aaron Swartz](https://github.com/zxlchina/jump_player/blob/master/E96D519C-B379-4325-A0DA-7EA3754E9D3D.png)

**4、以种子点为基础，用漫水法得到连通区域，并计算区域的中心点，为目标点，如图蓝星所示**
![Aaron Swartz](https://raw.githubusercontent.com/zxlchina/jump_player/master/100B1AE6-C50E-4A9F-B8DE-ED9692552822.png)

# 运行环境
* python3.5
* adb, 将源文件中的“/Users/lichzhang/Library/Android/sdk/platform-tools/adb”修改为本机adb路径
* opencv、numpy、matplotlib
