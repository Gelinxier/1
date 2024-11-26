"""
以 pygame 库作为可视化窗口，通过多线程执行视觉方面的代码。
支持显示动画、动态任务管理和用户交互功能，适用于特定的自动化任务。
"""
import queue
import threading
import time
import pygame
import imageio
import numpy as np
import random
import os
try:
    from VisualWindow.ui_elements import CheckBox, RoundedBox, LinkStart, Particle
    from Honkai_automatic import auto
except ImportError:
    from ..VisualWindow.ui_elements import CheckBox, RoundedBox, LinkStart, Particle
    from ..Honkai_automatic import auto

# 初始化
pygame.init()
# 设置窗口大小
screen = pygame.display.set_mode((270, 360))
# 设置窗口标题
pygame.display.set_caption("崩坏3是世界上最好玩的游戏！")
# 设置窗口图标
pygame.display.set_icon(
    pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "亚津子3.png")))

# 定义颜色
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (100, 155, 255)

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "font", "SimHei.ttf")

def task_start(tasks: list, task_done_event: threading.Event, msg_queue: queue.Queue):
    """
    依次执行任务列表中的任务，支持中断机制和消息队列输出。

    :param tasks: 任务列表，每个任务是 1 （即为True）时执行
    :param task_done_event: 用于指示任务完成的事件对象。
    :param msg_queue: 用于存放任务进度的消息队列。
    :return: None
    """
    for i, task in enumerate(tasks):
        if task:
            msg_queue.put(f'任务{i}开始执行')
            print(f"执行task {i}")
            auto.main(task=i, msg_queue=msg_queue)

            if stop_task:  # 如果停止标志被设置，则中断任务
                msg_queue.put(f'任务{i}被中断')
                print(f"任务{i}被中断")
                break
            time.sleep(2)  # 模拟任务执行
            msg_queue.put(f'任务{i}已完成')
            print(f"任务{i}已完成")
    if not stop_task:
        msg_queue.put(f'所有任务全部完成')
    task_done_event.set()  # 任务完成/任务中断，触发事件


def seele(surface, clock, running):
    """
    显示 Logo 动画，控制动画持续时间和透明度变化。

    :param surface: Pygame窗口对象。
    :param clock: Pygame 时钟对象。
    :param running: 程序运行状态标志。
    :return: running, None
    """
    center_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "崩坏3.jpg")
    center_image = pygame.image.load(center_image_path).convert_alpha()
    center_image = pygame.transform.scale(center_image, (473/3, 319/3))  # 调整图片大小
    center_image_rect = center_image.get_rect(center=(135, 100))

    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "鸽鸽.gif")
    gif_frames = imageio.mimread(gif_path)
    particles = []  # 存储粒子
    frames = []
    gif_width, gif_height = 100, 100  # 缩放后的 GIF 尺寸
    for frame in gif_frames:
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        scaled_frame = pygame.transform.scale(frame_surface, (gif_width, gif_height))
        frames.append(scaled_frame)

    # GIF 动画参数
    gif_frame_index = 0
    gif_fps = 30
    gif_position = [random.randint(50, 270-100), random.randint(50, 360-100)]  # 初始位置
    gif_target_position = gif_position[:]
    gif_move_speed = 5  # 每帧移动像素
    gif_move_timer = time.time()

    # 动画时间和透明度
    start_time = time.time()
    animation_duration = 3  # 动画总时长
    alpha_decay_rate = 255 / animation_duration

    # 显示动画
    while running:
        # 正常程序逻辑
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        current_time = time.time() - start_time
        if current_time >= animation_duration:
            break

        surface.fill(White)

        # 中心图片透明度渐变
        remaining_alpha = max(255 - int(alpha_decay_rate * current_time), 0)
        faded_image = center_image.copy()
        faded_image.fill((255, 255, 255, remaining_alpha), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(faded_image, center_image_rect)

        # 更新 GIF 目标位置每 0.5 秒
        if time.time() - gif_move_timer >= 0.5:
            gif_move_timer = time.time()
            gif_target_position = [random.randint(50, 270 - 100), random.randint(50, 360 - 100)]

        # 逐帧移动 GIF 到目标位置
        for i in range(2):
            if gif_position[i] < gif_target_position[i]:
                gif_position[i] = min(gif_position[i] + gif_move_speed, gif_target_position[i])
            elif gif_position[i] > gif_target_position[i]:
                gif_position[i] = max(gif_position[i] - gif_move_speed, gif_target_position[i])
        # 更新例子
        for particle in particles[:]:
            particle.update()
            particle.draw(surface)
            if particle.life <= 0:
                particles.remove(particle)

        if random.random() < 0.3:
            particles.append(Particle(135, 100))

        # 绘制当前帧的 GIF
        surface.blit(frames[gif_frame_index], gif_position)
        gif_frame_index = (gif_frame_index + 1) % len(frames)  # 循环播放 GIF

        # 更新显示
        pygame.display.update()
        clock.tick(gif_fps)
    return running, False


# 主程序
def main():
    """
    程序入口，控制界面显示、任务执行、用户交互和消息队列处理。
    """
    # 创建时钟对象
    clock = pygame.time.Clock()

    # 消息
    msg_queue = queue.Queue()
    display_messages = []
    min_message_interval = 30
    bottom_position = 360 - 20
    elia_task = [0] * 5
    # 复选框
    checkbox0 = CheckBox(75, 25, "0.登录游戏", color=(80, 170, 255))
    checkbox1 = CheckBox(75, 50, '1.材料远征')
    checkbox2 = CheckBox(75, 75, '2.家园打工')
    checkbox3 = CheckBox(75, 100, '3.舰团委托')
    checkbox4 = CheckBox(75, 125, '4.领取奖励')
    # 圆角框
    rounded_box = RoundedBox(65, 20, 140, 175)
    # 下面的标记必须相同
    start_button = RoundedBox(90, 150, 80, 40)
    link_start = LinkStart(90, 150, 80, 40)

    task_running = False
    task_done_event = threading.Event()
    global stop_task
    stop_task = False

    # 控制 logo 显示时间
    logo_display_time = 3  # 设定 Logo 显示 3 秒
    logo_start_time = time.time()  # 获取开始显示 logo 的时间
    is_logo_displaying = True  # 标记 logo 是否正在显示

    running = True
    while running:
        # 分两种显示
        if is_logo_displaying:
            # 显示 logo 动画或效果
            running, is_logo_displaying = seele(screen, clock, running)

            # 判断是否已经显示过了设定的时间
            if time.time() - logo_start_time >= logo_display_time:
                is_logo_displaying = False  # Logo 显示时间到，停止显示
        else:
            while running:
                screen.fill(White)
                # 正常逻辑
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        checkbox0.handle_event(event)
                        checkbox1.handle_event(event)
                        checkbox2.handle_event(event)
                        checkbox3.handle_event(event)
                        checkbox4.handle_event(event)
                        if any(elia_task[i] == 1 for i in range(5)) and not link_start.checked:
                            link_start.handle_event(event)
                        elif link_start.checked:
                            link_start.handle_event(event)
                            stop_task = True

                if checkbox0.checked:
                    elia_task[0] = 1
                else:
                    elia_task[0] = 0
                if checkbox1.checked:
                    elia_task[1] = 1
                else:
                    elia_task[1] = 0
                if checkbox2.checked:
                    elia_task[2] = 1
                else:
                    elia_task[2] = 0
                if checkbox3.checked:
                    elia_task[3] = 1
                else:
                    elia_task[3] = 0
                if checkbox4.checked:
                    elia_task[4] = 1
                else:
                    elia_task[4] = 0

                if link_start.checked and not task_running:
                    task_running = True
                    stop_task = False
                    threading.Thread(target=task_start, args=(elia_task, task_done_event, msg_queue),
                                     daemon=True).start()

                if not msg_queue.empty():
                    msg = msg_queue.get()
                    new_msg_position = bottom_position
                    if display_messages:
                        last_msg_position = display_messages[-1][2]
                        if last_msg_position > new_msg_position - min_message_interval:
                            new_msg_position = last_msg_position - min_message_interval
                    display_messages.append([msg, time.time(), new_msg_position])
                    # 越新的消息越靠后，所以列表倒着读
                    for i in range(len(display_messages) - 2, -1, -1):
                        if display_messages[i][2] > display_messages[i + 1][2] - min_message_interval:
                            display_messages[i][2] = display_messages[i + 1][2] - min_message_interval

                for i, (msg, start_time, y_position) in enumerate(display_messages):
                    elapsed_time = time.time() - start_time
                    alpha = max(255 - int(elapsed_time * 255 / 4), 0)

                    display_messages[i][2] -= 0.5

                    font = pygame.font.Font(font_path, 20)
                    text_surface = font.render(msg, True, Black)
                    rect_text = text_surface.get_rect(center=(135, y_position))
                    text_surface.set_alpha(alpha)
                    screen.blit(text_surface, rect_text)

                    if alpha == 0:
                        display_messages.pop(i)

                if task_done_event.is_set():
                    task_running = False
                    link_start.checked = False
                    task_done_event.clear()

                if link_start.checked:
                    link_start.draw(screen, "停止")
                else:
                    link_start.draw(screen, "开始")
                    if task_done_event.is_set():
                        print("主程序停止")
                        task_done_event.set()

                rounded_box.draw(screen)
                checkbox0.draw(screen)
                checkbox1.draw(screen)
                checkbox2.draw(screen)
                checkbox3.draw(screen)
                checkbox4.draw(screen)
                start_button.draw(screen)

                # 更新显示
                pygame.display.flip()

                # 控制帧率为 60 FPS
                clock.tick(60)


if __name__ == '__main__':
    main()