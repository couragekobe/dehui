from django.db import models
from django.shortcuts import render,redirect
from user.models import *
from django.http import HttpResponse, Http404
import re
# Create your models here.
from django.utils.deprecation import MiddlewareMixin
'''
    此文件为权限验证功能所使用的中间件
    权限列表为全局变量
'''
# 管理员权限列表
ADMINISTRATORPERMISSION = [
    '/administrators/(.*)',
    '/admin/(.*)',
    '/verify/(.*)',
    '/goods/(.*)'
]
# 卖家权限列表
SALLERSPERMISSION = [
    '/sale/(.*)',
    '/verify/(.*)',
    '/goods/(.*)',

]

# 买家权限列表
BUYERSPEMISSION = [
    '/user/(.*)',
    '/verify/(.*)',
    '/goods/(.*)',
    '/cart/(.*)',
    '/address/(.*)',
    '/favorite/(.*)',
]

# 路由白名单
WHITELIST = [
    '/(.*)/login',
    '/verify/(.*)',
    '/index.html',
    '/header.html',
    '/footer.html',
    "/"
]


# 用来验证权限的函数
def verrification(permissionList,next_path):
    for permission in permissionList:
        middle = False
        if re.match(permission,next_path):
            middle = True
            break
    if middle:
        return "通过验证"
    else:
        return "未通过验证"

# 权限验证中间件类
class Pemission(MiddlewareMixin):
    def process_request(self, request):
        next_path = request.path_info  # request.path_info方法是获取请求路由的方法
        for w_path in WHITELIST:
            if re.match(w_path, next_path):
                return
        # 判断用户是否已经登录,未登录转去登录路由
        try:
            username = request.session['user']
        except:
            username = False
        if not username:
            # 首先验证将要访问的路由分配给不同模块的登录页
            message1 = verrification(ADMINISTRATORPERMISSION, next_path)
            message2 = verrification(SALLERSPERMISSION, next_path)
            message3 = verrification(BUYERSPEMISSION, next_path)
            if message1 == "通过验证":
                return redirect('/administrators/login/')
            if message2 == "通过验证":
                return redirect('/sale/user/login/')
            if message3 == "通过验证":
                return redirect('/user/login/')
            # if next_path == :
            #     return
        user = User.objects.filter(username=username)[0]
        # 根据用户类型进行路由权限判断
        if user.usertype == 1:
            message = verrification(ADMINISTRATORPERMISSION,next_path)
            if message == "通过验证":
                # 返回值为空代表验证通过可去试图执行
                return
            else:
                # 验证不通过返回404页面
                raise Http404("无权访问此路由")
        if user.usertype == 2:
            message = verrification(SALLERSPERMISSION, next_path)
            if message == "通过验证":
                return
            else:
                raise Http404("无权访问此路由")
        if user.usertype == 3:
            message = verrification(BUYERSPEMISSION, next_path)
            if message == "通过验证":
                return
            else:
                raise Http404("无权访问此路由")

