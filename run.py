import subprocess
import time
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

adb="/Users/lichzhang/Library/Android/sdk/platform-tools/adb"
test_mode = False
test_screen = "screenshot_1514609919.png"
test_screen = "screenshot_1514640400.png"
test_screen = "screenshot_1514644308.png" #小药瓶
test_screen = "screenshot_1514644687.png" #图片未加载完毕
test_screen = "screenshot_1514648118.png" 
test_screen = "screenshot_1514640998.png" #圆柱体
test_screen = "screenshot_1514682807.png" 
test_screen = "screenshot_1514691372.png" 

def run_cmd(cmd):
    return subprocess.getstatusoutput(cmd) 


def touch(x, y):
    cmd = adb + " shell input tap %d %d" % (x, y)
    run_cmd(cmd)


def swipe(x, y, nx, ny, t):
    cmd = adb + " shell input swipe %d %d %d %d %d" % (x, y, nx, ny, t)
    run_cmd(cmd)



#得到屏幕截屏
def get_capture():
    time_now = int(time.time())
    cmd = "mv ./screenshot.png ./screenshot_%d.png" %  time_now
    run_cmd(cmd)
    cmd = adb + " shell /system/bin/screencap -p /sdcard/screenshot.png"
    run_cmd(cmd)
    cmd = adb + " pull /sdcard/screenshot.png ./"
    run_cmd(cmd)


def find_p():
    p = cv2.imread("p.png", 1)
    screen = cv2.imread("screenshot.png", 1)
    if test_mode == True:
        screen = cv2.imread(test_screen, 1)
    result=cv2.matchTemplate(screen, p, cv2.TM_CCOEFF_NORMED)

    (height, width, n)=p.shape
    (min_val, max_val, minimumLocation, maximumLocation) = cv2.minMaxLoc(result)
    top_left = maximumLocation
    bottom_right = ((top_left[0] + width), (top_left[1] + height))
    print(top_left, bottom_right, min_val, max_val)

    res_x = (top_left[0] + bottom_right[0]) / 2
    res_y = bottom_right[1] - 20

    if test_mode == True:
        plt.figure(0)
        plt.imshow(screen)
        x=[top_left[0], bottom_right[0]]
        y=[top_left[1], bottom_right[1]]
        plt.plot(x, y)
        plt.plot([res_x], [res_y], "r*") 
        plt.show()

    

    if max_val < 0.6:
        return False, res_x, res_y
    else:
        return True, res_x, res_y


def is_over():
    p = cv2.imread("again.png", 1)
    screen = cv2.imread("screenshot.png", 1)
    if test_mode == True:
        screen = cv2.imread(test_screen, 1)
    result=cv2.matchTemplate(screen, p, cv2.TM_CCOEFF_NORMED)

    (height, width, n)=p.shape
    (min_val, max_val, minimumLocation, maximumLocation) = cv2.minMaxLoc(result)
    top_left = maximumLocation
    bottom_right = ((top_left[0] + width), (top_left[1] + height))

    #print(top_left, bottom_right, min_val, max_val)

    if test_mode == True:
        plt.figure(0)
        plt.imshow(screen)
        x=[top_left[0], bottom_right[0]]
        y=[top_left[1], bottom_right[1]]
        plt.plot(x, y)
        plt.show()

    x = (top_left[0] + bottom_right[0]) / 2
    y = bottom_right[1] - 20

    if max_val > 0.5:
        touch(x, y)
        return True
    else:
        return False

def find_target(px = 0):
    img = cv2.imread("screenshot.png", 1)
    if test_mode == True:
        img = cv2.imread(test_screen, 1)


    img = cv2.GaussianBlur(img,(9,9),0)  
    #img = cv2.GaussianBlur(img,(3,3),0)  

    canny = cv2.Canny(img, 5, 15) 

    if test_mode == True:
        plt.figure(0)
        plt.imshow(canny) 
        plt.show() 
    
    #下面开始找像素点
    rx = 0
    ry = 0
    size = canny.shape
    find = False
    bg_color = canny[100, 100]
    for y in range(500, size[0]):
        for x in range(size[1]): 
            if bg_color != canny[y, x]:
                if px > 0: 
                    if abs(x - px) < 100:
                        #距离小人的x坐标太近，跳过
                        continue
                find = True
                print(x, y)
                rx = x
                ry = y
                print(canny[y, x])
                break

        if find == True:
            break
    
    #开始修补缝隙
    print (size)
    count = 4
    start_x = rx - 500
    if start_x < count: 
        start_x = count

    end_x = rx + 500
    if end_x > size[1] - count - 1:
        end_x = size[1] - count - 1

    start_y = ry
    end_y = ry + 500
    if end_y > size[0] - count - 1:
        end_y = size[0] - count - 1

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if canny[y, x] == 255: 
                #开始向外扩散
                for i in range(-count, count + 1):
                    for j in range(-count, count + 1):
                        if i == 0 and j == 0:
                            continue
                        canny[y + j, x + i] = 125
    ry = ry + 70
    
    count = 10 
    succ = True
    if canny[ry, rx] != 0:
        succ = False
        #说明这个点处在轮廓上, 需要修正
        for i in range(-count, count + 1):
            for j in range(-count, count + 1):
                if canny[ry + j, rx + i] == 0:
                    ry = ry + j
                    rx = rx + i
                    succ = True
                    break
            if succ == True:
                break
    
     

    if test_mode == True:
        plt.figure(0)
        plt.imshow(canny) 
        plt.plot([rx], [ry], "r*") 
        plt.show()

    #下面根据水漫金山大法确定中心点
    mask = None 
    seed_pt = rx, ry
    #lo = cv2.cvScalar(10, 10, 10, 10)
    #hi = (10, 10, 10)
    flags = 4
    retval, canny, mask, rect = cv2.floodFill(canny, mask, seed_pt, (255, 0, 0))

    new_x = rect[0] + rect[2] / 2
    new_y = rect[1] + rect[3] / 2

    if succ == False:
        new_x = rx
        new_y = ry 
        print("succ False, so use rx ry")

    if test_mode == True:
        plt.figure(0)
        plt.imshow(canny) 
        plt.plot([rx], [ry], "r*") 
        plt.plot([new_x], [new_y], "b*") 
        plt.show()

    if rx < 100 or rx > size[1] - 100:
        #距离边缘太近，就重新尝试
        find = False
    print("rx ry:", rx, ry)
        
    if find == True:
        return True, new_x, new_y
        #return True, rx, ry
    else:
        return False, 0, 0


if __name__ == "__main__":
    

    if test_mode == True:
        res, sx, sy = find_p()
        res1, tx, ty = find_target(sx)
        dis = math.sqrt((sx - tx) * (sx - tx) + (sy - ty) * (sy - ty))
        print(res, sx, sy, res1, tx, ty)
        print("Dis:%d" % dis)
        sys.exit(0) 
        
    try_count = 0
    while True: 
        print ("\n\n\n")
        get_capture()
        if is_over() == True:
            time.sleep(1)
            print ("New Game !")
            continue
        
        res1, sx, sy = find_p()
        res2, tx, ty = find_target(sx)

        if res1 == False:
            print("Reco Person Error! Try Again")
            time.sleep(0.5)
            continue

        if res2 == False:
            print("Reco Target Error! Try Again")
            time.sleep(0.5)
            continue 

        dis = math.sqrt((sx - tx) * (sx - tx) + (sy - ty) * (sy - ty))
        print("Distance:%d" % dis)

        if dis < 300 and try_count < 3: 
            #最多确认三次
            try_count = try_count + 1 
            print("Distance Too Small, Check Again:%d" % try_count)
        else:
            w = 0.9
            if dis < 400:
                w = 0.85
            elif dis < 600:
                w = 0.9
            elif dis < 800:
                w = 0.92
            else:
                w = 0.95
            #w = 1  mate9
            w = 0.93
            t = dis * w
            swipe(250, 250, 251, 251, t)
            try_count = 0
            print ("Touch Time:%f" % t)
        time.sleep(0.7)

    sys.exit(0)

    t = 100
    if len(sys.argv) > 1:
        t = int(sys.argv[1])

    swipe(250, 250, 251, 251, t)
    sys.exit(0)
    for i in range(10):
        touch(100, 100) 
        time.sleep(0.1)

