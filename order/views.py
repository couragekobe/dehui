from django.shortcuts import render,redirect
from django.http import HttpResponse
from cart.models import *
from address.models import *
from order.models import *
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证




# Create your views here.
# 显示所有的订单
@login_required(login_url='/user/login/')
def order_list(request):
    if request.method == "GET":
        orders = Order.objects.filter(buy_user=request.user)
        order_goods_list = []
        for new_order in orders:
            order_goodss = OrderGoods.objects.filter(order=new_order)
            # 找出所有的商品 判断是否有状态变化
            for order_goods in order_goodss:
                order_goods.tprice = float(order_goods.amount) * float(order_goods.price)
                try:
                    s = order_goods.goods.goods_images
                    goods_images = eval(s)
                    order_goods.head_image = '/images/goods/' + str(order_goods.goods.id) + '/' + goods_images[0]
                except:
                    order_goods.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
                if order_goods.order.status == 1:
                    order_goods.status_wo = "去付款"
                    order_goods.status_w = "待付款"
                    order_goods.status_ws = "取消订单"
                elif order_goods.order.status == 2:
                    order_goods.status_w = "待发货"
                    order_goods.status_ws = "退款申请"
                elif order_goods.order.status == 3:
                    order_goods.status_w = "配送中"
                    order_goods.status_ws = "退货申请"
                elif order_goods.order.status == 4:
                    order_goods.status_w = "交易完成"
                    order_goods.status_ws = "确认收货"
                elif order_goods.order.status == 0:
                    order_goods.status_wz = " "
                    order_goods.status_w = "订单关闭"
                    order_goods.status_ws = "订单关闭"
                order_goods_list.append(order_goods)
        return render(request, "order/myOrder.html", locals())

# 显示订单详情
def order_detail(request,orderid):
    new_order = Order.objects.filter(id=orderid)[0]
    address = Address.objects.filter(user=new_order.buy_user)[0]
    order_goods = OrderGoods.objects.filter(order=new_order)
    for order_good in order_goods:
        order_good.tprice = float(order_good.amount) * float(order_good.price)
        try:
            s = order_good.goods.goods_images
            goods_images = eval(s)
            order_good.head_image = '/images/goods/' + str(order_good.goods.id) + '/' + goods_images[0]
        except:
            order_goods.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
        order_good.tprice = float(order_good.amount) * float(order_good.price)
    if new_order.status == 1:
        new_order.status_w = "待付款"
    elif new_order.status == 2:
        new_order.status_w = "待发货"
    elif new_order.status == 3:
        new_order.status_w = "配送中"
    elif new_order.status == 4:
        new_order.status_w = "交易完成"
    elif new_order.status == 0:
        new_order.status_w = "订单关闭"
    return render(request, 'order/orderInfo.html', locals())

# 买家订单状态改变
def order_change(request, status ,orderid):
    # 取消订单操作
    if int(status) == 1:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 0
        change_order.save()
        return redirect('/order')
    # 退款操作
    if int(status) == 2:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 0
        change_order.save()
        return redirect('/order')
    # 退货操作
    if int(status) == 3:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 0
        change_order.save()
        return redirect('/order')
    # 确认收货操作
    if int(status) == 4:
        change_order = Order.objects.filter(id=orderid)[0]
        change_order.status = 5
        change_order.save()
        return redirect('/order')

# 订单支付
@login_required(login_url='/user/login/')
def order_pay(request, orderid):
    # 跳转到支付页面
    if request.method == "GET":
        new_order = Order.objects.filter(id=orderid)[0]
        return render(request, 'order/payment.html', locals())
    # 支付完成 修改状态为待发货
    if request.method == "POST":
        order_id = request.POST.get("orderid")
        new_order = Order.objects.filter(id=order_id)[0]
        new_order.status = 2
        new_order.save()
        return render(request, 'order/pay_success.html', locals())



