from django.shortcuts import render,redirect

# Create your views here.


from django.contrib import auth
from django.contrib.auth import hashers  # 用户授权用户密码加密

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证

from django.db import utils
from .models import User
import verify

def login(request):
    '''用户登陆功能,先判断用户是否已经登陆，如果已经登陆过，则直接跳转到用户信息界面
       GET 请求时，返回登陆页面
       POST 请求时，检查用户提交的数据是否合法。如果合法，则
    '''
    if request.user.is_authenticated():  # 判断是否已经登陆过
        return redirect('/')

    if request.method == 'GET':
        # 确定查询字符串中next跳转的位置,如果有则在表单中加入next 隐藏值
        try:
            next = request.GET["next"]
        except:
            next = ''

        return render(request, "user/login.html", locals())
    elif request.method == 'POST':
        # 判断验证码是否正确,
        if not verify.isValidVerifycode(request):
            return HttpResponse("验证码输入有错")

        # 验证用户名和密码是否合法
        username=request.POST.get('username', '')
        password=request.POST.get('password', '')
        if not username or not password:
            return HttpResponse("用户名或密码不能为空")

        # 验证用户名和密码是否通过,通过返回此用户的User 数据对象
        user = auth.authenticate(request=request, username=username, password=password)

        # 确定跳转位置
        try:
            next = request.POST['next']
        except:
            next = '.'

        if user and user.is_active:  # 通过验证
            auth.login(request, user)  # 让用户信息与当前的request 请求进行关联，从此通过request.user可以访问此用户
            print("user: " + user.username + " is login!")
            return HttpResponseRedirect(next)
        else:
            return HttpResponse("用户名或密码不正确")


@login_required(login_url='/user/login.html')
def logout(request):
    '''退出登陆'''
    print("user: " + request.user.username + " is logout!")
    if request.method == 'GET':
        auth.logout(request)  # 用退登陆，将user 与 request 解绑
        return HttpResponseRedirect("/")

def register(request):
    '''用户注册'''
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')

        # 判断两次密码是否一致!
        if password != password2:
            return HttpResponse("两次密码不一致")

        # 判断是否有末填写信息
        if not (username and password and mobile and email):
            return HttpResponse("输入项不能为空")

        # 查看此用户是否已经注册过
        olduser = User.objects.filter(username=username)
        if olduser:
            return HttpResponse("该用户名已经存在")
        else:
            # 用当前密码，生成sha1 进行加密生成密文的字符串 password_sha1 准备存入数据库中
            password_sha1 = hashers.make_password(password, None, 'pbkdf2_sha1')   # 'pbkdf2_sha1'为加密串
            try:
                User.objects.create(username=username, nickname=username, password=password_sha1, mobile=mobile, email=email)
                print("用户注册:", username, "成功")
            except utils.DatabaseError as e:
                print("用户注册:", username, "失败！ 原因:", e)
                return HttpResponse("注册失败: 数据库错误!!!")
            return HttpResponse("注册成功")

@login_required(login_url='/user/login.html')
def mod_password(request):
    '''进入首页'''
    # changepwd
    return render(request, 'user/personal_password.html', locals())

@login_required(login_url='/user/login.html')
def index(request):
    '''用户首页'''
    # return render(request, 'user/index.html', locals())
    return render(request, 'user/personage.html', locals())

def test(request):
    '''测试用'''
    return render(request, 'user/personal_password.html')
