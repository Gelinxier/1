"""
该py文件具体实现步骤与任务1类似,只是任务1将图片路径的获取单独写了一个函数,
而在homeland函数中直接使用了相对路径获取图片,再用seeking函数匹配屏幕上对应的图像并点击
任务2 家园打工的流程如下:
检测是否处于主界面->家园->领取金币->家园打工->一键打工->确认打工->领取奖励->确认奖励'
最后通过执行两次匹配点击返回按钮返回主界面
该py文件主要用于实现家园打工并最后返回主界面的任务
"""
import pyautogui
import time
import random
import os
from .index_seeking import index_seeking
from .pos_click import seeking,delay_random, locateOnScreen

def get_image_path(img_name):
    return os.path.join("Honkai_automatic","pictures", 'homeland', img_name)

# 任务2：家园打工
def homeland(msg_queue=None):
    print(index_seeking())
    if index_seeking() == "已处于主界面":
        # 点击家园按钮
        # image_path = r'Honkai_automatic\pictures\homeland.png'
        image_path = get_image_path('homeland.png')
        seeking(image_path, "家园")
        time.sleep(delay_random())

        # 点击金币采集按钮
        # image_path = r'Honkai_automatic\pictures\collect.png'
        image_path = get_image_path('collect.png')
        seeking(image_path, "金币")
        time.sleep(delay_random())

        # 点击家园打工按钮
        # image_path = r'Honkai_automatic\pictures\work.png'
        image_path = get_image_path('work.png')
        seeking(image_path, "家园打工")
        time.sleep(delay_random())

        # 点击一键打工按钮
        # image_path = r'Honkai_automatic\pictures\arrangement.png'
        image_path = get_image_path('arrangement.png')
        seeking(image_path, "一键打工")
        time.sleep(delay_random())

        # 点击确认打工按钮
        # image_path = r'Honkai_automatic\pictures\confirm_arrangement.png'
        image_path = get_image_path('confirm_arrangement.png')
        seeking(image_path, "确认打工")
        time.sleep(delay_random())

        # 点击领取奖励按钮
        # image_path = r'Honkai_automatic\pictures\receive_homeland.png'
        image_path = get_image_path('receive_homeland.png')
        seeking(image_path, "领取奖励",click = 'i')
        time.sleep(delay_random())

        # 点击确认奖励按钮，这里是在关闭奖励界面
        # image_path = r'Honkai_automatic\pictures\confirm.png'
        image_path = get_image_path('confirm.png')
        seeking(image_path, "确认奖励")
        time.sleep(delay_random())

        # 可以添加的功能：进入家园远征界面，识别用户当前的体力值，并远征相应数量的指定关卡
        # 并领取已经完成的远征奖励

        # 点击返回按钮，家园界面没有主菜单按钮，点击返回操作两次之后即可返回主界面
        for i in range(2):
            # pos = locateOnScreen(r'Honkai_automatic\pictures\back.png', confidence=0.8)
            pos = locateOnScreen(get_image_path('back.png'), confidence=0.8)
            if pos:
                left, top, width, height = pos
                rand_x = random.randint(left, left + width)
                rand_y = random.randint(top, top + height)
                pyautogui.moveTo(rand_x, rand_y)
                pyautogui.click(rand_x, rand_y)
                time.sleep(delay_random())
        if index_seeking() == "已处于主界面":
            if msg_queue:
                msg_queue.put("家园任务完成，已处于主界面")
            else:
                print("家园任务完成，已处于主界面")
        else:
            if msg_queue:
                msg_queue.put("未处于主界面")
            else:
                print("未处于主界面")