"""
这是实现功能部分的内操作台,在main函数内打印了功能实现的菜单:
输入0,实现自动登录和签到领取功能
输入1,完成材料远征任务
输入2,完成家园打工任务
输入3,完成舰团委托任务
输入4,完成领取任务奖励
如果输入其他数字,打印输入错误,请重新输入
"""
import time
from . import login
from . import material_collection
from . import homeland
from . import ship_regiments
from . import mission_accomplished


def main(task=None, msg_queue=None):
    print("欢迎使用HAA自动脚本！")
    if task is None:
        print("请选择要执行的任务：")
        print("0.开始登舰")
        print("1.材料远征")
        print("2.家园打工")
        print("3.舰团委托")
        print("4.领取任务奖励")
        task = int(input("请输入任务序号："))
    else:
        tasks = ["0.开始登舰", "1.材料远征", "2.家园打工", "3.舰团委托", "4.领取任务奖励"]
        print("你当前执行的脚本为{}".format(tasks[task]))
    if task == 0:
        time.sleep(6)
        if msg_queue is None:
            login.login()
        else:
            login.login(msg_queue)
    elif task == 1:
        time.sleep(6)
        if msg_queue is None:
            material_collection.material_collection()
        else:
            material_collection.material_collection(msg_queue)
    elif task == 2:
        time.sleep(6)
        if msg_queue is None:
            homeland.homeland()
        else:
            homeland.homeland(msg_queue)
    elif task == 3:
        time.sleep(6)
        if msg_queue is None:
            ship_regiments.ship_regiments()
        else:
            ship_regiments.ship_regiments(msg_queue)
    elif task == 4:
        time.sleep(6)
        if msg_queue is None:
            mission_accomplished.mission_accomplished()
        else:
            mission_accomplished.mission_accomplished(msg_queue)
    else:
        print("输入错误，请重新输入")

if __name__ == '__main__':
    main()