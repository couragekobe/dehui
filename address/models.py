from django.db import models

# Create your models here.

# from user import models as user_models
from user.models import User

class Address(models.Model):
    '''收货地址信息表'''
    consignee = models.CharField("收件人", max_length=20, null=False, default="any")
    address = models.TextField("收货地址",null=False)
    mobile = models.CharField("手机号", max_length=13, null=False)
    is_default = models.BooleanField("是否为默认地址", default=False)
    zipcode = models.CharField("邮编", max_length=6, default="000000")
    alias = models.CharField("别名", max_length=50)  # 家，公司，学校等
    user = models.ForeignKey(User)  # 外键关联用户信息

    def __str__(self):
        return self.consignee

    class Meta:
        ordering = ['id']
