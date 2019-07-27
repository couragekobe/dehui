"""onlybuy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',index,name='index'),#会首页
    url(r'^user/login/$',login,name='login'),#登录页
    url(r'^user/info/$',info_,name='info'),#卖家个人信息页
    url(r'^user/mod_info/$',mod_info,name='mod_info'),#更改个人信息
    url(r'^user/mod_infoname/$',mod_infoname,name='mod_info_'),#更改个人信息POST
    url(r'^user/mod_password/$',mod_password,name='mod_password'),#更改登录密码
    url(r'^goods/new_goods/$',new_goods,name='new_goods'),#上传新商品
    url(r'^goods/new_shelves/$',new_shelves,name='new_shelves'),#商品上架
    url(r'^goods/closed_shelves/$',closed_shelves,name='closed_shelves'),#商品下架
    url(r'^goods/preview/$', new_preview, name='preview'),  # 商品展示预览
    url(r'^goods/mod/(.*)$',mod_,name='mod'),#修改商品信息GET
    url(r'^goods/mod_goods/$',mod_goods,name='mod_goods'),
    url(r'^goods/logout/$',logout,name='logout'),#退出登录
    url(r'^goods/del_img/(.*)/$',del_img,name='del_img'),#删除产品图
    url(r'^goods/del_detail_img/(.*)/$',del_detail_img,name='del_detail_img'),#删除详情图
    url(r'^goods/del_gui/(.*)/$',del_gui,name='del_gui'),#删除规格
    url(r'^goods/mod_images/$',mod_image,name='mod_images'),#添加产品图和详情图
    url(r'^goods/mod_title/$',mod_title,name='mod_title'),#修改商品名称路由
    url(r'^goods/mod_price/$',mod_price,name='mod_price'),#修改规格
    url(r'^goods/new_price/$',new_price,name='new_price'),#添加新的产品规格
    url(r'^goods/insert_img/$',insert_img,name='insert_img'),#插入商品图片
    url(r'^goods/insert_detail_img/$',insert_detail_img,name='insert_detail_img'),#插入商品详情图
    url(r'^goods/mod_goods_img/$',mod_goods_img,name='mod_goods_img'),#修改商品图
    url(r'^goods/mod_detail_img/$',mod_detail_img,name='mod_detail_img'),#修改详情图
    url(r'^order_list', order_list),  # 订单信息
    url(r'^order_change/(?P<status>\d+)/(?P<orderid>\d+)', sale_order_change),  # 订单信息

]
