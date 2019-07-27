from django.contrib import admin

# Register your models here.

from . import models

class FavoriteManager(admin.ModelAdmin):
    list_display = ['id', 'user', 'spec']

admin.site.register(models.Favorite, FavoriteManager)


