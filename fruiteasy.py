from tkinter import font
import pgzrun
import pygame
import random
import math
import os
from pgzero.builtins import Actor
from pgzero.builtins import Rect
import sys
import time 

# 定义游戏相关属性
TITLE = '果了个果' 
WIDTH = 640
HEIGHT = 680

# 自定义游戏常量
T_WIDTH = 60
T_HEIGHT = 66

# 下方牌堆的位置
DOCK = Rect((0, 564), (T_WIDTH*7, T_HEIGHT))

# 上方的所有牌
tiles = []
# 牌堆里的牌
docks = []

# 初始化牌组，12*12张牌随机打乱
ts = list(range(1, 13))*12
random.shuffle(ts)
n = 0
for k in range(7):    # 7层
    for i in range(7-k):    #每层减1行
        for j in range(7-k):
            t = ts[n]        #获取排种类
            n += 1
            tile = Actor(f'fruit{t}')       #使用tileX图片创建Actor对象
            tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9    #设定位置
            tile.tag = t            #记录种类
            tile.layer = k          #记录层级
            tile.status = 1          #设置牌的状态
            tiles.append(tile)
for i in range(4):        #剩余的4张牌放下面（为了凑整能通关）
    t = ts[n]
    n += 1
    tile = Actor(f'fruit{t}')
    tile.pos = 210 + i * tile.width, 516
    tile.tag = t
    tile.layer = 0
    tile.status = 1  
    tiles.append(tile)

#自动生成
# 初始化倒计时
countdown_time = 144  # 倒计时时间（秒）
start_time = time.time()  # 游戏开始时间

# 游戏帧绘制函数
def draw():
    global countdown_time
    screen.clear()
    screen.blit('back', (0, 0))  # 背景图
    
    # 绘制牌
    for tile in tiles:
        tile.draw()
        if tile.status == 0:
            screen.blit('mask', tile.topleft)  # 不可点的添加遮罩

    for i, tile in enumerate(docks):
        tile.left = (DOCK.x + i * T_WIDTH)
        tile.top = DOCK.y
        tile.draw()

    # 计算剩余时间
    elapsed_time = time.time() - start_time
    remaining_time = max(0, countdown_time - int(elapsed_time))

    # 绘制倒计时
    font = pygame.font.SysFont(None, 40)
    text_surface = font.render(f'time left:{remaining_time}S', True, (255, 0, 0))
    screen.blit(text_surface, (250, 10))

    # 检查倒计时是否结束
    if remaining_time == 0:
        screen.blit('end', (0, 0))
        return

    # 超过14张，失败
    if len(docks) >= 11:
        screen.blit('end', (0, 0))
    # 没有剩牌，胜利
    if len(tiles) == 0:
        screen.blit('win', (0, 0))

# 鼠标点击响应
def on_mouse_down(pos):
    global docks
    if len(docks) >= 11 or len(tiles) == 0:  # 游戏结束不响应
        return
    for tile in reversed(tiles):  # 逆序循环是为了先判断上方的牌，如果点击了就直接跳出，避免重复判定
        if tile.status == 1 and tile.collidepoint(pos):
            # 状态1可点，并且鼠标在范围内
            tile.status = 2
            tiles.remove(tile)
            diff = [t for t in docks if t.tag != tile.tag]  # 获取牌堆内不相同的牌
            if len(docks) - len(diff) < 2:  # 如果相同的牌数量<2，就加进牌堆
                docks.append(tile)
            else:  # 否则用不相同的牌替换牌堆（即消除相同的牌）
                docks = diff
            for down in tiles:  # 遍历所有的牌
                if down.layer == tile.layer - 1 and down.colliderect(tile):  # 如果在此牌的下一层，并且有重叠
                    for up in tiles:  # 那就再反过来判断这种被覆盖的牌，是否还有其他牌覆盖它
                        if up.layer == down.layer + 1 and up.colliderect(down):  # 如果有就跳出
                            break
                    else:  # 如果全都没有，说明它变成了可点状态
                        down.status = 1
            return

pgzrun.go()
