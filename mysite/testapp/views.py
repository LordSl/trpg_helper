from django.shortcuts import render
from django.http import HttpResponse
from . import models
import json

# 注册（用户）register不能重复
# 上线（用户）login
# 创建房间（用户 房间号）createRoom
# 改变状态（用户 改变后的状态码）changeState
# 获取所有人信息（）（后台）getAll
# 获取房间内信息（房间）（所有人）getRoom
# 注销（用户）（所有人）delUser
# 注销（房间）（后台）delRoom
# 注销（）（后台）delAll

# id 用户名userName 房间roomName 状态state

# state
# 1已注册，下线
# 2已登录，在线（空闲）
# 3打字中（检测键盘输入）
# 4临时有事，离开

def myHttpResponse(items):
        return HttpResponse(json.dumps(items))

def register(request):
    try:
        print(request.GET, ' register')
        userName = request.GET['userName']
        models.TRPGHelper.objects.create(userName=userName, state='1_4', roomName='\0')
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')


def login(request):
    try:
        print(request.GET,' login')
        userName = request.GET['userName']
        models.TRPGHelper.objects.filter(userName = userName).update(state='1_3')
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')

def createRoom(request):
    try:
        print(request.GET, ' createRoom')
        userName = request.GET['userName']
        roomName = request.GET['roomName']
        models.TRPGHelper.objects.filter(userName=userName).update(roomName=roomName)
        return myHttpResponse({'roomName':roomName})
    except:
        return myHttpResponse('failure')

def changeState(request):
    try:
        print(request.GET,' changeState')
        userName = request.GET['userName']
        state = request.GET['state']
        models.TRPGHelper.objects.filter(userName=userName).update(state=state)
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')

def getAll(request):
    try:
        print(request.GET, ' getAll')
        imf = models.TRPGHelper.objects.all()
        res = []
        for item in imf:
            dict = {}
            dict['userName'] = str(vars(item)['userName'])
            dict['state'] = str(vars(item)['state'])
            res.append(dict)
        return myHttpResponse(res)
    except:
        return myHttpResponse('failure')

def getRoom(request):
    try:
        print(request.GET, ' getRoom')
        roomName = request.GET['roomName']
        imf = models.TRPGHelper.objects.filter(roomName=roomName)
        res = []
        for item in imf:
            dict = {}
            dict['userName'] = str(vars(item)['userName'])
            dict['state'] = str(vars(item)['state'])
            res.append(dict)
        return myHttpResponse(res)
    except:
        return myHttpResponse('failure')

def delAll(request):
    try:
        print(request.GET,' delAll')
        models.TRPGHelper.objects.all().delete()
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')

def delRoom(request):
    try:
        print(request.GET,' delRoom')
        roomName = request.GET['roomName']
        models.TRPGHelper.objects.filter(roomName=roomName).delete()
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')

def delUser(request):
    try:
        print(request.GET,' delUser')
        userName = request.GET['userName']
        models.TRPGHelper.objects.filter(userName=userName).delete()
        return myHttpResponse('success')
    except:
        return myHttpResponse('failure')
