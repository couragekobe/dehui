from django.contrib import admin

# Register your models here.

from . import models

class AddressManager(admin.ModelAdmin):
    '''在 /admin/Address/Address/ 商品管理类中表格的显示属性'''
    list_display = ['id', 'Addressname', 'mobile', 'email']
    list_display = ['consignee', 'address', 'mobile', 'zipcode', 'alias', 'user']


admin.site.register(models.Address, AddressManager)
