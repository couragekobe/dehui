from django.db import models
from goods.models import *
from user.models import *

# Create your models here.

ORDER_STATUS = (
    (0, "订单关闭"),
    (1, "待付款"),
    (2, "待发货"),
    (3, "配送中"),
    (4, "交易完成"),
)

class Order(models.Model):
    '''订单信息
        在购物车中,如果有不同商家的商品时，在支付完成后，会按商家的个数分别拆分为N个订单，
        一个订单可能包含有多个商品，每个商家客自走自己的物流, 一个订单在支付后可能会拆分为多个订单,
        由多个商家各自发出自己的商品,每个商品走独自的物流,也可以走同一个物流
    '''
    orderNo = models.CharField("订单号", max_length=20, null=False, default="20190601HHMMSSXXXXXX") # 订单号前8位为时间  # 后面的随机生成不重复的数字
    status = models.IntegerField("订单状态", choices=ORDER_STATUS, null=False, default=0)
    real_money = models.DecimalField('实际价格', max_digits=8, decimal_places=2, default=0.0)
    logistics = models.CharField("物流信息", max_length=300, null=False, default="北京市东城区珠市口东大街6号珍贝大厦三层达内科技")
    amount = models.IntegerField("数量", null=True, default=0)
    bank = models.CharField("支付方式加卡号",max_length=50, null=False, default="unpay")
    dealtime = models.DateTimeField("交易时间", auto_now_add=True)
    buy_user = models.ForeignKey(User, related_name="买家", default=1)  # 关联买家
    sale_user = models.ForeignKey(User, related_name="卖家", default=1)  # 关联卖家
    def __str__(self):
        return self.orderNo


class OrderGoods(models.Model):
    '''
    订单商品信息
    '''
    order = models.ForeignKey(Order)  # 关联订单
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 关联商品
    saller = models.ForeignKey(User, on_delete=models.CASCADE)  # 此商品的商家用户
    title = models.CharField("商品名称", max_length=300, null=False, default="商品名称")
    price = models.DecimalField('商品交易时价格', max_digits=8, decimal_places=2)
    amount = models.IntegerField("交易数量", null=True, default=0)
    goodsimg = models.CharField("产品图",max_length=100, default="/images/default.png")  # 只记录其中一条

    spec_name = models.CharField("规格名称", max_length=300, default='规格')

    spec_info = models.CharField('规格信息', max_length=300, null=False)


    def __str__(self):
        return self.order.orderNo+self.title

    def __setitem__(self, k, v):
        self.k = v
















# class Logistics(models.Model):
#     '''商品物流'''
#     delivery_time = models.DateTimeField()
#     logistics_company = models.IntegerField("物流公司", choices=COMPANY_INFO, default=0)
#     express_number = models.CharField("快递编号", max_length=200, null=True, blank=True)
#     order = models.OneToOneField(Order)

#     def __str__(self):
#         return self.express_number


# class LogisticsInfo(models.Model):
#     '''物流商品流程信息'''
#     information = models.CharField("物流信息", max_length=200)
#     datetime = models.DateTimeField(auto_now_add=True)
#     logist = models.ForeignKey(Logistics)

#     def __str__(self):
#         return self.information

