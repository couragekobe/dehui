from django.db import models

# Create your models here.

from user.models import User
# from goods.models import Goods
from goods.models import GoodsSpecification

class Favorite(models.Model):
    '''收藏模块
    此模块的 user 关联收藏人
    此模块的 spce 关联收藏商品的规格信息
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 收藏用户
    spec = models.ForeignKey(GoodsSpecification, on_delete=models.CASCADE)  # 根据规格信息一定能找到唯一的商品

    def __str__(self):
        return self.user.username
