# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 14:19:56 2019
QQ群：476842922(欢迎加群讨论学习)
@author: Administrator
"""
# import sys, os
from pynput.keyboard import Controller, Key, Listener
import time
import _thread

is_input_flag = False
#表示该用户是否在输入
#摸鱼的标准是，已有>=5秒未进行输入动作

time_last_press = time.time()
time_last_release = time.time()

# 监听按压
def on_press(key):
    try:
        # print("正在按压:", format(key.char))
        global time_last_press
        time_last_press = time.time()
        print('press',time_last_press,'id',id(time_last_press))
    except AttributeError:
        print('error')

# 监听释放
def on_release(key):
    try:
        # print("已经释放:", format(key))
        global time_last_release
        time_last_release = time.time()
        print('release',time_last_release,'id',id(time_last_release))
    except:
        print('error')


# 开始监听
def start_listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def checker(threadName):
    try:
        while(True):
            time.sleep(5)
            time_current = time.time()
            if time_last_release < time_last_press:
                is_input_flag = True
            elif time_current -  time_last_release < 5:
                is_input_flag = True
            else:
                is_input_flag = False
            # print('{} - {} = {}'.format(time_current,time_last_release,time_current-time_last_release))
            print(is_input_flag,'id',id(time_last_press),'id',id(time_last_release))
    except:
        print('error')

if __name__ == '__main__':
    # 实例化键盘
    kb = Controller()

    # # 使用键盘输入一个字母
    # kb.press('a')
    # kb.release('a')

    # # 使用键盘输入字符串,注意当前键盘调成英文
    # kb.type("hello world")

    # 使用Key.xxx输入
    # kb.press(Key.space)
    _thread.start_new_thread(checker,('傻子',))

    # 开始监听
    start_listen()