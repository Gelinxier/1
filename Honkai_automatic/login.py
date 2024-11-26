"""
login函数将先在崩坏三主界面匹配"点击任意处进入游戏",匹配成功后会在目标图像内随机生成一处坐标,
鼠标会先移动至这处坐标，然后进行点击操作
后面的每日签到领取，签到确定均是如此
完成每个操作中间都会有一些时间的间隔
最后还有一个可能性的任务，如果有活动界面弹出，程序会识别屏幕上是否有"X"的图标，进行关闭操作，
如果没有识别到"X",则跳过本次操作，当这一套操作走完后，会打印"自动登录功能结束"
该py文件主要用于完成自动登录,签到奖励领取的任务
"""
import pyautogui
import time
import os
from .pos_click import seeking, locateOnScreen


def get_image_path(img_name):
    return os.path.join("Honkai_automatic", "pictures", 'login', img_name)

# 登录
def login(msg_queue=None):
    # 点击登录按钮
    # image_path = r'Houkai_automatic\pictures\TapToLogin.png'
    image_path = get_image_path('TapToLogin.png')
    seeking(image_path,"自动登录")
    if msg_queue:
        msg_queue.put('Capital on the bridge!')
    else:
        print('Capital on the bridge!')
    time.sleep(8)
    # 自动签到领取奖励
    # 可以添加的功能：识别签到奖励并提示用户明日签到奖励（将领取界面的截图和图片库进行匹配）
    image_path = get_image_path('receive_sign_in_reward.png')  #领取
    seeking(image_path,"领取签到奖励")
    time.sleep(5)
    image_path = get_image_path('sign_in_confirm.png')  #签到确定
    seeking(image_path,"签到确定")
    time.sleep(5)

    # 关闭游戏活动窗口
    # 可以添加的功能：识别当前正在进行的活动（使用文字识别技术）
    location = locateOnScreen(get_image_path('close.png'), confidence=0.8) #X
    if location:
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        pyautogui.click(center)

    time.sleep(3)
    print("自动登录功能结束")
    #点击任意处即可关闭该页面，这里先不写