# jump_player
# 功能
自动玩微信“跳一跳”的python工具
# 基本原理
利用adb获取屏幕信息，利用python下opencv库的模板匹配、边缘提取、水漫法提取跳跃的起点、终点坐标，进而计算跳跃的像素距离，再将其转化为按压时间，最后通过adb控制手机运动。
# 运行环境
* python3.5
* adb, 将源文件中的“/Users/lichzhang/Library/Android/sdk/platform-tools/adb”修改为本机adb路径
* opencv、numpy、matplotlib
