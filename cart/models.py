from django.db import models

# Create your models here.

from user.models import User
from goods.models import *


class CartItem(models.Model):
    '''此类用于描述购物车中数据项'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 购物车关联的用户
    goods_spec = models.ForeignKey(GoodsSpecification, on_delete=models.CASCADE)  # 购物车关联的商品规格信息
    count = models.IntegerField("商品个数", default=1)  # 商品个数

    def __str__(self):
        return self.user.username + str(self.goods_spec)


# class Buynow(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
#     color = models.CharField('颜色', max_length=50)
#     spec = models.CharField('规格', max_length=50)
#     amount = models.IntegerField("数量", null=True, default=0)

#     def __str__(self):
#         return self.user.username
