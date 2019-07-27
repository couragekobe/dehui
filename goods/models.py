from django.db import models

from user.models import User
# Create your models here.


class GoodsType(models.Model):
    title = models.CharField("分类名称", max_length=30, null=False, default="分类名称")
    is_delete = models.BooleanField("是否下架", default=False)
    # create_time = models.DateField("创建时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

class Goods(models.Model):
    '''
        商品信息类
        +-------------------+---------------+------+-----+---------+----------------+
        | Field             | Type          | Null | Key | Default | Extra          |
        +-------------------+---------------+------+-----+---------+----------------+
        | id                | int(11)       | NO   | PRI | NULL    | auto_increment |
        | title             | varchar(100)  | NO   |     | NULL    |                |
        | desc              | varchar(1000) | YES  |     | NULL    |                |
        | goods_images      | varchar(1000) | NO   |     | NULL    |                |
        | detail_images     | varchar(1000) | NO   |     | NULL    |                |
        | spec_name         | varchar(20)   | NO   |     | NULL    |                |
        | is_saller_empower | tinyint(1)    | NO   |     | NULL    |                |
        | is_admin_empower  | tinyint(1)    | NO   |     | NULL    |                |
        | is_delete         | tinyint(1)    | NO   |     | NULL    |                |
        | goods_type_id     | int(11)       | NO   | MUL | NULL    |                |
        | saller_id         | int(11)       | NO   | MUL | NULL    |                |
        +-------------------+---------------+------+-----+---------+----------------+
    '''
    # 商品信息相关字段
    title = models.CharField("商品名称", max_length=100, null=False, default="商品名称")
    desc = models.CharField('描述', max_length=1000, null=True)
    # goods_images 存储商品小图的图片位置列表JSON数据,如: ["image/1.png", "image/2.png"]
    goods_images = models.CharField("商品图列表", default='[]', max_length=1000)
    detail_images = models.CharField("商品详情图列表", default='[]', max_length=1000)  # 商品详细信息图片,格式同上

    goods_type = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    spec_name = models.CharField("规格名称", max_length=20, default='规格')

    # 商品管理相关字段
    saller = models.ForeignKey(User, on_delete=models.CASCADE)  # 此商品的商家用户
    is_saller_empower = models.BooleanField("卖家上架", default=False)  # 卖家决定是否上架
    is_admin_empower = models.BooleanField("管理员上架审批", default=False)  # 管理员确认是否上架(两个都为True是才可以在商品商显示)
    is_delete = models.BooleanField("商品无效", default=False)  # 商品是否有效, 为True是，说明已商品已经不再有效

    # create_time = models.DateField("创建时间", auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['id']  # 设置排序顺序为 id从小到大

class GoodsSpecification(models.Model):
    '''商品规格明细表:
      此表规定商品的规格，如:
        规格名为"颜色"时，规格可以是:"红色"，"白色"，"黑色"
        规格名为SD卡的"容量"时，规格可以是:"16G"，"32G"，"64G"
          ...
      注:
         规格的名字添加在Goods 商品表的 'spec_name' 中
    '''
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    price = models.DecimalField('此规格的价格', max_digits=8, decimal_places=2)
    spec_info = models.CharField('规格信息', max_length=100, null=False)
    stock = models.IntegerField("库存", null=False, default=1)

    def __str__(self):
        return self.spec_info + " . . . .  价格: " + str(self.price)

    class Meta:
        ordering = ['id']

