import requests
import json

#'http://123.57.200.185:8001'
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
    print(type(res),res)
    return res

cmd = ''
while(cmd != 'q'):
    cmd = input('请输入命令\n')
    if (cmd=='r'):
        userName = input('请输入用户名\n')
        myHttpRequest(url_register,{'userName':userName})
    if (cmd == 'l'):
        userName = input('请输入用户名\n')
        myHttpRequest(url_login, {'userName': userName})
    if (cmd == 'cr'):
        userName = input('请输入用户名\n')
        roomName = input('请输入房间名\n')
        myHttpRequest(url_createRoom, {'userName': userName,'roomName':roomName})
    if (cmd=='cs'):
        userName = input('请输入用户名\n')
        state = input('请输入状态\n')
        myHttpRequest(url_changeState, {'userName': userName,'state':state})
    if (cmd == 'ga'):
        myHttpRequest(url_getAll, {})
    if (cmd == 'gr'):
        roomName = input('请输入房间名\n')
        myHttpRequest(url_getRoom, {})
    if (cmd == 'da'):
        myHttpRequest(url_delAll, {})
    if (cmd == 'dr'):
        roomName = input('请输入房间名\n')
        myHttpRequest(url_delRoom, {'roomName':roomName})
    if (cmd == 'du'):
        userName = input('请输入用户名\n')
        myHttpRequest(url_delUser, {'userName': userName})

print('over')