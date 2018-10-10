from PIL import ImageGrab, Image
import os,sys
from pymouse import *
from pykeyboard import PyKeyboard
from math import pi,cos,sin
import random
import time

top = 700
left = 700
bottom = 0
right = 0

# 位置--> 点
def pos_point(x,y,bottom,right,pos):
    yy = y - 1 - (bottom - 12 - pos[1]) / 16
    xx = x - 1 - (right - 11 - pos[0]) / 16
    point = yy*x + xx
    return point

# 获取扫雷程序在屏幕上的位置
def locate_program():
    global top, bottom, left, right
    top = 700
    left = 700
    bottom = 0
    right = 0
    blank = (128, 128, 128, 255)
    img = ImageGrab.grab((0,0,1400,900)).convert('RGBA')
    for j in range(700):
        for i in range(700):
            if img.getpixel((i,j))== blank and img.getpixel((i+1,j+1))==(255,255,255,255):
                if j > bottom:
                    bottom = j
                if i > right:
                    right = i
            if img.getpixel((i,j))== blank and img.getpixel((i-1,j))== blank and img.getpixel((i+1,j))==(255,255,255,255):
                if j < top:
                    top = j
                if i < left:
                    left = i
    right = right - 9
    bottom = bottom - 9
    left = left + 9
    top = top + 8
    print(left,right,top,bottom,'\r\n')


def main():
    mouse = PyMouse()
    # 各标记的像素值
    one = (0, 0, 255, 255)
    two = (0, 128, 0, 255)
    three = (255, 0, 0, 255)
    four = (0, 0, 128, 255)
    five = (128, 0, 0, 255)
    six = (0, 128, 128, 255)
    seven = (0, 0, 0, 255)
    eight = (128, 128, 128, 255)
    mine = (255, 255, 255, 255)
    zero = (192, 192, 192, 255)
    blank = (128, 128, 128, 255)
    restart = (255, 255, 0, 255)

    ge = 16 # 每一格16
    global top, bottom, left, right

    print("—————————— 自动扫雷程序 by Rose ——————————")
    print("请设置屏幕分辨为1280×720，并打开扫雷程序（白色旧版），拖动至屏幕左上方置顶，勿遮挡！")
    a = input("按任意键继续...")

    running = True 
    
    
    # 用户界面循环，每次选择难度之后将重复扫雷10次
    while running:
        
        locate_program()
        menu = top - 70
        
        while True:
            print("\r\n请选择扫雷难度：Easy(9×9)请输入1，Middle(16×16)请输入2，Hard(30×16)请输入3，每次选择后将扫雷10次")
            mode = int(input("请输入难度选择："))
            mouse.click(left, top-ge, 1)
            mouse.click(left, menu, 1)
            mouse.click(left, top + (mode-2) * 20, 1)
            mouse.move(left, top - 100)
            if mode == 1:
                x, y = 9, 9
                break
            elif mode == 2:
                x, y = 16, 16
                break
            elif mode == 3:
                x, y = 30, 16
                break
            else:
                print("输入错误，请重新输入！")
                
        time.sleep(1)
        locate_program()
        restart_x = int((left + right)/2)
        restart_y = top - 34 

        run_times = 10
        win = 0
        total_time = 0
        time0 = time.time()

        # 每一次扫雷循环
        while run_times:
            print("第", 11-run_times, "次扫雷开始：")
            run_times -= 1
            mouse.click(left, top-ge, 1)
            time.sleep(0.5)
            mouse.click(restart_x, restart_y, 1)
            mouse.click(right, bottom, 1)
            last_guess_point = x*y-1
            if mode == 3:
                mouse.click(left, bottom, 1)
                last_guess_point = x*y-x

            fail = False
            game_over = False
            check = False
            start_time = time.time()
            

            list_cue = [9] *x*y
            clicked = [0] *x*y

            # 扫雷核心算法循环
            while not game_over and not fail:                    
                used_time = (time.time() - time0)% 62
                if used_time > 60:
                    a=input("超时,任意键继续")
                    break
           
                # 截屏，读取图片
                try:
                    img = ImageGrab.grab((0,0,1400,900)).convert('RGBA')
                except OSError:
                    a = input("截图出错")

                # 将图片像素信息转化为list_cue[poin] = cue（0为空白，1-8为数字，9为未翻开区域，10为flag）
                for j in range(y):
                    for i in range(x):
                        
                        # (i,j)对应的点为j*x+i,对应的位置为pos0,pos1
                        pos0 = right - (x-1-i)*ge
                        pos1 = bottom - (y-1-j)*ge
                        if img.getpixel((pos0 - int(ge/2) + 1 ,pos1 - int(ge/2) + 1)) == mine:  # 右上角为白色
                            if img.getpixel((pos0,pos1 - 1))== zero:  # 中间白点
                                list_cue[j*x+i] = 9
                        if img.getpixel((pos0 - int(ge/2) + 1 ,pos1 - int(ge/2) + 1)) == zero: # 右上角是灰色
                            if img.getpixel((pos0,pos1))== eight:
                                list_cue[j*x+i] = 8
                            elif img.getpixel((pos0,pos1))== seven and img.getpixel((pos0-2,pos1))== blank:
                                list_cue[j*x+i] = 7
                            elif img.getpixel((pos0,pos1))== six:
                                list_cue[j*x+i] = 6
                            elif img.getpixel((pos0,pos1))== five:
                                list_cue[j*x+i] = 5
                            elif img.getpixel((pos0,pos1))== four:
                                list_cue[j*x+i] = 4
                            elif img.getpixel((pos0,pos1))== three:
                                list_cue[j*x+i] = 3
                            elif img.getpixel((pos0,pos1))== two:
                                list_cue[j*x+i] = 2
                            elif img.getpixel((pos0,pos1))== one:
                                list_cue[j*x+i] = 1
                            elif img.getpixel((pos0,pos1))== zero:
                                list_cue[j*x+i] = 0
                        if img.getpixel((pos0 - 1,pos1 - 1))== mine: # 所有雷
                            list_cue[j*x+i] = -1
                        if img.getpixel((pos0 + int(ge/2) - 1 ,pos1 + int(ge/2) - 1))== three:# 炸雷的位置
                            list_cue[j*x+i] = -10
                            fail = True
                            print("boom:(",i,j,")")
                        if img.getpixel((pos0-1,pos1+1))== three: #标雷标错了
                            list_cue[j*x+i] = -20
                            check = True
                            
                #标雷标错了
                if check:
                    run_times += 1
                    print("Abnormal fail, not count!\r\n")
                    break
                    '''
                    for i in range(y):
                        print(list_cue[x*i:x*i+x])
                    print('')
                    a = input("check...")
                    check = False
                    '''    
                if fail:
                    if list_cue[0] == -10 or list_cue[x*y-x] == -10 \
                       or list_cue[x-1] == -10 or list_cue[x*y-1] == -10:
                        run_times += 1
                        print("corner mine, not count!")
                    else:
                        print("fail!\r\n")
                    break
                    
                # 如果所有都翻开，则game_over,break
                move = False
                game_over = True
                for i in range(x*y):
                    if list_cue[i] == 9:
                        game_over = False
                        break
                if game_over:
                    used_time = time.time()-start_time
                    print("You Win! 用时：",used_time,'\r\n')
                    if used_time < 0.1:
                        print("Abnormal win, not count!")
                        run_times += 1
                        '''
                        for i in range(y):
                            print(list_cue[x*i:x*i+x])
                        print('')
                        command = input("checkwin... ")
                        '''
                    else:
                        total_time += used_time
                        win += 1
                    break
           
                # 以下都是遍历所有翻开的有数字的格子(一次截屏可翻出多个格子)
                
                # 普通找法1：查找neighbor中只有一个空白=cue - flag 的point,判断它是否为雷，flag或者点开
                for point in range(x*y):
                    if list_cue[point] in range(1,8):
                        flag_num = 0
                        blank_num = 0
                        blank_neighbor = []        
                        for j in range(8):
                            xx = int(1.5 * cos(j* pi/4))
                            yy = int(1.5 * sin(j* pi/4))
                            next_point = point + yy*x + xx
                            if ((point % x) + xx) in range(x) and ((point // x) + yy) in range(y):
                                if list_cue[next_point] == 10:
                                    flag_num += 1
                                elif list_cue[next_point] == 9:
                                    blank_num += 1
                                    blank_neighbor.append(next_point)
                        if blank_num == (list_cue[point] - flag_num) and blank_num:
                            for each in blank_neighbor:
                                if not clicked[each]:
                                    pos00 = right - (x - 1 - each % x)* ge
                                    pos11 = bottom - (y - 1 - each // x)* ge
                                    mouse.click(pos00,pos11,2)
                                    move = True
                                    clicked[each] = 1
                                    list_cue[each] = 10
                                    

                # 普通找法2：查找所有neighbor中flag = cue的point,双击它(打开它的neibor_8)
                for point in range(x*y):
                    if list_cue[point] in range(1,8):
                        flag_num = 0
                        blank_num = 0
                        blank_neighbor = []    
                        for j in range(8):
                            xx = int(1.5 * cos(j* pi/4))
                            yy = int(1.5 * sin(j* pi/4))
                            next_point = point + yy*x + xx
                            if (point % x) + xx in range(x) and (point // x) + yy in range(y):
                                if list_cue[next_point] == 10:
                                    flag_num += 1
                                elif list_cue[next_point] == 9:
                                    blank_num += 1
                                    blank_neighbor.append(next_point)
                        if list_cue[point] == flag_num and blank_num > 0:
                            for each in blank_neighbor:
                                if not clicked[each]: 
                                    pos00 = right - (x - 1 - each % x)* ge
                                    pos11 = bottom - (y - 1 - each // x)* ge
                                    mouse.click(pos00,pos11,1)
                                    move = True
                                    clicked[each] = 1
                
                if not move:
                    
                    # 高级找法准备：找出所有标数字的点周围的标旗数，空白数，空白点坐标
                    list_neighbor_flag_num = [0] *x*y
                    list_neighbor_blank_num = [0] *x*y
                    list_blank_neighbor = [[-1]] *x*y
                    for point in range(x*y):
                        if list_cue[point] in range(1,8):
                            blank_neighbor = [-1]               
                            for j in range(8):
                                xx = int(1.5 * cos(j* pi/4))
                                yy = int(1.5 * sin(j* pi/4))
                                next_point = point + yy*x + xx
                                if ((point % x) + xx) in range(x) and ((point // x) + yy) in range(y):
                                    if list_cue[next_point] == 10:
                                        list_neighbor_flag_num[point] += 1
                                    elif list_cue[next_point] == 9:
                                        list_neighbor_blank_num[point] += 1
                                        blank_neighbor.append(next_point)
                            list_blank_neighbor[point] = blank_neighbor
                            
                    
                    for point1 in range(x*y):
                        if list_blank_neighbor[point1] != [-1]:
                            for point2 in range(x*y):
                                if point2 != point1 and list_blank_neighbor[point2] != [-1]:
                                    
                                    # 高级找法1：一个点的空白邻居都包含在另一个点的空白邻居之内，而且两个点还剩雷数量相同，则另一个点其余的空白都不是雷
                                    if set(list_blank_neighbor[point2]).issubset(set(list_blank_neighbor[point1])):
                                        differences = set(list_blank_neighbor[point1]).difference(set(list_blank_neighbor[point2]))
                                        if list_cue[point1] - list_neighbor_flag_num[point1] == \
                                           list_cue[point2] - list_neighbor_flag_num[point2]:
                                            for each in differences:
                                                if not clicked[each]:
                                                    pos00 = right - (x - 1 - each % x)* ge
                                                    pos11 = bottom - (y - 1 - each // x)* ge
                                                    mouse.click(pos00,pos11,1)
                                                    move = True
                                                    clicked[each] = 1
                                                    
                                    # 高级找法2：一个点的空白邻居比另一个点多n个，但是还剩雷的数目也多n个，则多的那n个点都是雷        
                                    if set(list_blank_neighbor[point1]) & set(list_blank_neighbor[point2]) != {-1}:
                                        differences1 = set(list_blank_neighbor[point1]) - set(list_blank_neighbor[point2])
                                        if differences1:
                                            if list_cue[point1] - list_neighbor_flag_num[point1] == \
                                               list_cue[point2] - list_neighbor_flag_num[point2] + len(differences1):
                                                for each in differences1:
                                                    if not clicked[each]:
                                                        pos00 = right - (x - 1 - each % x)* ge
                                                        pos11 = bottom - (y - 1 - each // x)* ge
                                                        mouse.click(pos00,pos11,2)
                                                        move = True
                                                        clicked[each] = 1
                                                        list_cue[each] = 10
                                                differences2 = set(list_blank_neighbor[point1]) - set(list_blank_neighbor[point2])
                                                for each in differences2:
                                                    if not clicked[each]:
                                                        pos00 = right - (x - 1 - each % x)* ge
                                                        pos11 = bottom - (y - 1 - each // x)* ge
                                                        mouse.click(pos00,pos11,1)
                                                        move = True
                                                        clicked[each] = 1
                                                 
                                            
                # 如果以上情况都没有，则靠猜了，随机点开（优先四个角）
                
                if not move:  
                    for i in range(2):          
                        if list_cue[i*(x-1)] == 9 and not clicked[i*(x-1)]:
                            pos00 = left + i * (x-1) * ge
                            pos11 = top
                            mouse.click(pos00,pos11,1)
                            clicked[i*(x-1)] = 1
                            move = True
                            print('guess:',i*(x-1),0)
                            break
                
                if not move:
                    #a = input("guess?")
                    #mouse.click(left, top - ge, 1)
                    for point in range(x*y):
                        if list_cue[point] == 9 and not clicked[point]:
                            guess_point = point
                            choosed = True
                            for j in range(8):
                                xx = int(1.5 * cos(j* pi/4))
                                yy = int(1.5 * sin(j* pi/4))
                                next_point = point + yy*x + xx
                                if ((point % x) + xx) in range(x) and ((point // x) + yy) in range(y):
                                    if list_cue[next_point] != 9:
                                        choosed = False
                                        break
                            if choosed:
                                guess_point = point
                                break
                    if guess_point == last_guess_point:
                        a = input("guess_point重复！")
                    pos00 = right - (x - 1 - guess_point % x)* ge
                    pos11 = bottom - (y - 1 - guess_point // x)* ge
                    mouse.click(pos00,pos11,1)
                    move = True
                    print('guess:',guess_point%x,guess_point//x)
                    last_guess_point = guess_point

                if not move:
                    print("not move!")
                    break
        if win:
            print("10次扫雷结束，成功率是：",win*10,"%  平均用时：", total_time/win, "s" )
        a = input("按任意键继续，按n/N退出：")
        if a == ('n' or 'N'):
            break


if __name__ == "__main__":
    main()

        

