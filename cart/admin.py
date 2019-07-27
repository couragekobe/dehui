from django.contrib import admin

# Register your models here.

from . import models

class CartManager(admin.ModelAdmin):
    list_display = ['id', 'user', 'goods_spec', 'count']

admin.site.register(models.CartItem, CartManager)


