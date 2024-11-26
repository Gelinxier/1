"""
首先获取崩坏三主界面任务、出击、舰团、家园这四张位于pictures文件夹中对应任务名文件夹中的截图,
通过get_image_paths函数返回由它们的绝对路径(相对路径)组成的数组（按顺序），
在index_Seekking函数中通过导入pos_click.py中的loacteonScreen函数检测目前屏幕上是否存在这些图片,
当四个图片均存在时，打印“已处于主界面”，否则打印“未处于主界面”
该py文件主要是用于检测当前是否处于崩坏三的主界面中
"""
import os
from .pos_click import locateOnScreen

def get_image_paths():
    """
    获取图片的相对路径列表，适配不同运行环境
    """
    image_relative_paths = [
        "mission.png",
        "sortie.png",
        "Ship_regiments.png",
        "homeland.png",
    ]
    return [os.path.join("Honkai_automatic", "pictures", "index_seeking", path) for path in image_relative_paths]

#主界面定位：执行每一个任务之前需要定位到主界面
def index_seeking():
    images = get_image_paths()
    positions = 0
    for image in images:
        # 使用 locateOnScreen 检测图片是否存在
        pos = locateOnScreen(image, confidence=0.6)
        if pos:
            positions+=1
    if len(images) == positions:
        return "已处于主界面"
    else:
        return "未处于主界面"

# def index_seeking():
#     images = get_image_paths()
#     for image in images:
#         # 使用 locateOnScreen 检测图片是否存在
#         pos = locateOnScreen(image, confidence=0.6)
#         if pos:
#             continue
#         else:
#             return "未处于主界面"
#     return "已处于主界面"

if __name__ == '__main__':
    print(index_seeking())