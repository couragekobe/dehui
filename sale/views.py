from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import hashers  # 用户授权用户密码加密
from goods.models import *
from user.models import *
from PIL import Image
import datetime
import json
import os
from order.models import *
from address.models import *
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证
# Create your views here.

#访问主页
def index(request):
    return render(request,'sale/home-page.html')

#登录
def login(request):
    if request.method == "GET":
        return render(request,'sale/login.html')
    if request.method == 'POST':
        username = request.POST.get('salename', '')     #接收用户名
        password = request.POST.get('spassword', '')    #接收密码
        code = request.session['verifycode'].lower()    #接收验证码
        new_verify = request.POST.get('verify_code').lower()
        #判断验证码
        if code != new_verify:
            code_message = '验证码错误'
            return render(request, "sale/login.html", locals())

        if username and password:
            # 使用django提供的验证方法，传入用户名和密码，会返回一个user对象
            user = auth.authenticate(username=username, password=password,usertype=2)
            if user is not None and user.is_active:
                auth.login(request,user)
                request.session['salename'] = user.username
                request.session['userid'] = user.id
                return redirect('/sale/')
            else:
                message ="用户名或密码错误"
                return render(request,"sale/login.html",locals())
        else:
            message="请输入用户名或密码"
            render(request, "sale/login.html", locals())

# 用户是否登录验证
def check_login_status(func):
    def wrapper(request, *args, **kwargs):
        # request.user.is_authenticated()是验证用户是否已经登录   之前用的是（）    这里应该是一个属性名
        if request.user.is_authenticated:
            # user = UserInfo.objects.get(username='asdfgh')
            # if user:
            #     request.user = user
            return func(request, *args, **kwargs)
        else:
            return render(request,"sale/login.html")
    return wrapper

# # 管理员退出
# @check_login_status
# def logout(request):
#     del request.session['salename']
#     auth.logout(request)
#     return HttpResponse("已经安全退出")


#卖家个人信息展示
@check_login_status
def info_(request):
    #从session中取卖家名
    salename = request.session.get('salename')
    print('session中的saleuser:', salename)
    #如果有用户名，从数据库中查询，取出所有信息
    if salename:
        users = User.objects.filter(username=salename)
        for user in users:
            print(user.username)
        content = {
            'name': user.username,
            'email': user.email,
            'mobile': user.mobile,
            'nickname':user.nickname,
        }
        return render(request, 'sale/saleuser.html', locals())
    return render(request, 'sale/login.html')

#如果get请求　将登录的用户信息返回页面
@check_login_status
def mod_info(request):
    if request.method == 'GET':
        #从session中取用户名
        salename = request.session.get('salename')
        print('session中的saleuser:', salename)
        if salename:
            #如果有　从Ｕｓｅｒ中查询
            users = User.objects.filter(username=salename)
            for user in users:
                print(user.username)
            content = {
                'name': user.username,
                'email': user.email,
                'mobile': user.mobile,
                'nickname':user.nickname
            }
            return render(request, 'sale/mod_info.html', locals())
        return render(request, 'sale/login.html')

#如果POST请求 将更改的个人信息和头像更改数据库　并保存　
@check_login_status
def mod_infoname(request):
    if request.method == 'POST':
        uname = request.session.get('salename')
        id = request.session.get('id')
        print('商户名',uname)
        print("ID:",id)
        # 从session中取用户名　并从user表中查询
        user = User.objects.filter(username=uname)[0]
        #接收新的用户名，昵称，邮箱，手机号
        new_name = request.POST.get('newname','')
        new_nickname = request.POST.get('newnickname','')
        new_email = request.POST.get('newemail','')
        new_mobile = request.POST.get('newmobile','')
        #判断是否有值
        if new_nickname:
            user.nickname = new_nickname
        if new_name:
            user.username = new_name
            #将新用户名存在session中替换原来的
            request.session["salename"] = user.salename
        if new_email:
            user.email = new_email
        if new_mobile:
            user.mobile = new_mobile
        user.save()
        #打印存session的用户名:
        print('Session:',user.username)

    return redirect('/sale/')

#修改卖家密码
@check_login_status
def mod_password(request):
    if request.method == 'GET':
        salename = request.session['salename']
        saleuser = User.objects.filter(username=salename)
        for su in saleuser:
            print('初始密码:',su.password)
        return render(request,'sale/mod_password.html')

    if request.method == 'POST':
        salename = request.session['salename']
        saleuser = User.objects.filter(username=salename)[0]
        #接收新密码
        spassword = request.POST.get('new_password')
        print('新密码',spassword)
        #接收再次输入的密码
        cspassword = request.POST.get('cnew_password')
        if spassword:
            #判断两次输入是否一样
            if spassword == cspassword:
                password_sha1 = hashers.make_password(spassword, None, 'pbkdf2_sha1')
                saleuser.password = password_sha1
                saleuser.save()
                return render(request,'sale/ok.html')
            else:
                salename = request.session['salename']
                saleuser = User.objects.filter(username=salename)
                for su in saleuser:
                    print('初始密码:', su.password)
                message = '两次输入密码不一致'
                return render(request,'sale/mod_password.html',locals())

        else:
            salename = request.session['salename']
            saleuser = User.objects.filter(salename=salename)
            for su in saleuser:
                print('初始密码:', su.spassword)
                message='请重新输入'
            return render(request,'sale/mod_password.html',locals())

#上传新商品
@check_login_status
def new_goods(request):
    #声明两个空列表，用于将图片名存在列表中，最终以json形式存储在数据库中
    goodsimagelist = []
    detailimageslist = []
    if request.method == 'GET':
        return render(request,'sale/new_goods.html')

    if request.method == 'POST':
        #获取商品的类型
        gtype = request.POST.get('gtype')
        print('gtypr=',gtype)
        goodstype = GoodsType.objects.get(title = gtype )
        print('goodstypeID',goodstype.id,goodstype.title)
        #获取用户的名字和id
        username = request.session.get('salename')
        userid = request.session.get('userid')
        print('username = ',username)
        user = User.objects.get(username=username,id=userid)
        print('userid = ',user.id)
        #将请求过来的产品标题等　存入数据库　先生成一个goods对象
        goods = Goods()
        goods.title = request.POST.get('title')
        goods.desc = request.POST.get('desc')
        goods.spec_name = request.POST.get('spec_name')
        goods.goods_type = goodstype
        goods.saller = user
        # 必须商品所有属性全部填写　才会上传
        if goods.title and goods.desc and goods.spec_name and goods.goods_type and goods.saller:
            request.session['goodstitle']=goods.title
            goods.save()
        else:
            return HttpResponse('请正确上传')
        request.session['goods_id'] = goods.id
        print('session中id:',goods.id)
        #从数据库中取出保存的商品id
        gds = Goods.objects.get(title=goods.title,id=goods.id)
        # request.session['goods_id'] = gds.id
        print(gds.id)
        #定义路径变量
        path = 'static/images/goods/%s/' % gds.id
        path2 =  'static/images/goods/%s/details/' % gds.id
        #判断是否有文件夹路径，没有的话创建
        if not os.path.exists(path) and not os.path.exists(path2):
            os.makedirs(path)
            os.makedirs(path2)

        #获取request过来的产品图片
        images = request.FILES.get('goods_images')
        if images:
            print('产品图片：', images)
            #打开产品图片
            image = Image.open(images)
            # img = Image.open(image)
            print("原始图片尺寸", image.size)
            # 进行按比例缩放，选择高质量模式
            image.thumbnail((96, 96), Image.ANTIALIAS)
            #获取前时间为
            filename = datetime.datetime.now()
            print(filename)
            #将当前时间按自定义格式设置为name变量
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            #保存图片在本地设置好的路径
            image = image.save(path + file_name + '.png')
            print('图片路径：', image)
            #设置存入数据库名称
            goodsimage = file_name + '.png'
            #将图片加入列表
            goodsimagelist.append(goodsimage)
            # 以json格式存入数据库
            jsonstr = json.dumps(goodsimagelist)
        #获取request过来的产品详情图
        images2 = request.FILES.get('detail_images')

        if images2:
            # 打开产品图片
            print('产品详情图片：', images2)
            image2 = Image.open(images2)
            print("原始图片尺寸", image2.size)
            # 进行按比例缩放，选择高质量模式
            image2.thumbnail((96, 96), Image.ANTIALIAS)
            #获取当前时间
            filename = datetime.datetime.now()
            print(filename)
            # 将当前时间按自定义格式设置为name变量
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            # 保存图片在本地设置好的路径
            image2 = image2.save(path2 + file_name + '.png')
            print('图片路径：', image2)
            # 设置存入数据库的图片名称
            detailimages = file_name + '.png'
            # 将图片加入列表
            detailimageslist.append(detailimages)
            # 以json格式存入数据库
            jsonstr2 = json.dumps(detailimageslist)
        #将两组json数据存入数据库
        goods.goods_images = jsonstr
        goods.detail_images = jsonstr2

        if goods.goods_images and goods.detail_images:
            goods.save()

        #创建一个商品规格的对象
        goodsspecification=GoodsSpecification()
        #获取请求过来的价格，库存等
        price = request.POST.get('price')
        spec_info = request.POST.get('spec_info')
        stock = request.POST.get('stock')
        if stock and spec_info and price:
            goodsspecification.stock = stock
            goodsspecification.price = price
            goodsspecification.spec_info = spec_info
            goodsspecification.goods = gds
            goodsspecification.save()
            return redirect('/sale/goods/mod_goods/')
        else:
            return HttpResponse('请正确上传')

#上架商品
@check_login_status
def new_shelves(request):
    #将is_delete和is_saller_empower都为false的去出来
    addGood = Goods.objects.filter(is_delete=False,is_saller_empower=False)
    for go in addGood:
        print("已下架商品：", go.title)
        #如果球球方式为get发那会给new_shekves.html页面
    if request.method == 'GET':
            return render(request, 'sale/new_shelves.html', locals())

    elif request.method == 'POST':
        for good in addGood:
            #获取商品标题和传递过来的{{ seller.id }}add的值
            title = request.POST.get(good.title)
            isAdmin = request.POST.get(str(good.id) + "add")
            #如果有　就将is_delete和is_saller_empower改为True表示上架
            if title and isAdmin == 'true':
                adgood = Goods.objects.filter(title = title,id=good.id)[0]
                adgood.is_delete = True
                adgood.is_saller_empower = True
                adgood.save()
        return redirect('/sale/goods/new_shelves')


#下架商品
@check_login_status
def closed_shelves(request):
    # 将is_delete和is_saller_empower都为True的去出来
    delGood = Goods.objects.filter(is_delete=True,is_saller_empower=True)
    for go in delGood:
        print("已上架商品：", go.title)
    if request.method == 'GET':
        return render(request, 'sale/closed_shelves.html', locals())

    elif request.method == 'POST':
        for good in delGood:
            # 获取商品标题和传递过来的{{ seller.id }}add的值
            print('已上架商品：', good.title)
            title = request.POST.get(good.title)
            isAdmin = request.POST.get(str(good.id) + "add")
            #如个满足条件，is_delete和is_saller_empower都为False表示下架
            if title and isAdmin == 'true':
                degood = Goods.objects.filter(id=good.id)[0]
                degood.is_delete = False
                degood.is_saller_empower = False
                degood.save()
        return redirect('/sale/goods/closed_shelves/')


#修改商品信息
@check_login_status
def mod_(request,title):

    if request.method == 'GET':
        print('成功')
        #生成两个表的对象
        goods = Goods.objects.get(title = title)
        goodgui = GoodsSpecification.objects.filter(goods = goods)
        #判断goods_images字段是否不等于２　因为如果为空[]占两个字符
        if len(goods.goods_images) !=2 :
            #将字段值通过json解析生成列表
            img_list = json.loads(goods.goods_images)
            print(img_list)
            print(img_list,type(img_list))
            #首图为第一个索引值为零
            head_img = img_list[0]
        #将商品详情图通过json解析
        if goods.detail_images:
            detail_list = json.loads(goods.detail_images)
        #将此商品的名称和id存在session中
        request.session['goodstitle'] = goods.title
        request.session['goods_id'] = goods.id
        return render(request, 'sale/mod_goods3.html', locals())


#商品展示预览
@check_login_status
def preview(request):
    if request.method == 'GET':
        title = request.session['goodstitle']
        print('存在session:', title)
        id = request.session['goods_id']
        print('存在session的ID:', id)
        goods = Goods.objects.get(id=id, title=title)
        print('goods对象：', goods.title)
        goodsdetail = GoodsSpecification.objects.filter(goods = goods)
        for gd in goodsdetail:
            print(gd.stock)
        return render(request,'sale/preview.html',locals())



#注销登录
@check_login_status
def logout(request):
    request.session.clear()
    auth.logout(request)
    return render(request, 'sale/login.html')

#删除产品图
@check_login_status
#将图片名称img_title传参过来
def del_img(request,img_title):
    #从session中取商品title和id
    title = request.session['goodstitle']
    id = request.session['goods_id']
    goods = Goods.objects.get(title=title,id=id)
    #取出goods.goods_imgages字段中的值
    img_list = goods.goods_images
    #json解析生成列表
    goods_image_list = json.loads(img_list)
    print(goods_image_list)
    #用list.remove方法删除字段列表中的元素
    goods_image_list.remove(img_title)
    print('删除后的列表',goods_image_list)
    #转为json数据存入数据库中
    jsonstr_list = json.dumps(goods_image_list)
    goods.goods_images = jsonstr_list
    goods.save()
    #查询图片所在路径删除图片
    path = 'static/images/goods/%s/' % goods.id
    os.remove(path + img_title)
    return redirect('/sale/goods/mod_goods/')


#删除产品详情图
@check_login_status
def del_detail_img(request,detail_img_title):
    title = request.session['goodstitle']
    id = request.session['goods_id']
    goods = Goods.objects.get(title=title, id=id)
    detail_img_list = goods.detail_images
    detail_image_list = json.loads(detail_img_list)
    print(detail_image_list)
    detail_image_list.remove(detail_img_title)
    print('删除后的列表', detail_image_list)
    jsonstr_detail_list = json.dumps(detail_image_list)
    goods.detail_images = jsonstr_detail_list
    goods.save()
    path2 = 'static/images/goods/%s/details/' % goods.id
    os.remove(path2 + detail_img_title)
    return redirect('/sale/goods/mod_goods/')

@check_login_status
def mod_goods(request):
    if request.method == 'GET':
        print('成功')
        title=request.session['goodstitle']
        print('session中名字',title)
        id = request.session['goods_id']
        goods = Goods.objects.get(title = title,id=id)
        goodgui = GoodsSpecification.objects.filter(goods = goods)
        print('列表长度',len(goods.goods_images))

        if len(goods.goods_images) != 2:
            img_list = json.loads(goods.goods_images)
            print(img_list)
            print(img_list,type(img_list))
            head_img = img_list[0]
        if goods.detail_images:
            detail_list = json.loads(goods.detail_images)
        return render(request, 'sale/mod_goods3.html', locals())



#删除规格
@check_login_status
def del_gui(request,gui_id):
    #将传递过来的规格ｉd，在数据库总查询，查询匹配后删除
    gds = GoodsSpecification.objects.get(id=gui_id)
    gds.delete()
    return redirect('/sale/goods/mod_goods/')

#添加产品图和详情图
@check_login_status
def mod_image(request):
    if request.method=='POST':
        #通过session获取当前商品的id 和title
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title,id)
        goods = Goods.objects.get(id=id,title=title)
        goods_images = request.FILES.get('goods_img','')
        detail_images = request.FILES.get('detail_img', '')
        #取出goods_images和detail_iamges字段的值
        imagelist= goods.goods_images
        detaillist = goods.detail_images
        goodsimagelist = json.loads(imagelist)  # 解析json数据
        detailimagelist=json.loads(detaillist)
        print('商品产品图列表', goodsimagelist)
        print('商品详情图列表',detailimagelist)
        #设置两个路径
        path = 'static/images/goods/%s/' %id
        path2 = 'static/images/goods/%s/details/' %id
        #判断是否存在以商品id命名的文件夹，不存在就创建
        if not os.path.exists(path) and not os.path.exists(path2):
            os.makedirs(path)
            os.makedirs(path2)
        if goods_images:
            print('产品图：',goods_images )
            #打开图片
            image = Image.open(goods_images)
            print("原始图片尺寸", image.size)
            #将图片按比例缩放，设置存储质量
            image.thumbnail((96, 96), Image.ANTIALIAS)
            #将当前时间设为存储名并设置存储格式
            filename = datetime.datetime.now()
            print(filename)
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            image.save(path + file_name + '.png')
            #设置存储在数据库字段中的图片名称
            goodsimage = file_name + '.png'
            print('图片title：', goodsimage)
            #村进列表中
            goodsimagelist.append(goodsimage)
            jsonstr = json.dumps(goodsimagelist)  # 以json格式存入数据库
            goods.goods_images = jsonstr
            goods.save()

        if detail_images:
            #同goods_images
            print('产品详情图：', detail_images)
            image2 = Image.open(detail_images)
            print("原始图片尺寸", image2.size)
            image2.thumbnail((96, 96), Image.ANTIALIAS)
            filename = datetime.datetime.now()
            print(filename)
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            image2.save(path2 + file_name + '.png')
            detailimage = file_name + '.png'
            print('详情图片title：', detailimage)
            detailimagelist.append(detailimage)
            jsonstr2 = json.dumps(detailimagelist)  # 以json格式存入数据库
            goods.detail_images = jsonstr2
            goods.save()
        return redirect('/sale/goods/mod_goods/')

#修改标题产品名
@check_login_status
def mod_title(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title,id)
        goods = Goods.objects.get(id=id,title=title)
        title = request.POST.get('new_title')
        # 取新的title desc spec_name　更新字段　
        if title:
            goods.title = title
        desc = request.POST.get('new_desc')
        if desc:
            goods.desc = desc
        spec_name = request.POST.get('new_spec_name')
        if spec_name:
            goods.spec_name = spec_name
        goods.save()
        request.session['goodstitle'] = goods.title
        return redirect('/sale/goods/mod_goods/')

#修改规格
@check_login_status
def mod_price(request):
    if request.method == 'POST':
        gds_id = request.POST.get('gds_id')
        gds = GoodsSpecification.objects.get(id=gds_id)
        price = request.POST.get('new_price')
        # 取新的商品规格　更新字段
        if price:
            gds.price = price

        stock =request.POST.get('new_stock')
        if stock:
            gds.stock = stock

        spec_info = request.POST.get('new_spec_info')
        if spec_info:
            gds.spec_info = spec_info

        gds.save()
        return redirect('/sale/goods/mod_goods/')


#添加新规格
@check_login_status
def new_price(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title, id)
        goods = Goods.objects.get(title=title,id=id)
        gds = GoodsSpecification()
        spec_info = request.POST.get('spec_info')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        #规格必须所有字段都填充
        if stock and price and spec_info:
            gds.price = price
            gds.spec_info = spec_info
            gds.stock = stock
            gds.goods = goods
            gds.save()
            return redirect('/sale/goods/mod_goods/')

        else:
            return HttpResponse('请正确输入')


@check_login_status
def new_preview(request):
    if request.method == 'GET':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title, id)
        goods = Goods.objects.get(title=title, id=id)
        return render(request,'sale/product_details.html',locals())

#插入产品图
@check_login_status
def insert_img(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title, id)
        goods = Goods.objects.get(id=id, title=title)
        goods_images = request.FILES.get('insert_img', '')
        img_title = request.POST.get('img_title','')
        print('商品图片title:',img_title)
        #取商品的goods_images字段
        imagelist = goods.goods_images
        # 解析json数据
        goodsimagelist = json.loads(imagelist)
        #取当前商品图片名称所在列表中的索引位置
        img_index = goodsimagelist.index(img_title)
        #差在后面　所以索引加一
        img_index = img_index + 1
        print('商品图片索引', img_index)
        path = 'static/images/goods/%s/' % id
        if goods_images:
            print('产品图：',goods_images )
            image = Image.open(goods_images)
            print("原始图片尺寸", image.size)
            image.thumbnail((96, 96), Image.ANTIALIAS)
            filename = datetime.datetime.now()
            print(filename)
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            image.save(path + file_name + '.png')
            goodsimage = file_name + '.png'
            print('图片title：', goodsimage)
            #插入列表中
            goodsimagelist.insert(img_index,goodsimage)
            jsonstr = json.dumps(goodsimagelist)  # 以json格式存入数据库
            goods.goods_images = jsonstr
            goods.save()
        return redirect('/sale/goods/mod_goods/')

#插入详情图
@check_login_status
def insert_detail_img(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        print('存在session:', title, id)
        goods = Goods.objects.get(id=id, title=title)
        detail_images = request.FILES.get('insert_detail_img', '')
        detail_title = request.POST.get('detail_title','')
        print('商品详情图title:',detail_title)
        detailimagelist = goods.detail_images
        detailimagelist = json.loads(detailimagelist)  # 解析json数据
        img_index = detailimagelist.index(detail_title)
        img_index = img_index + 1
        print('商品图片索引', img_index)
        path2 = 'static/images/goods/%s/details/' %id
        if detail_images:
            print('产品图：',detail_images )
            image = Image.open(detail_images)
            print("原始图片尺寸", image.size)
            image.thumbnail((96, 96), Image.ANTIALIAS)
            filename = datetime.datetime.now()
            print(filename)
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            image.save(path2 + file_name + '.png')
            goodsimage = file_name + '.png'
            print('图片title：', goodsimage)
            #插入列表中
            detailimagelist.insert(img_index,goodsimage)
            jsonstr = json.dumps(detailimagelist)  # 以json格式存入数据库
            goods.detail_images = jsonstr
            goods.save()
        return redirect('/sale/goods/mod_goods/')

#修改产品图
@check_login_status
def mod_goods_img(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        goods = Goods.objects.get(title=title, id=id)
        img_list = goods.goods_images
        goods_image_list = json.loads(img_list)
        #接收传递来的商品图片title
        img_title = request.POST.get('img_title')
        print('传递过来的图片title:',img_title)
        #接受传递来的新图片
        mod_goods_image = request.FILES.get('set_img')
        #用老图片的title取到索引位置
        img_index = goods_image_list.index(img_title)
        print('索引值为：',img_index)
        #设置路径
        path = 'static/images/goods/%s/' %id
        print('path:',path)
        #存入数据库并命名设置格式
        if mod_goods_image:
            image = Image.open(mod_goods_image)
            image.thumbnail((96, 96), Image.ANTIALIAS)
            filename = datetime.datetime.now()
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            print('存储图片名：',file_name)
            image.save(path + file_name + '.png')
            goodsimage = file_name + '.png'
            #更新看列表的索引值
            goods_image_list[img_index] = goodsimage
            jsonstr_list = json.dumps(goods_image_list)
            goods.goods_images = jsonstr_list
            goods.save()
            #删除原图片
            os.remove(path + img_title)
        return redirect('/sale/goods/mod_goods/')


#修改详情图
@check_login_status
def mod_detail_img(request):
    if request.method == 'POST':
        title = request.session['goodstitle']
        id = request.session['goods_id']
        goods = Goods.objects.get(title=title, id=id)
        img_list = goods.detail_images
        detail_image_list = json.loads(img_list)
        img_title = request.POST.get('deatil_title')
        mod_detail_image = request.FILES.get('set_detail_img')
        img_index = detail_image_list.index(img_title)
        print('索引值为：',img_index)
        #设置详情图存储路径
        path = 'static/images/goods/%s/details/' %id
        print('path:',path)
        if mod_detail_image:
            image = Image.open(mod_detail_image)
            image.thumbnail((96, 96), Image.ANTIALIAS)
            filename = datetime.datetime.now()
            file_name = filename.strftime("%Y%m%d_%H%M%S")
            print('存储图片名：',file_name)
            image.save(path + file_name + '.png')
            goodsimage = file_name + '.png'
            detail_image_list[img_index] = goodsimage
            jsonstr_list = json.dumps(detail_image_list)
            goods.detail_images = jsonstr_list
            goods.save()
            #删除原图片
            os.remove(path + img_title)
        return redirect('/sale/goods/mod_goods/')


# 显示全部订单
@login_required(login_url='/user/login/')
def order_list(request):
    if request.method == "GET":
        orders = Order.objects.filter(sale_user=request.user, status__gte=2)
        order_goods_list = []
        for new_order in orders:
            order_goodss = OrderGoods.objects.filter(order=new_order)
            for order_goods in order_goodss:
                order_goods.tprice = float(order_goods.amount) * float(order_goods.price)
                try:
                    s = order_goods.goods.goods_images
                    goods_images = eval(s)
                    order_goods.head_image = '/images/goods/' + str(order_goods.goods.id) + '/' + goods_images[0]
                except:
                    order_goods.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
                if order_goods.order.status == 2:
                    order_goods.status_w = "待发货"
                    order_goods.status_ws = "确认发货"
                if order_goods.order.status == 3:
                    order_goods.status_w = "配送中"
                    order_goods.status_ws = "完成交易"
                if order_goods.order.status == 4:
                    order_goods.status_w = "交易完成"
                    order_goods.status_ws = ""
                order_goods.tprice = float(order_goods.amount) * float(order_goods.price)
                order_goods_list.append(order_goods)
        return render(request, "sale/sale_myOrder.html",locals())

# 卖家状态改变
def sale_order_change(request, status ,orderid):
    # 发货操作
    if int(status) == 2:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 3
        change_order.save()
        return redirect('/sale/order_list')
    # 配送完成操作
    if int(status) == 3:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 4
        change_order.save()
        return redirect('/sale/order_list')
    # 显示历史订单
    if int(status) == 4:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 4
        change_order.save()
        return redirect('/sale/order_list')