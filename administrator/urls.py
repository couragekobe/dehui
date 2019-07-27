from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^home/', managementHome),
    url(r'^searchGoods/', searchGoods),
    url(r'^closedGoods/', closedGoods),
    url(r'^searchClassification/', searchClassification),
    url(r'^closedClassification/', closedClassification),
    url(r'^increaseClassification/', increaseClassification),
    url(r'^increaseSaller/', increaseSaller),
    url(r'^login/', login),
    url(r'^logout/', logout),
    url(r'^modPassword/', modPassword),
    url(r'^bannerManagement/', bannerManagement),
    url(r'^recommendManagement/', recommendManagement),
    url(r'^classifiedArrivalsManagement/', classifiedArrivalsManagement),
    url(r'^index/',index),
]