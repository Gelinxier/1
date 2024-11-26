"""
在mission_accomplished函数中直接使用了相对路径获取图片,然后根据此图片匹配当前屏幕上的图像并完成点击操作
任务4 家领取任务奖励的流程如下:
检测是否处于主界面->任务->一键领取->确认奖励
最后通过查找返回主界面的按钮，点击返回，如果程序检测到最后已处于主界面，会打印"任务奖励领取完毕"
该py文件主要用于完成领取任务奖励并最后返回主界面的任务
"""
import pyautogui
import time
import random
from .index_seeking import index_seeking
from .pos_click import seeking, delay_random, locateOnScreen

# 任务4：领取任务奖励
def mission_accomplished(msg_queue=None):
    if index_seeking() == "已处于主界面":
        # 点击任务按钮
        image_path = r'Honkai_automatic\pictures\mission_accomplished\mission.png'
        seeking(image_path, "任务")
        time.sleep(delay_random())

        # 点击一键领取按钮
        image_path = r'Honkai_automatic\pictures\mission_accomplished\receive_all_mission_reward.png'
        seeking(image_path, "一键领取")
        time.sleep(delay_random())

        # 点击确认按钮，这里是在关闭奖励界面
        image_path = r'Honkai_automatic\pictures\mission_accomplished\confirm.png'
        seeking(image_path, "确认奖励")
        time.sleep(delay_random())

        # 领取活跃度水晶奖励
        # 有没有那种从左至右的识别，识别到活跃度的进度条，领取达到进度的奖励

        # 点击主界面按钮
        pos = locateOnScreen(r'Honkai_automatic\pictures\mission_accomplished\index2.png',confidence=0.6)
        if pos:
            left, top, width, height = pos
            rand_x = random.randint(left, left + width)
            rand_y = random.randint(top, top + height)
            pyautogui.moveTo(rand_x, rand_y)
            pyautogui.click(rand_x, rand_y)
            time.sleep(delay_random())
            if index_seeking() == "已处于主界面":
                if msg_queue:
                    msg_queue.put("任务奖励领取完毕")
                else:
                    print("任务奖励领取完毕")
            else:
                if msg_queue:
                    msg_queue.put("发生错误")
                else:
                    print("发生错误")