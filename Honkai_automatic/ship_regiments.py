"""
在ship_regiments函数中直接使用了相对路径获取图片,然后根据此图片匹配当前屏幕上的图像并完成点击操作
任务3 家领取任务奖励的流程如下:
检测是否处于主界面->舰团->委托回收->申请新委托->接受->循环8次提交材料过程->舰团奖池->领取->确认领取
最后通过查找返回主界面的按钮，点击返回，如果程序检测到最后已处于主界面，会打印"舰团任务完成"
该py文件主要用于完成舰团委托并最后返回主界面的任务
"""
import pyautogui
import time
import random
from .index_seeking import index_seeking
from .pos_click import seeking, delay_random, locateOnScreen

# 任务3：舰团委托
def ship_regiments(msg_queue=None):
    if index_seeking() == "已处于主界面":
        # 点击舰团按钮
        image_path = r'Honkai_automatic\pictures\index_seeking\Ship_regiments.png'
        seeking(image_path, "舰团")
        time.sleep(delay_random())

        # 点击委托回收按钮
        # image_path = r'pictures\entrust.png'
        # seeking(image_path, "委托回收/委托已完成")
        pos = locateOnScreen(r'Honkai_automatic\pictures\ship_regiments\entrust.png', confidence=0.6)
        if pos:
            left, top, width, height = pos
            rand_x = random.randint(left, left + width)
            rand_y = random.randint(top, top + height)
            pyautogui.moveTo(rand_x, rand_y)
            pyautogui.click(rand_x, rand_y)
            time.sleep(delay_random())
        else:
            if msg_queue:
                msg_queue.put("未找到委托回收按钮，或者委托已完成")
            else:
                print("未找到委托回收按钮，或者委托已完成")

        # 申请新委托
        image_path = r'Honkai_automatic\pictures\ship_regiments\apply.png'
        seeking(image_path, "申请新委托")
        time.sleep(delay_random())

        # 点击接受按钮
        image_path = r'Honkai_automatic\pictures\ship_regiments\accept.png'
        seeking(image_path, "接受")
        time.sleep(delay_random())

        # 开始提交委托材料
        flag= True
        num = 0
        while flag:
            # 点击提交按钮，需要点两次不同的提交，再点放入舰团奖励池
            # 这里还需要做灰色提交按钮判断
            num += 1
            if msg_queue:
                msg_queue.put(f"第{num}次提交委托材料")
            else:
                print(f"第{num}次提交委托材料")  
            pos = locateOnScreen(r'Honkai_automatic\pictures\ship_regiments\submit1.png', confidence=0.6)
            if pos:
                left, top, width, height = pos
                rand_x = random.randint(left, left + width)
                rand_y = random.randint(top, top + height)
                pyautogui.moveTo(rand_x, rand_y)
                pyautogui.click(rand_x, rand_y)
                time.sleep(delay_random())
                pos = locateOnScreen(r'Honkai_automatic\pictures\ship_regiments\submit2.png', confidence=0.6)
                if pos:
                    left, top, width, height = pos
                    rand_x = random.randint(left, left + width)
                    rand_y = random.randint(top, top + height)
                    pyautogui.moveTo(rand_x, rand_y)
                    pyautogui.click(rand_x, rand_y)
                    time.sleep(delay_random())
                    pos = locateOnScreen(r'Honkai_automatic\pictures\ship_regiments\additions.png', confidence=0.6)
                    if pos:
                        left, top, width, height = pos
                        rand_x = random.randint(left, left + width)
                        rand_y = random.randint(top, top + height)
                        pyautogui.moveTo(rand_x, rand_y)
                        pyautogui.click(rand_x, rand_y)
                        time.sleep(delay_random())

            if num == 8:
                flag = False


        # 开始领取舰团奖池
        image_path = r'Honkai_automatic\pictures\ship_regiments\collect_reward.png'
        seeking(image_path, "舰团奖池")
        time.sleep(delay_random())

        # 点击领取按钮
        image_path = r'Honkai_automatic\pictures\ship_regiments\receive_ship_regiments_reward.png'
        seeking(image_path, "领取")
        time.sleep(delay_random())

        # 点击确认领取按钮，这里是在关闭奖励界面
        image_path = r'Honkai_automatic\pictures\ship_regiments\confirm.png'
        seeking(image_path, "确认领取")
        time.sleep(delay_random())

        # 可以添加的功能：识别用户领取到的奖励，并勾选下一次希望得到的奖励
        # 进去保税仓库，进行材料捐献，并发布自己的道具需求，或者领取其他人给予自己的道具
        # 进入舰团贡献，领取5000档的奖励

        # 点击主界面按钮
        pos = locateOnScreen(r'Honkai_automatic\pictures\ship_regiments\index2.png', confidence=0.6)
        if pos:
            left, top, width, height = pos
            rand_x = random.randint(left, left + width)
            rand_y = random.randint(top, top + height)
            pyautogui.moveTo(rand_x, rand_y)
            pyautogui.click(rand_x, rand_y)
            time.sleep(delay_random())
            if index_seeking() == "已处于主界面":
                if msg_queue:
                    msg_queue.put("舰团任务完成")
                else:
                    print("舰团任务完成")
            else:
                if msg_queue:
                    msg_queue.put("发生错误")
                else:
                    print("发生错误")