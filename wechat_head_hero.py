#-*- coding：utf-8 -*-
import os
import sys
import subprocess
import threading
from threading import Barrier

import time
import re
from PIL import Image


from config import *
import search
import tecent_wx as wx

#截取图片
def pull_screenshot(num):
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open('temp'+num+'.png', 'wb')
    f.write(screenshot)
    f.close()

#截取问题所在位置图片，使用ocr识别
def split_img(num,c_width,c_height,left_top_point,right_bottom_point):
    im = Image.open("temp"+num+".png")
    im_size = im.size
    ratio_left = left_top_point[0]/c_width
    ratio_top = left_top_point[1]/c_height
    ratio_right = right_bottom_point[0]/c_width
    ratio_bottom = right_bottom_point[1]/c_height
    region = im.crop((int(im_size[0]*ratio_left),int(im_size[1]*ratio_top)
             ,int(im_size[0]*ratio_right),int(im_size[1]*ratio_bottom)))
    region.save("split"+num+".png");


def dump_device_info():
    size_str = os.popen('adb shell wm size').read()
    device_str = os.popen('adb shell getprop ro.product.model').read()
    density_str = os.popen('adb shell wm density').read()
    print("如果你的脚本无法工作，上报issue时请copy如下信息:\n**********\
        \nScreen: {size}\nDensity: {dpi}\nDeviceType: {type}\nOS: {os}\nPython: {python}\n**********".format(
            size=size_str.strip(),
            type=device_str.strip(),
            dpi=density_str.strip(),
            os=sys.platform,
            python=sys.version
    ))
def check_adb():
    flag = os.system('adb devices')
    if flag == 1:
        print('请安装ADB并配置环境变量')
        sys.exit()

def get_screen_size():
    size_str = os.popen('adb shell wm size').read()
    m = re.search('(\d+)x(\d+)', size_str)
    if m:
        width = m.group(1)
        height = m.group(2)
        return (int(width),int(height))


b = Barrier(2)

global result_html
global ans

def thread_search_question():
     #截取问题图片块
    split_img("0",c_width,c_height,q_left_top_point,q_right_bottom_point)
    keywords = ''.join(wx.img_to_str("0"))
    print(keywords)
    global result_html
    result_html = search.search_BaiDu(keywords)
    b.wait()
def thread_ans_img_to_str():
    #pull_screenshot("1")
    t = time.time()
    split_img("1",c_width,c_height,a_left_top_point,a_right_bottom_point)
    global ans
    ans = wx.img_to_str("1") 
    print(time.time()-t)
    b.wait()


def main():
    search.init_browser()
    while True:
        s_input = input("按非‘#’号键回车继续截屏。。")
        if s_input == '#':
            break
        #获取手机屏
        pull_screenshot("0")
        if open_browser: # 使用浏览器自查

            split_img("0",c_width,c_height,q_left_top_point,q_right_bottom_point)
            keywords = ''.join(wx.img_to_str("0"))
            search.search_BaiDu(keywords)
        else:
            #使用词频查询结果（可能不准）
            threads = [] 
            #使用线程执行操作
            threads.append(threading.Thread(target=thread_search_question))
            threads.append(threading.Thread(target=thread_ans_img_to_str))
            threads[0].start()
            threads[1].start()
            threads[0].join()
            threads[1].join()

            maxindex = 0
            maxx = 0
            minindex = len(ans)-1
            minx = 1000000
            i = 0
            for a in ans:
                ct = len(re.findall(a,result_html))
                if ct > maxx:
                    maxindex = i
                    maxx =  ct 
                if ct < minx:
                    minindex = i
                    minx = ct
                i= i+1
            print(ans)
            if len(ans)>0:
                print(ans[maxindex])
                print(ans[minindex])
    search.close()

if __name__ == '__main__':
    main()
    
   
