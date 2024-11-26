"""
为pygame定义了基本的UI元素的类:CheckBox, RoundedBox, LinkStart
"""
import pygame
import os
import random

# 定义颜色
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (100, 155, 255)
# 定义字体路径
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "font", "SimHei.ttf")

# 定义勾选框类
class CheckBox:
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
        """
        :param x: 横坐标
        :param y: 纵坐标
        :param width: 宽
        :param height: 高
        :param border_radius: 圆角半径，默认10
        :param color: 颜色，默认黑色
        """
        self.rect_position = (x, y)
        self.rect_size = (width, height)
        self.border_radius = border_radius
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, Black, (*self.rect_position, *self.rect_size), 3, border_radius=self.border_radius)

# 定义开启/停止类
class LinkStart:
    def __init__(self, x, y, width, height, _font_path=font_path, font_size=20, color=Black):
        """
        :param x: 横坐标
        :param y: 纵坐标
        :param width: 宽
        :param height: 高
        :param _font_path: 字体路径（绝对路径）
        :param font_size: 字体大小，默认20
        :param color: 颜色，默认黑色(0, 0, 0)
        """
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

# 粒子类
class Particle:
    def __init__(self, x, y):
        """
        :param x: 横坐标
        :param y: 纵坐标
        """
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = random.choice([(0, 122, 255), (255, 0, 0), (255, 255, 0)])
        self.life = random.randint(20, 50)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
