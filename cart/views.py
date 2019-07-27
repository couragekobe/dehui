import datetime
from django.shortcuts import render
from address.models import *
from order.models import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证


from . import models
from cart.models import CartItem
from goods.models import GoodsSpecification
import json

@login_required(login_url='/user/login/')
def list_all(request):
    '''列出购物车中全部商品'''

    cart_items = models.CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.total = item.count * item.goods_spec.price

        a_product = item.goods_spec.goods
        try:
            s = a_product.goods_images
            goods_images = eval(s)
            item.head_image = '/images/goods/' + str(a_product.id) + '/' + goods_images[0]
        except :
            item.head_image = '/images/default.png'  #  没有图片时head_image 置为空字符串

    return render(request, 'cart/cart_list.html', locals())


#@login_required(login_url='/user/login/')
def add(request, spec_id, goods_count=1):
    '''向购物车加添加商品'''
    goods_count = int(goods_count)  # 转为整数
    try:
        spec = GoodsSpecification.objects.get(id=spec_id)
    except:
        raise Http404("没有此规格的商品")

    try:
        item = CartItem.objects.get(goods_spec=spec, user=request.user)
        item.count += goods_count
    except:
        item = models.CartItem(user=request.user, goods_spec=spec, count=goods_count)
    item.save()
    # 获取请求源路径
    p_path = request.META.get("HTTP_REFERER")
    # 请求原路径来自收藏夹返回成功添加页面
    if p_path == "http://localhost:8000/favorite/":
        m = "商品已成功加入到购物车!"
        return render(request, "cart/favorite_add_success.html", locals())
    return HttpResponseRedirect("/cart/")


def add_ajax(request, spec_id, goods_count=1):
    '''用ajax提交加入购物车（为ajax请求提供接口)
    '''
    json_dict = {"status": 200, "message": "添加成功"}
    if not request.user.is_authenticated():
        json_dict['status'] = 401
        json_dict['message'] = "用户没有登陆"
        return HttpResponse(json.dumps(json_dict))

    goods_count = int(goods_count)  # 转为整数
    try:
        spec = GoodsSpecification.objects.get(id=spec_id)
    except:
        json_dict['status'] = 404
        json_dict['message'] = "没有此规格的商品"
        return HttpResponse(json.dumps(json_dict))

    try:
        item = CartItem.objects.get(goods_spec=spec, user=request.user)
        item.count += goods_count
    except:        
        item = models.CartItem(user=request.user, goods_spec=spec, count=goods_count)

    item.save()
    return HttpResponse(json.dumps(json_dict))


@login_required(login_url='/user/login/')
def delete(request, id):
    '''从购物车中删除指定的商品'''
    try:
        item = CartItem.objects.get(id=id, user=request.user)
        item.delete()
    except:
        raise Http404('购物车中没有此商品')
    return HttpResponseRedirect("/cart")


def delete_ajax(request, id):
    '''用ajax删除购物车中的商品（为ajax请求提供接口)'''

    json_dict = {"status": 200, "message": "删除成功"}
    if not request.user.is_authenticated():
        json_dict['status'] = 401
        json_dict['message'] = "用户没有登陆"
        return HttpResponse(json.dumps(json_dict))

    try:
        item = CartItem.objects.get(id=id, user=request.user)
        item.delete()
    except:
        json_dict['status'] = 404
        json_dict['message'] = "购物车中没有此商品"
        return HttpResponse(json.dumps(json_dict))

    return HttpResponse(json.dumps(json_dict))


@login_required(login_url='/user/login/')
def clear_all(request):
    items = models.CartItem.objects.filter(user=request.user)
    items.delete()
    return HttpResponseRedirect("/cart")

# 订单结算功能
@login_required(login_url='/user/login/')
def settlement(request):
    if request.method == "POST":
        settlement_list = []
        goods_sum = 0
        goods_tprice = 0
        cart_items = models.CartItem.objects.filter(user=request.user)
        time_now = datetime.datetime.now()
        # 生成订单 状态为待付款
        order_name = time_now.strftime("%Y%m%d_%H%M%S")
        order = Order.objects.create(orderNo=order_name, status=1, buy_user=request.user)
        for item in cart_items:
            a_product = item.goods_spec.goods
            try:
                s = a_product.goods_images
                goods_images = eval(s)
                item.head_image = '/images/goods/' + str(a_product.id) + '/' + goods_images[0]
            except:
                item.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
        order = Order.objects.filter(orderNo=order_name)[0]
        # 循环购物车中所有的商品
        for item in cart_items:
            goods_id = request.POST.get(str(item.id))
            is_settlement = request.POST.get(str(item.id)+"settlement")
            goods_cunt = request.POST.get(str(item.id)+"cunt")
            # 所有被勾选的商品
            if goods_id and is_settlement == "true":
                cart_goods = CartItem.objects.filter(id=goods_id)[0]
                address_a = Address.objects.filter(user=cart_goods.user)
                try:
                    i_goods = cart_goods.goods_spec.goods
                    s = i_goods.goods_images
                    goods_img = eval(s)
                    cart_goods.head_image = '/images/goods/' + str(i_goods.id) + '/' + goods_images[0]
                except:
                    cart_goods.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
                cart_goods.cunt = goods_cunt
                goods_sum += int(cart_goods.cunt)
                cart_goods.t_price = float(goods_cunt) * float(cart_goods.goods_spec.price)
                goods_tprice += int(cart_goods.t_price)
                saller = cart_goods.goods_spec.goods.saller
                settlement_list.append(cart_goods)
                # 生成订单关联的商品表
                print(cart_goods.goods_spec.spec_info)
                order_goods = OrderGoods.objects.create(order=order,
                                                        goods=cart_goods.goods_spec.goods,
                                                        saller=cart_goods.goods_spec.goods.saller,
                                                        title=cart_goods.goods_spec.goods.title,
                                                        price=cart_goods.goods_spec.price,
                                                        amount=goods_cunt,
                                                        goodsimg=cart_goods.head_image,
                                                        spec_name=cart_goods.goods_spec.goods.spec_name,
                                                        spec_info=cart_goods.goods_spec.spec_info)
                order_goods.save()
        # 给订单添加 商品数量及总价格
        order.amount = goods_sum
        order.real_money = goods_tprice
        order.sale_user = saller
        order.save()
        if len(settlement_list)>0:
            return render(request, "cart/orderConfirm.html", locals())
        else:
            ms="请选择至少一项商品"
            # 如果没有选择商品 需要将订单删除
            order.delete()
            return render(request, "cart/cart_list.html", locals())