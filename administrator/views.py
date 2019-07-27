import datetime
import re

from django.shortcuts import render,redirect
from django.http import HttpResponse
import logging
from django.contrib import auth
from user.models import *
from goods.models import *
from verify.views import *
from django.contrib.auth.hashers import make_password,check_password
from user.models import *
# Create your views here.

#定義一個字符串 用於驗證密碼 生成隨機加密密碼
auth_check = "laksjdflajskfjlaj"

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
            return HttpResponse("用户未登录")
    return wrapper


# 管理员主页-审核商品上架
def managementHome(request):
    # 从数据库取出所有卖家已经上架的商品
    addGoods = Goods.objects.filter(is_delete=False,is_saller_empower=True, is_admin_empower=False)
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    # 未登录不提供任何服务
    if not Auser:
        return redirect("/administrators/login")
    if request.method == "GET":
        # 将待管理员上架的商品传输到前端
        return render(request, "goodsManagement/index.html", locals())
    elif request.method == "POST":
        # 将管理员已审核上架的商品在数据库中将字段 is_admin_empower改为 True 代表管理员已通过审核
        for good in addGoods:
            title = request.POST.get(good.title)
            isAdmin = request.POST.get(str(good.id) + "add")
            if title and isAdmin == "true":
                adgood = Goods.objects.filter(title=title, id=good.id)[0]
                adgood.is_admin_empower = True
                adgood.save()
        return redirect("/administrators/home/")

# 商品管理页-本模块只提供搜索服务
def searchGoods(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == "GET":
        # 提供静态网页
        resp = render(request, 'goodsManagement/commodity.html', locals())
        resp.delete_cookie("uname")
        return resp
    if request.method == "POST":
        # 获取输入的用户信息存储到 cookie 中备用
        uname = request.POST.get("uname")
        user = User.objects.filter(username=uname)
        if user:
            userr = user[0]
            resp = redirect("/administrators/closedGoods")
            resp.set_cookie("uname", userr.username, 60 * 60 * 365)
            return resp
        else:
            m = "用户名不存在"
            return render(request, "goodsManagement/commodity.html", locals())
# 商品管理页-下架商品
def closedGoods(request):
    try:
        Auser = request.session["user"]
        uname = request.COOKIES["uname"]
    except :
        Auser = False
        uname = False
        logging.warning("管理员用户未登录或未找到商家信息")
    if not Auser:
        return redirect("/administrators/login")
    # 如未从cookie中去到用户信息,转到搜索页面
    if not uname:
        return redirect("/administrators/searchGoods")
    user = User.objects.filter(username=uname, usertype=2)
    # 判断输入的用户是否是 商家
    if not user:
        m = "输入用户类型错误"
        return render(request, "goodsManagement/commodity.html", locals())
    if not Auser:
        return redirect("/administrators/login")
    userr = user[0]
    goods = Goods.objects.filter(saller=userr.id,is_delete=False,is_admin_empower=True,is_saller_empower=True)
    goodsd = Goods.objects.filter(saller=userr.id,is_delete=True,is_admin_empower=True,is_saller_empower=True)
    if request.method == "GET":
        # 判断用户是否被禁用，根据判断得出要给前端的用户管理的选项(封禁/解禁)
        if (userr and goods) and userr.is_delete==False:
            ms = "是否封禁"
            return render(request, "goodsManagement/commodity.html", locals())
        if (userr and goods) and userr.is_delete == True:
            ms = "是否解禁"
            return render(request, "goodsManagement/commodity.html", locals())
        if not(userr and goods) and userr.is_delete==False:
            m = "没有任何数据了"
            ms = "是否封禁"
            return render(request, "goodsManagement/commodity.html", locals())
        if not(userr and goods) and userr.is_delete == True:
            m = "没有任何数据了"
            ms = "是否解禁"
            return render(request, "goodsManagement/commodity.html", locals())
    if request.method == "POST":
        if (userr and goods) or userr:
            dname = request.POST.get(str(userr.id) + "del")
            # 处理用户封禁/解禁业务
            if dname=="是否封禁":
                delid = request.POST.get(str(userr.id))
                delid = int(delid)
                deluser = User.objects.filter(id=delid)[0]
                deluser.is_delete = True
                deluser.save()
                resp = redirect("/administrators/searchGoods")
                resp.delete_cookie("uname")
                return resp
            if dname=="是否解禁":
                delid = request.POST.get(str(userr.id))
                delid = int(delid)
                deluser = User.objects.filter(id=delid)[0]
                deluser.is_delete = False
                deluser.save()
                resp = redirect("/administrators/searchGoods")
                resp.delete_cookie("uname")
                return resp
            # 处理用户商品的下架
            if userr and goods:
                for good in goods:
                    title = request.POST.get(good.title)
                    isAdmin = request.POST.get(str(good.id) + "add")
                    if title and isAdmin == "true":
                        Good = Goods.objects.filter(title=title, id=good.id)[0]
                        Good.is_saller_empower = False
                        Good.is_admin_empower = False
                        Good.save()
                        return redirect("/administrators/closedGoods")


# 分类管理页-本模块只提供搜索服务
def searchClassification(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == "GET":
        resp = render(request, 'classifiedManagement/classified.html',locals())
        resp.delete_cookie("classified")
        return resp
    if request.method == "POST":
        classified = request.POST.get("classified")
        goodTypes = GoodsType.objects.filter(title=classified)
        if goodTypes:
            goodType = goodTypes[0]
            # 分类名称可能为中文，这里存取cookie是需要进行编码
            newuser = goodType.title.encode('utf-8').decode('latin-1')
            resp = redirect("/administrators/closedClassification")
            resp.set_cookie("classified",newuser)
            return resp
        else:
            m = "此分类不存在"
            return render(request, 'classifiedManagement/classified.html', locals())
# 分类管理页-删除分类
def closedClassification(request):
    try:
        Auser = request.session["user"]
        classified = request.COOKIES["classified"].encode('latin-1').decode('utf-8')
    except:
        Auser = False
        classified = False
        logging.warning("管理员用户未登录或未找到分类信息")
    if not Auser:
        return redirect("/administrators/login")
    if not classified:
        return redirect("/administrators/searchClassification")

    goodsTypes = GoodsType.objects.filter(title=classified)
    if not goodsTypes:
        m = "输入错误"
        return render(request, 'classifiedManagement/classified.html', locals())
    if not Auser:
        return redirect("/administrators/login")
    goodsType = goodsTypes[0]
    if request.method == "GET":
        if goodsType and (goodsType.is_delete == False):
            ms = "是否封禁"
            goods = Goods.objects.filter(goods_type=goodsType.id)
            return render(request, 'classifiedManagement/classified.html', locals())
        if goodsType and (goodsType.is_delete == True):
            ms = "是否恢复"
            goods = Goods.objects.filter(goods_type=goodsType.id)
            return render(request, 'classifiedManagement/classified.html', locals())
        else:
            m = "没有任何数据了"
            return render(request, 'classifiedManagement/classified.html', locals())
    if request.method == "POST":
            title = request.POST.get(str(goodsType.id))
            isAdmin = request.POST.get(str(goodsType.id) + "del")
            # 处理分类的封禁业务
            if title and isAdmin == "是否封禁":
                goodstype = GoodsType.objects.filter(id=int(title))[0]
                goodstype.is_delete = True
                goodstype.save()
                goods = Goods.objects.filter(goods_type=goodstype.id)
                for good in goods:
                    good.is_delete = True
                    good.save()
                m = "已封禁"
                resp = render(request, 'classifiedManagement/classified.html', locals())
                resp.delete_cookie("classified")
                return resp
            # 处理用户的解禁任务
            if title and isAdmin == "是否恢复":
                goodstype = GoodsType.objects.filter(id=int(title))[0]
                goodstype.is_delete = False
                goods = Goods.objects.filter(goods_type=goodstype.id)
                for good in goods:
                    good.is_delete = False
                    good.save()
                goodstype.save()
                m = "已解禁"
                resp = render(request, 'classifiedManagement/classified.html', locals())
                resp.delete_cookie("classified")
                return resp
            else:
                return HttpResponse("出现未知错误")
# 分类管理页-增加分类
def increaseClassification(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == "GET":
        return render(request, 'classifiedManagement/addclassified.html', locals())
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        goodstype = GoodsType.objects.filter(title=title)
        if goodstype:
            m = "分类名不可重复"
            return render(request, 'classifiedManagement/addclassified.html', locals())
        goodstype = GoodsType.objects.create(title=title, desc=desc)
        goodstype.save()
        return redirect("/administrators/searchClassification")

# 用户管理页-增加卖家
def increaseSaller(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == 'GET':
        return render(request,"userManagement/increaseSaller.html",locals())
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('upassword')
        password2 = request.POST.get('upassword2')
        email = request.POST.get('uemail')
        uphone = request.POST.get('uphone')
        old_username = User.objects.filter(username=uname)
        old_usermobile = User.objects.filter(mobile=uphone)
        if old_username:
            m = "用户名已存在"
            return render(request,"userManagement/increaseSaller.html",locals())
        if old_usermobile:
            m = "手机号已被注册"
            return render(request,"userManagement/increaseSaller.html",locals())
        if password != password2:
            m = "两次密码输入不一致"
            return render(request, "userManagement/increaseSaller.html", locals())
        # 此处使用 加密加密包 make_password 使密码在数据库为密文存储
        # 参数1 密码
        # 参数2 随机字符串
        # 参数3 加密的方法
        newpassword = make_password(password,auth_check,'pbkdf2_sha1')
        new_user = User.objects.create(username=uname, password=newpassword, email=email, usertype=2, mobile=uphone)
        new_user.save()
        m = "新商户注册成功"
        return render(request,"userManagement/increaseSaller.html",locals())
# 用户管理页-修改密码
def modPassword(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == 'GET':
        return render(request, "userManagement/modPassword.html", locals())
    if request.method == 'POST':
        uname = request.POST.get('uname')
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        newpassword2 = request.POST.get('newpassword2')
        oldUser = User.objects.filter(username=uname)
        # check_password的參數
        # 參數1: 明文  參數2: 密文
        # 返回值: True/False
        if not check_password(oldpassword,oldUser[0].password):
            m = "用户名或密码错误,无权更改"
            return render(request, "userManagement/modPassword.html", locals())
        if newpassword != newpassword2:
            m = "两次密码输入不一致"
            return render(request, "userManagement/modPassword.html", locals())
        new_user_pwd = make_password(newpassword, auth_check, 'pbkdf2_sha1')
        newUser = User.objects.filter(username=uname)[0]
        newUser.password = new_user_pwd
        newUser.save()
        m = "密码修改成功"
        return render(request, "userManagement/modPassword.html", locals())

# 注意此数据为全局数据，重启服务后 之前所有改动将无效
# 轮播图数据
banner = [
    ("product_list.html?typeid=3", "/static/images/banner/index_banner1.jpg"),
    ("product_list.html?typeid=1", "/static/images/banner/index_banner2.jpg"),
    ("product_list.html?typeid=3", "/static/images/banner/index_banner3.jpg"),
    ("product_list.html?typeid=1", "/static/images/banner/index_banner4.jpg"),
    ("product_list.html?typeid=2", "/static/images/banner/index_banner5.jpg"),
]

# 特别推荐数据
recommend = [
    ('product_details.html?typeid=2&goodid=958', '/static/images/index/index_Sbanner_img1.png'),
    ('product_details.html?typeid=3&goodid=976', '/static/images/index/index_Sbanner_img2.png'),
    ('product_details.html?typeid=1&goodid=942', '/static/images/index/index_Sbanner_img3.png'),
]


# 分类推荐数据
type_list = [
    {
        'title' : '背包',
        'link' : '/goods/list?1',
        'goods_list' : [
            ('UREVO', '活力学院休闲双肩包', '￥6688.00', 'product_details.html?typeid=2&goodid=957', '/static/images/index/index_bp1.png'),
            ('Grinder 牛津休闲双肩包', '￥6688.00', 'product_details.html?typeid=2&goodid=956', '/static/images/index/index_bp2.png'),
            ('90分户外休闲双肩包', '￥68.00', 'product_details.html?typeid=2&goodid=958', '/static/images/index/index_Sbanner_img1.png'),
        ]
    },
    {
        'title': '拉杆箱',
        'link': '/goods/list?2',
        'goods_list': [
            ('90分旅行箱 1A', '与你走向更远的的地方', '￥6688.00', 'product_details.html?typeid=1&goodid=942', '/static/images/index/index_Sbanner_img3.png'),
            ('与爱箱随 一路精彩', '￥6688.00', 'product_details.html?typeid=1&goodid=947', '/static/images/index/index_trunk1.png'),
            ('让美好旅行触手可及', '￥68.00', 'product_details.html?typeid=1&goodid=945', '/static/images/index/index_trunk2.png'),
        ]
    },
    {
        'title': '手提包',
        'link': '/goods/list?3',
        'goods_list': [
            ('时尚都市菱格双肩包', '经典百搭 时尚优雅', '￥6688.00', 'roduct_details.html?typeid=3&goodid=974', '/static/images/index/index_hb1.png'),
            ('CARRYO 轻奢级牛皮水桶包', '￥6688.00', 'product_details.html?typeid=3&goodid=976','/static/images/index/index_Sbanner_img2.png'),
            ('英伦复古轻奢级马鞍包', '￥68.00', 'product_details.html?typeid=3&goodid=975', '/static/images/index/index_hb2.png'),
        ]
    },
]

# 处理图片的函数
def store_pictutes(page):
    file = page
    path = 'static/images/banner/'
    image = Image.open(file)
    image.thumbnail((1920,768),Image.ANTIALIAS)
    time_now = datetime.datetime.now()
    file_name = time_now.strftime("%Y%m%d_%H%M%S")
    store_file = path+file_name+'.png'
    image.save(store_file)
    return store_file

#买家首页-更改后的预览页面
def index(request):
    if request.method == 'GET':
        return render(request, 'index/index.html', globals())
#首页管理-轮播图修改
def bannerManagement(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == 'GET':
        types = GoodsType.objects.all()
        return render(request,'goodsManagement/bannerManagement.html',locals())
    if request.method == 'POST':
        #修改轮播图
        NO1_page = request.FILES.get('NO1_page')
        NO2_page = request.FILES.get('NO2_page')
        NO3_page = request.FILES.get('NO3_page')
        NO4_page = request.FILES.get('NO4_page')
        NO5_page = request.FILES.get('NO5_page')
        NO1_type = request.POST.get('NO1_type')
        NO2_type = request.POST.get('NO2_type')
        NO3_type = request.POST.get('NO3_type')
        NO4_type = request.POST.get('NO4_type')
        NO5_type = request.POST.get('NO5_type')
        if not(NO1_page):
            m = '请上传五张图片并选择类型'
            return render(request, 'goodsManagement/bannerManagement.html', locals())
        submit_type = request.POST.get('submit_type')
        if not submit_type:
            m = '请选择提交类型'
            return render(request, 'goodsManagement/bannerManagement.html',locals())
        # 图片进行处理 得到想要的尺寸并存储起来
        img_link1 = store_pictutes(NO1_page)
        img_link2 = store_pictutes(NO2_page)
        img_link3 = store_pictutes(NO3_page)
        img_link4 = store_pictutes(NO4_page)
        img_link5 = store_pictutes(NO5_page)
        if submit_type == "修改":
            # 修改全局下的列表
            global banner
            banner = [
                ("product_list.html?typeid="+NO1_type, '/'+img_link1),
                ("product_list.html?typeid="+NO2_type, '/'+img_link2),
                ("product_list.html?typeid="+NO3_type, '/'+img_link3),
                ("product_list.html?typeid="+NO4_type, '/'+img_link4),
                ("product_list.html?typeid="+NO5_type, '/'+img_link5),
            ]
            m = '轮播图修改完成'
            return render(request, 'goodsManagement/bannerManagement.html', {'m': m})
        if submit_type == "预览":
            # 创建新的列表用作提供预览的数据
            banner_c = [
                ("product_list.html?typeid="+NO1_type, '/'+img_link1),
                ("product_list.html?typeid="+NO2_type, '/'+img_link2),
                ("product_list.html?typeid="+NO3_type, '/'+img_link3),
                ("product_list.html?typeid="+NO4_type, '/'+img_link4),
                ("product_list.html?typeid="+NO5_type, '/'+img_link5),
            ]
            return render(request, 'index/index.html', {'banner': banner_c})

#首页管理-新品推荐管理
def recommendManagement(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == 'GET':
        types = GoodsType.objects.all()
        return render(request,'goodsManagement/recommendMannagement.html',locals())
    if request.method == 'POST':
        #修改新品推荐
        NO1_title = request.POST.get('NO1_title')
        NO2_title = request.POST.get('NO2_title')
        NO3_title = request.POST.get('NO3_title')
        NO1_uname = request.POST.get('NO1_uname')
        NO2_uname = request.POST.get('NO2_uname')
        NO3_uname = request.POST.get('NO3_uname')
        NO1_type = request.POST.get('NO1_type')
        NO2_type = request.POST.get('NO2_type')
        NO3_type = request.POST.get('NO3_type')
        if not(NO1_title):
            m = '请上按规则填写全部内容'
            return render(request, 'goodsManagement/recommendMannagement.html', locals())
        submit_type = request.POST.get('submit_type')
        if not submit_type:
            m = '请选择提交类型'
            return render(request, 'goodsManagement/recommendMannagement.html',locals())

        user1 = User.objects.filter(username=NO1_uname)
        type1 = GoodsType.objects.filter(id=NO1_type)
        if user1 and type1:
            goods1 = Goods.objects.filter(title=NO1_title,saller=user1[0].id,goods_type=type1[0].id)
            if not goods1:
                m1 = "商品名不存在"
                return render(request, 'goodsManagement/recommendMannagement.html', locals())
        else:
            m1 = "用户名不存在"
            return render(request, 'goodsManagement/recommendMannagement.html', locals())

        user2 = User.objects.filter(username=NO2_uname)
        type2 = GoodsType.objects.filter(id=NO2_type)
        if user2 and type2:
            goods2 = Goods.objects.filter(title=NO2_title,saller=user2[0].id,goods_type=type2[0].id)
            if not goods2:
                m2 = "商品名不存在"
                return render(request, 'goodsManagement/recommendMannagement.html', locals())
        else:
            m2 = "用户名不存在"
            return render(request, 'goodsManagement/recommendMannagement.html', locals())

        user3 = User.objects.filter(username=NO3_uname)
        type3 = GoodsType.objects.filter(id=NO3_type)
        if user3 and type3:
            goods3 = Goods.objects.filter(title=NO3_title,saller=user3[0].id,goods_type=type3[0].id)
            if not goods3:
                m3 = "商品名不存在"
                return render(request, 'goodsManagement/recommendMannagement.html', locals())
        else:
            m3 = "用户名不存在"
            return render(request, 'goodsManagement/recommendMannagement.html', locals())
        if submit_type == "修改":
            global recommend
            recommend = [
                ('product_details.html?typeid=' + str(type1[0].id) + '&goodid=' + str(goods1[0].id), '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                ('product_details.html?typeid=' + str(type2[0].id) + '&goodid=' + str(goods2[0].id), '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                ('product_details.html?typeid=' + str(type3[0].id) + '&goodid=' + str(goods3[0].id), '/images/goods/' + str(goods3[0].id) + '/0.jpg')
            ]
            m = '新品推荐修改完成'
            return render(request,'goodsManagement/recommendMannagement.html',locals())
        if submit_type == "预览":
            recommend_c = [
                ('product_details.html?typeid=' + str(type1[0].id) + '&goodid=' + str(goods1[0].id), '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                ('product_details.html?typeid=' + str(type2[0].id) + '&goodid=' + str(goods2[0].id), '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                ('product_details.html?typeid=' + str(type3[0].id) + '&goodid=' + str(goods3[0].id), '/images/goods/' + str(goods3[0].id) + '/0.jpg')
            ]
            return render(request,'index/index.html',{'banner':banner,'recommend':recommend_c,'type_list':type_list})

#首页管理-分类推荐管理
def classifiedArrivalsManagement(request):
    try:
        Auser = request.session["user"]
    except:
        Auser = False
        logging.warning("管理员用户未登录")
    if not Auser:
        return redirect("/administrators/login")
    if request.method == 'GET':
        types = GoodsType.objects.all()
        return render(request,'goodsManagement/classifiedArrivalsManagement.html',locals())
    if request.method == 'POST':
        #修改分类推荐
        NO1_title = request.POST.get('NO1_title')
        NO2_title = request.POST.get('NO2_title')
        NO3_title = request.POST.get('NO3_title')
        NO1_uname = request.POST.get('NO1_uname')
        NO2_uname = request.POST.get('NO2_uname')
        NO3_uname = request.POST.get('NO3_uname')
        good_type = request.POST.get('goods_type')
        if not(NO1_title):
            m = '请上按规则填写全部内容'
            return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())
        submit_type = request.POST.get('submit_type')
        if not submit_type:
            m = '请选择提交类型'
            return render(request, 'goodsManagement/classifiedArrivalsManagement.html',locals())

        user1 = User.objects.filter(username=NO1_uname)
        goods_type = GoodsType.objects.filter(id=good_type)
        if user1 and goods_type:
            goods1 = Goods.objects.filter(title=NO1_title,saller=user1[0].id,goods_type=goods_type[0].id)
            if not goods1:
                m1 = "商品名不存在"
                return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())
            goods1_price = GoodsSpecification.objects.filter(goods=goods1[0].id)
        else:
            m1 = "用户名不存在"
            return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())

        user2 = User.objects.filter(username=NO2_uname)
        if user2 and goods_type:
            goods2 = Goods.objects.filter(title=NO2_title,saller=user2[0].id,goods_type=goods_type[0].id)
            if not goods2:
                m2 = "商品名不存在"
                return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())
            goods2_price = GoodsSpecification.objects.filter(goods=goods2[0].id)
        else:
            m2 = "用户名不存在"
            return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())

        user3 = User.objects.filter(username=NO3_uname)
        if user3 and goods_type:
            goods3 = Goods.objects.filter(title=NO3_title,saller=user3[0].id,goods_type=goods_type[0].id)
            if not goods3:
                m3 = "商品名不存在"
                return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())
            goods3_price = GoodsSpecification.objects.filter(goods=goods3[0].id)
        else:
            m3 = "用户名不存在"
            return render(request, 'goodsManagement/classifiedArrivalsManagement.html', locals())

        if submit_type == "修改":
            global type_list
            for type in type_list:
                if type['title'] == goods_type[0].title:
                    type['title'] = goods_type[0].title
                    type['link'] = '/goods/list?'+str(goods_type[0].id)
                    type['goods_list'] = [
                        (re.findall('\w+', goods1[0].title)[0], re.findall('\s\w+', goods1[0].desc)[0],
                         goods1_price[0].price,
                         'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods1[0].id),
                         '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                        (re.findall('\w+', goods2[0].title)[0], goods2_price[0].price,
                         'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods2[0].id),
                         '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                        (re.findall('\w+', goods3[0].title)[0], goods3_price[0].price,
                         'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods3[0].id),
                         '/images/goods/' + str(goods3[0].id) + '/0.jpg'),
                    ]
                    m = '分类更新商品完成'
                    return render(request,'goodsManagement/classifiedArrivalsManagement.html',locals())
            else:
                type = type_list[0]
                type['title'] = goods_type[0].title
                type['link'] = '/goods/list?' + str(goods_type[0].id)
                type['goods_list'] = [
                    (re.findall('\w+', goods1[0].title)[0], re.findall('\s\w+', goods1[0].desc)[0],goods1_price[0].price, 'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods1[0].id), '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                    (re.findall('\w+', goods2[0].title)[0], goods2_price[0].price,'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods2[0].id), '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                    (re.findall('\w+', goods3[0].title)[0], goods3_price[0].price,'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods3[0].id), '/images/goods/' + str(goods3[0].id) + '/0.jpg'),
                ]
                m = '修改分类完成'
                return render(request, 'goodsManagement/recommendMannagement.html', locals())
        if submit_type == "预览":
            type_list_c = [
                {
                    'title': '背包',
                    'link': '/goods/list?1',
                    'goods_list': [
                        ('UREVO', '活力学院休闲双肩包', '￥6688.00', 'product_details.html?typeid=2&goodid=957',
                         '/static/images/index/index_bp1.png'),
                        ('Grinder 牛津休闲双肩包', '￥6688.00', 'product_details.html?typeid=2&goodid=956',
                         '/static/images/index/index_bp2.png'),
                        ('90分户外休闲双肩包', '￥68.00', 'product_details.html?typeid=2&goodid=958',
                         '/static/images/index/index_Sbanner_img1.png'),
                    ]
                },
                {
                    'title': '拉杆箱',
                    'link': '/goods/list?2',
                    'goods_list': [
                        ('90分旅行箱 1A', '与你走向更远的的地方', '￥6688.00', 'product_details.html?typeid=1&goodid=942',
                         '/static/images/index/index_Sbanner_img3.png'),
                        ('与爱箱随 一路精彩', '￥6688.00', 'product_details.html?typeid=1&goodid=947',
                         '/static/images/index/index_trunk1.png'),
                        ('让美好旅行触手可及', '￥68.00', 'product_details.html?typeid=1&goodid=945',
                         '/static/images/index/index_trunk2.png'),
                    ]
                },
                {
                    'title': '手提包',
                    'link': '/goods/list?3',
                    'goods_list': [
                        ('时尚都市菱格双肩包', '经典百搭 时尚优雅', '￥6688.00', 'roduct_details.html?typeid=3&goodid=974',
                         '/static/images/index/index_hb1.png'),
                        ('CARRYO 轻奢级牛皮水桶包', '￥6688.00', 'product_details.html?typeid=3&goodid=976',
                         '/static/images/index/index_Sbanner_img2.png'),
                        ('英伦复古轻奢级马鞍包', '￥68.00', 'product_details.html?typeid=3&goodid=975',
                         '/static/images/index/index_hb2.png'),
                    ]
                },
            ]
            for type in type_list_c:
                if type['title'] == goods_type[0].title:
                    type['title'] = goods_type[0].title
                    type['link'] = '/goods/list?'+str(goods_type[0].id)
                    type['goods_list'] = [
                        (re.findall('\w+',goods1[0].title)[0], re.findall('\s\w+', goods1[0].desc)[0], goods1_price[0].price, 'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods1[0].id), '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                        (re.findall('\w+',goods2[0].title)[0], goods2_price[0].price, 'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods2[0].id), '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                        (re.findall('\w+',goods3[0].title)[0], goods3_price[0].price, 'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods3[0].id), '/images/goods/' + str(goods3[0].id) + '/0.jpg'),
                    ]
                    return render(request, 'index/index.html', {'banner':banner, 'recommend':recommend, 'type_list':type_list_c})
            else:
                type = type_list_c[0]
                type['title'] = goods_type[0].title
                type['link'] = '/goods/list?' + str(goods_type[0].id)
                type['goods_list'] = [
                    (re.findall('\w+', goods1[0].title)[0], re.findall('\s\w+', goods1[0].desc)[0],goods1_price[0].price, 'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods1[0].id), '/images/goods/' + str(goods1[0].id) + '/0.jpg'),
                    (re.findall('\w+', goods2[0].title)[0], goods2_price[0].price,'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods2[0].id), '/images/goods/' + str(goods2[0].id) + '/0.jpg'),
                    (re.findall('\w+', goods3[0].title)[0], goods3_price[0].price,'product_details.html?typeid=' + str(goods_type[0].id) + '&goodid=' + str(goods3[0].id), '/images/goods/' + str(goods3[0].id) + '/0.jpg'),
                ]
                return render(request, 'index/index.html',{'banner': banner, 'recommend': recommend, 'type_list': type_list_c})


# 管理员登录
def login(request):
    if request.method == "GET":
        return render(request, 'userManagement/login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        code = request.session['verifycode'].lower()
        new_verify = request.POST.get('verify').lower()
        if code != new_verify:
            m = "验证码错误"
            return render(request, "userManagement/login.html", locals())
        if username and password:
            # 使用django提供的验证方法，传入用户名和密码，会返回一个user对象
            user = auth.authenticate(username=username, password=password,usertype=1)
            if user is not None and user.is_active:
                auth.login(request,user)
                request.session['user'] = user.username
                return redirect('/administrators/home/')
            else:
                m="用户名或密码错误"
                return render(request,"userManagement/login.html",locals())
        else:
            m="未输入密码"
            render(request, "userManagement/login.html", locals())
# 管理员退出
@check_login_status
def logout(request):
    del request.session['user']
    auth.logout(request)
    return redirect('administrators/login')


