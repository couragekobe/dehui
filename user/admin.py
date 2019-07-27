from django.contrib import admin

# Register your models here.

from . import models

class UserManager(admin.ModelAdmin):
    '''在 /admin/user/user/ 商品管理类中表格的显示属性'''
    list_display = ['id', 'username', 'is_superuser', 'is_staff', 'is_active', 'mobile', 'email', 'sex', 'is_delete', 'usertype']

admin.site.register(models.User, UserManager)
