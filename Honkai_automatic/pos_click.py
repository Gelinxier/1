"""
定义了delay_random(), preprocess_image(),match_template(),pos_click(),seeking(),locateOnScreen()
delay_random():返回随机时间，(0.25,0.8)
preprocess_image():返回图像灰度图
match_template():多尺度匹配，则返回最佳的相关值
pos_click():执行点击的相关操作
seeking():执行pos_click()，最多执行5次
locateOnScreen():重构pyautogui.locateOnscreen()
"""
import cv2
import pyautogui
import random
import time
import keyboard
import numpy as np

def delay_random():
    """
    :return: 返回随机时间，(0.75,1.5)
    """
    random.seed(time.time())
    random_delay = random.uniform(0.75, 1.5)  # 延迟随机范围
    return random_delay

def preprocess_image(image_path):
    """
    :param image_path: 图像路径（一般为绝对路径）
    :return: 灰度图
    """
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"无法加载图像：{image_path}")
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用高斯滤波去噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def match_template(screenshot, template, method=cv2.TM_CCOEFF_NORMED,scale_range=(0.5,1.5),scale_step=0.05):
    """
    多尺度模板匹配，尝试不同缩放比例的模板进行匹配
    :param screenshot: 转换成np格式的截图
    :param template: 对应模板图像（灰度图）
    :param method: 模板匹配方法，归一化相关性
    :param scale_range: 与原模板图的比例范围
    :param scale_step: 每次比例比重提高的数字
    :return:
    """
    best_val = -1
    best_loc = None
    best_template = template
    # best_scale = -1.0
    # 将屏幕截图转换为灰度图
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    for scale in np.arange(scale_range[0], scale_range[1], scale_step):
        # 按比例缩放模板图像
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # 跳过过大或过小的模板
        if resized_template.shape[0] > screenshot_gray.shape[0] or resized_template.shape[1] > screenshot_gray.shape[1]:
            continue
        # 模板匹配
        result = cv2.matchTemplate(screenshot_gray, resized_template, method)
        # 获取匹配结果中的最大值和最小值以及位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 如果当前匹配值更高，则更新最佳匹配
        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_template = resized_template
            # best_scale = scale  # 缩放比例，暂时用不到
    return best_loc, best_val, best_template

def pos_click(image_path, label, click=None, threshold=0.6, msg_queue=None):
    """
    :param image_path: 图像路径
    :param label: 标签
    :param click: 键盘点击操作，默认为None
    :param threshold: 最低confidence（最低匹配度）
    :param msg_queue: 消息队列
    :return: 如果匹配度大于or等于要求的匹配度，则返回True；否则返回False
    """
    try:
        if click:
            time.sleep(1)
            keyboard.press_and_release(click)
            time.sleep(2)
        # 预处理模板图像
        template = preprocess_image(image_path)
        # 捕获屏幕截图
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        # 模板匹配
        max_loc, max_val, best_template = match_template(screenshot, template)
        # 判断匹配结果是否足够好
        if max_val >= threshold:
            left, top = max_loc
            width, height = best_template.shape[::-1]
            rand_x = random.randint(left, left + width)
            rand_y = random.randint(top, top + height)
            pyautogui.moveTo(rand_x, rand_y)
            time.sleep(2)
            pyautogui.mouseDown()
            time.sleep(0.5)
            pyautogui.mouseUp()
            time.sleep(delay_random())
            return True
        else:
            if msg_queue:
                msg_queue.put(f"未找到{label}按钮")
            else:
                print(f"未找到{label}按钮")
            return False
    except Exception as e:
        if msg_queue:
            msg_queue.put(f"发生错误：{e}")
        else:
            print(f"发生错误：{e}")
        return False

# 寻找按钮，找到则点击，否则等待
def seeking(image_path, label, click=None, msg_queue=None):
    """
    :param image_path: 图像路径
    :param label: 标签
    :param click: 键盘点击操作
    :param msg_queue: 消息队列
    :return: None
    """
    for i in range(5):
        if not pos_click(image_path, label, click):
            if msg_queue:
                msg_queue.put(f"找了{i+1}次")
            else:
                print (f"找了{i+1}次")
            time.sleep(0.5)
        else:
            break

# 纯模板匹配和pos_click()差不多
def locateOnScreen(image_path, confidence=0.8):
    """
    :param image_path: 图像路径
    :param confidence: 匹配度，默认0.8
    :return: 如果大于或等于confidence，则返回最佳匹配后的图像值(left, top, width, height)；否则返回None
    """
    template = preprocess_image(image_path)
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    max_loc, max_val, best_template = match_template(screenshot, template)
    left, top = max_loc
    width, height = best_template.shape[::-1]

    # 如果超过confidence，则返回正确的；否则返回None
    if max_val >= confidence:
        return left, top, width, height
    print("当前匹配度:", max_val)
    print("left, top, width, height:", left, top, width, height)
    return None


if __name__ == '__main__':
    pos_click("pycharm_label.png", "pycharm")