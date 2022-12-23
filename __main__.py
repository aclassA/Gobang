import pygame
from pygame import *
import time
#import numpy
import easygui

import os
import sys
#import turtle


#鼠标位置 ball_x, ball_y = pygame.mouse.get_pos()

class Gobang(object):

    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((800,800),depth=32)
        #鼠标点击坐标
        self.ball_x = 0
        self.ball_y = 0
        #记录走了几步棋
        self.step = 0
        #窗口标题
        pygame.display.set_caption("五子棋1.0")
        #加载图标图片
        icon = pygame.image.load('imags/logo.png')
        # 窗口图标绘制
        pygame.display.set_icon(icon)
        #设置背景颜色
        self.white = [234,180,105]
        #定义棋盘列表
        self.list = []
        #创建15*15的空列表
        # 通过nump模块快速创建二维列表
        """self.list = numpy.zeros([15,15],dtype=int)"""
        for i in range(15):
            q = []
            for j in range(15):
                q.append(0)
            self.list.append(q)
        #胜利判断检测
        self.judge = False

# 背景绘制
    def BackGround(self):
        #绘制白色背景
        self.screen.fill(self.white)
        #绘制五子棋的5个点
        pygame.draw.circle(self.screen, (0, 0, 0), center=(200, 200), radius=5)
        pygame.draw.circle(self.screen, (0, 0, 0), center=(200, 600), radius=5)
        pygame.draw.circle(self.screen, (0, 0, 0), center=(400, 400), radius=5)
        pygame.draw.circle(self.screen, (0, 0, 0), center=(600, 600), radius=5)
        pygame.draw.circle(self.screen, (0, 0, 0), center=(600, 200), radius=5)

        for i in range(50, 800, 50):
            pygame.draw.line(self.screen, (0, 0, 0), (50, i), (800-50, i))
            pygame.draw.line(self.screen, (0, 0, 0), (i, 50), (i, 800-50))


#白子类绘制
    def White_Chess(self):
        pygame.draw.circle(self.screen, (255, 255, 255), center=(self.ball_x, self.ball_y), radius=20)
        #pygame.draw.rect(self.screen, [238, 48, 167], [11, 22, 44, 44], 2, text_1.txt)
#黑子类绘制
    def Black_Chess(self):
        pygame.draw.circle(self.screen, (0, 0, 0), center=(self.ball_x, self.ball_y), radius=20)


# 绘制文字
    def drawText(self,text,x,y,textHeight = 40,Color = (255,0,0)):
        pygame.font.init()
        font_obj = pygame.font.SysFont('arial',24)
        #font_obj = pygame.font.Font('.\\font\\FZSTK.TTF',textHeight)
        text_obj = font_obj.render(text,True,Color,None)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x,y)

        self.screen.blit(text_obj,text_rect)

#鼠标检测
    def Mouse(self):
        #获取键盘事件
        sun = Algorithm()
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == QUIT:
                print("退出")
                exit()
            # 获取鼠标点击判断(元组)
            elif pygame.mouse.get_pressed() != None:
                #获取鼠标点击
                mouse = pygame.mouse.get_pressed()
                # 获取鼠标坐标
                self.ball_x, self.ball_y = pygame.mouse.get_pos()
                #自动归为
                self.ball_x, self.ball_y = sun.sumXY(self.ball_x, self.ball_y)

                #字体绘制
                """Gobang.drawText(self,text='当前棋数为：'+str(self.step),x=750,y=700)"""

                if mouse[0] == 1 and self.step % 2 == 0 and self.ball_y<775 and self.ball_x<775 and self.ball_x>25 and self.ball_y>25:
                    #获取棋子的列表位置 加工获取的鼠标坐标
                    x, y = sun.list_Conversion(self.ball_x, self.ball_y)
                    #判断该列表位置是否为没有棋子
                    if self.list[x][y] == 0:
                        if self.judge != True:
                            #为空写入棋子
                            self.list[x][y] = 2
                            #判断
                            self.judge = Algorithm.Core(self, self.list, 2)
                            # 记录鼠标点击次数
                            self.step += 1
                            Gobang.Black_Chess(self)
                        if self.judge == True:
                            easygui.msgbox('游戏结束:白子获胜 步时：：'+str(self.step), '五子棋')
                            break
                elif mouse[2] == 1 and self.step % 2 == 1 and self.ball_y<775 and self.ball_x<775 and self.ball_x>25 and self.ball_y>25:
                    # 获取棋子的列表位置 加工获取的鼠标坐标
                    x, y = sun.list_Conversion(self.ball_x, self.ball_y)
                    # 判断该列表位置是否为没有棋子
                    if self.list[x][y] == 0:
                        if self.judge != True:
                            # 为空写入棋子
                            self.list[x][y] = 1
                            # 判断
                            self.judge = Algorithm.Core(self, self.list, 1,)
                            # 记录鼠标点击次数
                            self.step += 1
                            Gobang.White_Chess(self)
                        if self.judge == True:
                            easygui.msgbox('游戏结束:黑子获胜 步时：'+str(self.step), '五子棋')
                            break

#算法
class Algorithm(object):
    def __init__(self):
        pass
    def sumXY(self,x,y):
        #五子棋位置归为算法
        if x % 100 >= 25 and x % 100 <= 75:
            x = int(x / 100) * 100 + 50
        elif x % 100 < 25:
            x = int(x / 100) * 100
        elif x % 100 > 75 and x % 100 < 100:
            x = int(x / 100 + 1) * 100
        else:
            print("错误报告：棋子归为")

        if y % 100 >= 25 and y % 100 <= 75:
            y = int(y / 100) * 100 + 50
        elif y % 100 < 25:
            y = int(y / 100) * 100
        elif y % 100 > 75 and y % 100 < 100:
            y = int(y / 100 + 1) * 100
        else:
            print("错误报告：棋子归为")
        return x,y
    def list_Conversion(self,x,y):
        # 转换位置(将图片坐标转换为列表坐标)
        ball_x = int(x / 50 - 1)
        ball_y = int(y / 50 - 1)
        return ball_x,ball_y
    def Core(self,list_all,piece):
        print('进入条件')
        for x in range(0, len((list_all))):
            for y in range(0, len(list_all[x])):
                if x >=0 and y>=0 :
                    if x<=10 and list_all[x][y] == piece and list_all[x+1][y] == piece and \
                        list_all[x+2][y]== piece and list_all[x+3][y]==piece and list_all[x+4][y]==piece:
                        print("横着获胜①")
                        return True
                        break
                    elif y<=10 and list_all[x][y] == piece and list_all[x][y+1] == piece and\
                        list_all[x][y+2]== piece and list_all[x][y+3]==piece and list_all[x][y+4]==piece:
                        print("竖着获胜②")
                        return True
                        break
                    elif y<=10 and x<=10 and list_all[x][y] == piece and list_all[x+1][y+1] == piece and\
                        list_all[x+2][y+2]== piece and list_all[x+3][y+3]==piece and list_all[x+4][y+4]==piece:
                        print("右斜获胜③")
                        return True
                        break
                    elif x>=4 and y<=10 and list_all[x][y] == piece and list_all[x-1][y+1] == piece and\
                        list_all[x-2][y+2]== piece and list_all[x-3][y+3]==piece and list_all[x-4][y+4]==piece:
                        print("左斜获胜④")
                        return True
                        break

#主程序
class Main(object):
    def main(self):
        time.sleep(0.05)
        main_i = Gobang.BackGround()
        main.Mouse()
        main.DrawIrxt()


if __name__ == '__main__':
    main = Gobang()
    main.BackGround()
    while True:
        main.Mouse()
        pygame.display.update()
