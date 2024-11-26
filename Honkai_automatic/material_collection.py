"""
先通过get_image_path函数获取本次任务所需图片的路径
随后在material_collection函数中,先传入图片(截图)路径，再根据此图片匹配屏幕上对应的图像并完成点击操作
完成材料远征的流程如下：
检测是否处于主界面->出击->小的出击按钮->材料远征->一键减负->确认减负->确认奖励
最后通过查找返回主界面的按钮，点击返回，如果程序检测到最后已处于主界面，会打印"材料远征完成"
该py文件主要用于完成材料远征并最后返回主界面的任务
"""
import pyautogui
import time
import random
import os
# import cv2
from .index_seeking import index_seeking
from .pos_click import seeking,delay_random,locateOnScreen

def get_image_path(img_name):
    return os.path.join("Honkai_automatic", "pictures", "material_collection", img_name)

#任务1：材料远征
def material_collection(msg_queue=None):
    #print(index_seeking())
    if index_seeking() == "已处于主界面":
        # 点击出击按钮
        image_path= get_image_path('sortie.png')
        seeking(image_path, "出击", msg_queue=msg_queue)
        time.sleep(delay_random())
        print('XIXI')

        # 点击小的出击按钮
        image_path = get_image_path(r'attack.png')
        seeking(image_path, "小的出击", msg_queue=msg_queue)
        time.sleep(delay_random())

        # 点击材料远征按钮,进入材料远征界面
        image_path = get_image_path('material_collections.png')
        seeking(image_path, "材料远征", msg_queue=msg_queue)
        time.sleep(delay_random())

        # 可以添加的功能：识别用户当前的体力值，判断是否有足够的体力值完成所有远征关卡
        # 识别远征关卡需要的体力值，两者相减，打印出剩余体力值

        # 点击一键减负按钮
        image_path = get_image_path('raids.png')
        seeking(image_path, "一键减负", msg_queue=msg_queue)
        time.sleep(delay_random())

        # 点击确认减负
        # image_path = r'Honkai_automatic\pictures\confirm_raids.png'
        image_path = get_image_path('confirm_raids.png')
        seeking(image_path,"确认减负", click='i', msg_queue=msg_queue)
        time.sleep(delay_random())

        # 点击确认按钮，这里是在关闭奖励界面
        image_path = get_image_path('confirm.png')
        seeking(image_path,"确认奖励", msg_queue=msg_queue)
        time.sleep(delay_random())

        # 点击主界面按钮
        # pos = locateOnScreen(r'Honkai_automatic\pictures\index2.png', confidence=0.8)
        pos = locateOnScreen(get_image_path('index2.png'), confidence=0.8)
        if pos:
            left, top, width, height = pos
            rand_x = random.randint(left, left + width)
            rand_y = random.randint(top, top + height)
            pyautogui.moveTo(rand_x, rand_y)
            pyautogui.click(rand_x, rand_y)
            time.sleep(delay_random())
            if index_seeking() == "已处于主界面":
                if msg_queue:
                    msg_queue.put("已处于主界面，材料远征完成")
                else:
                    print("材料远征完成")
            else:
                if msg_queue:
                    msg_queue.put("发生错误")
                else:
                    print("发生错误")
    else:
        if msg_queue:
            msg_queue.put("未处于主界面")
        else:
            print("未处于主界面")