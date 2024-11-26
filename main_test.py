import queue
import threading
import time
import pygame
from Honkai_automatic import auto
import imageio
import numpy as np
import random

# 初始化
pygame.init()
# 设置窗口大小
screen = pygame.display.set_mode((500, 500))
# 设置窗口标题
pygame.display.set_caption("崩坏3是世界上最好玩的游戏！")
# 设置窗口图标
# pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.display.set_icon(pygame.image.load('visualization_window/assets/images/亚津子3.png'))

# 定义颜色
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (100, 155, 255)

# 定义字体路径
font_path = r"E:\free2\字体\SimHei.ttf"

# 定义勾选框类
class Checkbox:
    def __init__(self, x, y, label, font_size=17, size=20, color=Black, check_color=White, fill_color=Blue, _font_path=font_path):
        """
        :param x: 横坐标
        :param y: 纵坐标
        :param label: 复选框后跟随的标签
        :param font_size: 文字大小
        :param size: 复选框的长/宽
        :param color: 复选框的颜色
        :param check_color: 选中后用到的颜色
        :param fill_color: 选中后用到的颜色
        :param _font_path: 字体路径
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.label = label
        self.color = color
        self.check_color = check_color
        self.fill_color = fill_color
        self.checked = False
        self.font = pygame.font.Font(_font_path, font_size)

    # 绘制
    def draw(self, surface):
        # 绘制边框
        pygame.draw.rect(surface, self.color, self.rect,2)
        if self.checked:
            # 填充为蓝色
            pygame.draw.rect(surface, self.fill_color, self.rect)
            # 重新绘制黑色边框
            pygame.draw.rect(surface, self.color, self.rect, 2)
            # 绘制白色对勾
            pygame.draw.line(surface, self.check_color,
                             (self.rect.x + 3, self.rect.y + self.rect.height // 2),
                             (self.rect.x + self.rect.width // 3, self.rect.y + self.rect.height - 3), 3)
            pygame.draw.line(surface, self.check_color,
                             (self.rect.x + self.rect.width // 3, self.rect.y + self.rect.height - 3),
                             (self.rect.x + self.rect.width - 3, self.rect.y + 3), 3)

        # 绘制标签文字
        label_surface = self.font.render(self.label, True, self.color)
        surface.blit(label_surface, (self.rect.right + 10, self.rect.y))

    # 如果选中则取反
    def toggle(self):
        self.checked = not self.checked

    # 点击事件
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()

# 定义圆角框类
class RoundedBox:
    def __init__(self, x, y, width, height, border_radius=10, color=Black):
        self.rect_position = (x, y)
        self.rect_size = (width, height)
        self.border_radius = border_radius
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, Black, (*self.rect_position, *self.rect_size), 3, border_radius=self.border_radius)

# 定义开启/停止类
class LinkStart:
    def __init__(self, x, y, width, height, _font_path=font_path, font_size=20, color=Black):
        self.rect = pygame.Rect(x, y, width, height)
        self.checked = False
        self.font = pygame.font.Font(_font_path, font_size)
        self.color = color

    def draw(self, surface, label):
        label_surface = self.font.render(label, True, self.color)
        label_rect = label_surface.get_rect(center=self.rect.center)
        surface.blit(label_surface, label_rect)

    def toggle(self):
        self.checked = not self.checked

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle()


# 执行任务的函数
def task_start(tasks: list, task_done_event: threading.Event, msg_queue: queue.Queue):
    for i, task in enumerate(tasks):
        if task:
            msg_queue.put(f'任务{i + 1}开始执行')
            print(f"执行task {i + 1}")
            auto.main(task=i+1, msg_queue=msg_queue)

            if stop_task:  # 如果停止标志被设置，则中断任务
                msg_queue.put(f'任务{i + 1}被中断')
                print(f"任务{i + 1}被中断")
                break
            time.sleep(2)  # 模拟任务执行
            msg_queue.put(f'任务{i + 1}已完成')
            print(f"任务{i + 1}已完成")
    if not stop_task:
        msg_queue.put(f'所有任务全部完成')
    task_done_event.set()  # 任务完成/任务中断，触发事件

def seele(screen, clock,running):
    # 加载中心图片并缩放
    center_image_path = "visualization_window/assets/images/亚津子3.png"
    center_image = pygame.image.load(center_image_path).convert_alpha()
    center_image = pygame.transform.scale(center_image, (100, 100))  # 调整图片大小
    center_image_rect = center_image.get_rect(center=(250, 250))

    # 加载 GIF 文件并转换为帧
    gif_path = "visualization_window/assets/images/鸽鸽.gif"
    gif_frames = imageio.mimread(gif_path)
    frames = []
    gif_width, gif_height = 100, 100  # 缩放后的 GIF 尺寸
    for frame in gif_frames:
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        scaled_frame = pygame.transform.scale(frame_surface, (gif_width, gif_height))
        frames.append(scaled_frame)

    # GIF 动画参数
    gif_frame_index = 0
    gif_fps = 30
    gif_position = [random.randint(50, 400), random.randint(50, 400)]  # 初始位置
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

        screen.fill(White)

        # 中心图片透明度渐变
        remaining_alpha = max(255 - int(alpha_decay_rate * current_time), 0)
        faded_image = center_image.copy()
        faded_image.fill((255, 255, 255, remaining_alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(faded_image, center_image_rect)

        # 更新 GIF 目标位置每 0.5 秒
        if time.time() - gif_move_timer >= 0.7:
            gif_move_timer = time.time()
            gif_target_position = [random.randint(50, 400), random.randint(50, 400)]

        # 逐帧移动 GIF 到目标位置
        for i in range(2):
            if gif_position[i] < gif_target_position[i]:
                gif_position[i] = min(gif_position[i] + gif_move_speed, gif_target_position[i])
            elif gif_position[i] > gif_target_position[i]:
                gif_position[i] = max(gif_position[i] - gif_move_speed, gif_target_position[i])

        # 绘制当前帧的 GIF
        screen.blit(frames[gif_frame_index], gif_position)
        gif_frame_index = (gif_frame_index + 1) % len(frames)  # 循环播放 GIF

        # 更新显示
        pygame.display.update()
        clock.tick(gif_fps)
    return running, False
# 主程序
def main():
    # 创建时钟对象
    clock = pygame.time.Clock()

    msg_queue = queue.Queue()
    display_messages = []
    min_message_interval = 30
    bottom_position = 500 - min_message_interval
    elia_task = [0] * 4
    checkbox1 = Checkbox(50, 50, '材料远征')
    checkbox2 = Checkbox(50, 70, '家园打工')
    checkbox3 = Checkbox(50, 90, '舰团委托')
    checkbox4 = Checkbox(50, 110, '领取奖励')
    rounded_box = RoundedBox(40, 40, 200, 200)
    start_button = RoundedBox(50, 200, 80, 40)
    link_start = LinkStart(50, 200, 80, 40)

    task_running = False
    task_done_event = threading.Event()
    global stop_task
    stop_task = False

    # 控制 logo 显示时间
    logo_display_time = 5  # 设定 Logo 显示 5 秒
    logo_start_time = time.time()  # 获取开始显示 logo 的时间
    is_logo_displaying = True  # 标记 logo 是否正在显示

    running = True
    while running:

        if is_logo_displaying:
            # 显示 logo 动画或效果
            running,is_logo_displaying = seele(screen,clock,running)  # 假设你在这个方法里处理 logo 的显示和特效

            # 判断是否已经显示过了设定的时间
            if time.time() - logo_start_time >= logo_display_time:
                is_logo_displaying = False  # Logo 显示时间到，停止显示
        else:
            while running:
                screen.fill(White)
                # 正常程序逻辑
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        checkbox1.handle_event(event)
                        checkbox2.handle_event(event)
                        checkbox3.handle_event(event)
                        checkbox4.handle_event(event)
                        if any(elia_task[i] == 1 for i in range(4)) and not link_start.checked:
                            link_start.handle_event(event)
                        elif link_start.checked:
                            link_start.handle_event(event)
                            stop_task = True

                if checkbox1.checked:
                    elia_task[0] = 1
                else:
                    elia_task[0] = 0
                if checkbox2.checked:
                    elia_task[1] = 1
                else:
                    elia_task[1] = 0
                if checkbox3.checked:
                    elia_task[2] = 1
                else:
                    elia_task[2] = 0
                if checkbox4.checked:
                    elia_task[3] = 1
                else:
                    elia_task[3] = 0

                if link_start.checked and not task_running:
                    task_running = True
                    stop_task = False
                    threading.Thread(target=task_start, args=(elia_task, task_done_event, msg_queue), daemon=True).start()

                if not msg_queue.empty():
                    msg = msg_queue.get()
                    new_msg_position = bottom_position
                    if display_messages:
                        last_msg_position = display_messages[-1][2]
                        if last_msg_position > new_msg_position - min_message_interval:
                            new_msg_position = last_msg_position - min_message_interval
                    display_messages.append([msg, time.time(), new_msg_position])

                for i in range(len(display_messages) - 2, -1, -1):
                    if display_messages[i][2] > display_messages[i + 1][2] - min_message_interval:
                        display_messages[i][2] = display_messages[i + 1][2] - min_message_interval

                for i, (msg, start_time, y_position) in enumerate(display_messages):
                    elapsed_time = time.time() - start_time
                    alpha = max(255 - int(elapsed_time * 255 / 4), 0)

                    display_messages[i][2] -= 1

                    font = pygame.font.Font(font_path, 20)
                    text_surface = font.render(msg, True, Black)
                    rect_text = text_surface.get_rect(center=(250, y_position))
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

                rounded_box.draw(screen)
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