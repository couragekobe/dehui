from django.shortcuts import render

# Create your views here.
# 此模块为收货地址管理模块

from .models import Address
from user.models import User

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证
from django.db import utils


@login_required(login_url='/user/login.html')
def add_address(request):
    '''添加收件人地址信息'''
    print(request.POST)
    if request.method == 'GET':
        return HttpResponseRedirect('.')
        # return render(request, 'user/register.html')
    elif request.method == 'POST':
        # consignee = models.CharField("收件人", max_length=20, null=False, default="any")
        # address = models.TextField("收货地址",null=False)
        # mobile = models.CharField("手机号", max_length=13, null=False)
        # is_default = models.BooleanField("是否为默认地址", default=False)
        # zipcode = models.CharField("邮编", max_length=6, default="000000")
        # alias = models.CharField("别名", max_length=50)  # 家，公司，学校等
        # user = models.ForeignKey(User)  # 外键关联用户信息

        consignee = request.POST.get('consignee', '')
        address = request.POST.get('address', '')
        mobile = request.POST.get('mobile', '')
        zipcode = request.POST.get('zipcode', '')
        alias = request.POST.get('alias', '')
        user = request.user  # 根据用户登陆的user, 找到当前用户

        # 判断是否有末填写信息
        if not (consignee and address and mobile):
            return HttpResponse("输入项不能为空")

        # 查看此用户是否已经注册过
        try:
            addr = Address(consignee=consignee, address=address, mobile=mobile,
                           zipcode=zipcode, alias=alias, user=request.user)
            addr.save()
        except utils.DatabaseError as e:
            pass
    return HttpResponseRedirect(".")
    #         return HttpResponse("添加用户地址失败: 数据库错误!!!")
    #     return HttpResponse("添加用户地址成功")
    # return HttpResponse("其它请求!")


@login_required(login_url='/user/login.html')
def list_address(request):
    return HttpResponse("list_address")


@login_required(login_url='/user/login.html')
def default(request):
    return HttpResponse("default")


@login_required(login_url='/user/login.html')
def delete_adress(request):
    return HttpResponse("delete_adress")


@login_required(login_url='/user/login.html')
def index(request):
    return render(request, 'address/index.html', locals())
    # return HttpResponse("index")
