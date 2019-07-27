from django.contrib import admin

# Register your models here.

from . import models

class GoodsManager(admin.ModelAdmin):
    '''在 /admin/goods/goods/ 商品管理类中表格的显示属性'''
    list_display = ['id', 'title', 'spec_name', 'is_delete', 'saller', 'is_saller_empower', 'is_admin_empower']

admin.site.register(models.Goods, GoodsManager)

class GoodsTypeManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_delete']

admin.site.register(models.GoodsType, GoodsTypeManager)

class GoodsSpecManager(admin.ModelAdmin):
    '''在 /admin/goods/goodsspecification/ 显示属性'''
    list_display = ['id', 'spec_info', 'price', 'stock', 'goods_id']

admin.site.register(models.GoodsSpecification, GoodsSpecManager)

