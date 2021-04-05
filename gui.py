from tkinter import W,Tk,Frame,Button,Entry,Menu,Menubutton,Label,PhotoImage
import requests
import json
from pynput.keyboard import Listener
from PIL import Image,ImageTk
import time
import threading
import multiprocessing
import os

# url_register = 'http://123.57.200.185:8001/register'
# url_login = 'http://123.57.200.185:8001/login'
# url_createRoom = 'http://123.57.200.185:8001/createRoom'
# url_changeState = 'http://123.57.200.185:8001/changeState'
# url_getAll = 'http://123.57.200.185:8001/getAll'
# url_getRoom = 'http://123.57.200.185:8001/getRoom'
# url_delAll = 'http://123.57.200.185:8001/delAll'
# url_delRoom = 'http://123.57.200.185:8001/delRoom'
# url_delUser = 'http://123.57.200.185:8001/delUser'

url_register = 'http://127.0.0.1:8000/register'
url_login = 'http://127.0.0.1:8000/login'
url_createRoom = 'http://127.0.0.1:8000/createRoom'
url_changeState = 'http://127.0.0.1:8000/changeState'
url_getAll = 'http://127.0.0.1:8000/getAll'
url_getRoom = 'http://127.0.0.1:8000/getRoom'
url_delAll = 'http://127.0.0.1:8000/delAll'
url_delRoom = 'http://127.0.0.1:8000/delRoom'
url_delUser = 'http://127.0.0.1:8000/delUser'

def myHttpRequest(url:str,items:dict):
    req = requests.get(url,params=items)
    try:
        res = json.loads(req.content)
    except:
        res = 'failure'
        print('failure')
    return res

is_input_flag = False
# 表示该用户是否在输入
# 摸鱼的标准是，已有5秒未进行输入动作
time_last_press = time.time()
time_last_release = time.time()

class ListenerMod (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        def on_press(key):
            try:
                global time_last_press
                time_last_press = time.time()
            except:
                print('error')
        def on_release(key):
            try:
                global time_last_release
                time_last_release = time.time()
            except:
                print('error')
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

class CheckMod(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        global is_input_flag
        try:
            while (True):
                time.sleep(1)
                time_current = time.time()
                if time_last_release < time_last_press or time_current - time_last_release < 5:
                    is_input_flag = True
                else:
                    is_input_flag = False
        except:
            print('error')

class GUIMod(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.img_dict = {}
        self.data_room = []
        self.data_role = {'userName':'\0','state':'\0','roomName':'\0'}
        self.realRoot = None
        self.root = None
        self.rootFrame = None
        self.entryFrame = None

    def loadImg(self):
        self.img_dict['1'] = PhotoImage(file='img/咖啡.png')  # 空闲
        self.img_dict['2'] = PhotoImage(file='img/键盘.png')  # 打字中
        self.img_dict['3'] = PhotoImage(file='img/在线.png')  # 在线
        self.img_dict['4'] = PhotoImage(file='img/忙碌.png')  # 忙碌
        self.img_dict['5'] = PhotoImage(file='img/等待.png')  # 给我点时间，我要思考
        self.img_dict['6'] = PhotoImage(file='img/快进.png')  # 搞快点
        self.img_dict['7'] = PhotoImage(file='img/疑问.png')  # 令人困惑
        self.img_dict['8'] = PhotoImage(file='img/震惊.png')  # 令人震惊
        self.img_dict['9'] = PhotoImage(file='img/灯泡.png')  # 有想法了
        self.img_dict['10'] = PhotoImage(file='img/用户.png')  # 我是主角
        self.img_dict['11'] = PhotoImage(file='img/空白.png')

    def change_state(self,state_list:list):
        try:
           old = self.data_role['state'].split('_')
           if(self.data_role['state']=='\0' or self.data_role['userName']=='\0' or self.data_role['roomName']=='\0'):
               return
           for i in range(len(old)):
               if(state_list[i]=='-1'):
                   state_list[i] = old[i]
           new = '_'.join(state_list)
           if(new==self.data_role['state']):
               return
           myHttpRequest(url_changeState, {'userName': self.data_role['userName'], 'state': new})
        except:
            print('change_state error')
        
    def set_line(self, item: dict, frame: Frame):
        children = frame.winfo_children()
        children[0].configure(text=item['userName'])
        mark = item['state'].split('_')
        children[1].configure(image=self.img_dict[mark[0]])
        children[2].configure(image=self.img_dict[mark[1]])

    def get_role(self):
        for i in range(len(self.data_room)):
            if(self.data_room[i]['userName']==self.data_role['userName']):
                self.data_role['state'] = self.data_room[i]['state']
                break

    def rebuild(self):
        self.rootFrame.destroy()
        self.rootFrame = Frame(self.root, height=100, width=200)
        self.rootFrame.grid(row=2,column=0)
        for i in range(len(self.data_room)):
            item = self.data_room[i]
            f = Frame(self.rootFrame)
            f.grid(row=i,column=0,pady=3,sticky=W)
            mark = item['state'].split('_')
            Label(f, text=item['userName'],width=10).grid(row=0,column=0,padx=5)
            Label(f, image=self.img_dict[mark[0]],width=35).grid(row=0,column=1,padx=5)
            Label(f, image=self.img_dict[mark[1]],width=35).grid(row=0, column=2,padx=5)
            if(item['userName']==self.data_role['userName']):
                Label(f, image=self.img_dict['10'],width=35).grid(row=0,column=3,padx=5)
            else:
                Label(f, image=self.img_dict['11'],width=35).grid(row=0,column=3,padx=5)

    def report_keyboard(self):
        if (is_input_flag == True):
            self.change_state(['2', '-1'])
        else:
            self.change_state(['1', '-1'])

    def update(self):
        if(self.data_role['userName']!='\0' and self.data_role['roomName']!='\0'):
            self.report_keyboard()
            data_room_new = myHttpRequest(url_getRoom, {'roomName':self.data_role['roomName']})
            if (len(data_room_new) != len(self.data_room)):
                self.data_room =data_room_new
                self.rebuild()
            else:
                for i in range(len(self.data_room)):
                    if(self.data_room[i]!=data_room_new[i]):
                        self.set_line(data_room_new[i],self.rootFrame.winfo_children()[i])
                self.data_room = data_room_new
                self.get_role()

        self.root.after(1000, self.update)

    def run(self):
        self.realRoot = Tk()
        self.realRoot.attributes('-alpha', 0.75)
        self.realRoot.title('TRPGHelper')

        self.realRoot.protocol("WM_DELETE_WINDOW", lambda : os._exit(0))

        width = 260
        height = 400
        img = ImageTk.PhotoImage(Image.open('img/bg.png').resize((width, height)))
        l = Label(self.realRoot, image=img)
        l.grid(row=0,column=0)

        self.root = Frame(self.realRoot)
        self.root.grid(row=0,column=0)

        self.loadImg()
        self.entryFrame = Frame(self.root, height=50, width=120)
        self.rootFrame = Frame(self.root, height=100, width=120)

        self.entryFrame.grid(column=0)
        self.rootFrame.grid(row=2, column=0,sticky=W)

        ButtonRoomName = Button(self.entryFrame, height=1, text='房间')
        ButtonUserName = Button(self.entryFrame, height=1, text='用户')
        EntryRoomName = Entry(self.entryFrame, width=10)
        EntryUserName = Entry(self.entryFrame, width=10)

        MenuButtonState = Menubutton(self.entryFrame, text='选择状态',width=10)
        ms = Menu(MenuButtonState,tearoff=False)
        ms.add_command(label='我在线哦', command=lambda: self.change_state(['-1', '3']))
        ms.add_command(label='真的很忙', command=lambda: self.change_state(['-1', '4']))
        ms.add_command(label='等等我！', command=lambda: self.change_state(['-1', '5']))
        ms.add_command(label='搞快点！', command=lambda: self.change_state(['-1', '6']))
        ms.add_command(label='令人困惑', command=lambda: self.change_state(['-1', '7']))
        ms.add_command(label='瓦特法？', command=lambda: self.change_state(['-1', '8']))
        ms.add_command(label='懂了悟了', command=lambda: self.change_state(['-1', '9']))
        MenuButtonState.configure(menu=ms)

        def _call_roomNameButton(roomName):
            self.data_role['roomName'] = roomName

        def _call_userNameButton_right():
            myHttpRequest(url_delUser, {'userName': self.data_role['userName']})

        def _call_userNameButton_left(userName):
            if(userName!=self.data_role['userName']):
                self.change_state(['1', '4'])
            self.data_role['userName'] = userName
            try:
                if (self.data_role['userName'] != '\0'):
                    myHttpRequest(url_register, {'userName': self.data_role['userName']})
                    myHttpRequest(url_createRoom,
                                  {'userName': self.data_role['userName'], 'roomName': self.data_role['roomName']})
                    self.rebuild()
            except:
                print('userNameButton error')

        ButtonRoomName.bind("<Button-1>", lambda f: _call_roomNameButton(EntryRoomName.get()))
        ButtonUserName.bind("<Button-1>", lambda f: _call_userNameButton_left(EntryUserName.get()))
        ButtonUserName.bind("<Button-3>", lambda f: _call_userNameButton_right())

        ButtonRoomName.grid(column=0, row=0, ipady=2, pady=5, ipadx=2, padx=5)
        ButtonUserName.grid(column=0, row=1, ipady=2, pady=5, ipadx=2, padx=5)
        EntryRoomName.grid(column=1, row=0, pady=5, ipadx=2, padx=5)
        EntryUserName.grid(column=1, row=1, pady=5, ipadx=2, padx=5)
        MenuButtonState.grid(column=2, row=0, pady=5, ipadx=2, padx=5)

        self.root.after(1000, self.update)
        self.root.mainloop()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    try:
        thread1 = ListenerMod(1, "监听模块", 1)
        thread2 = CheckMod(2, "计算模块", 2)
        thread3 = GUIMod(3, "图形模块", 3)
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
        time.sleep(86400)
        print('over')
    except:
        print('sth wrong')




