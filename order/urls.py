from django.conf.urls import url

from . import views

urlpatterns = [
    # 商品列表页用到的路由
    url(r'^$', views.order_list),
    url(r'^pay/(?P<orderid>\d+)', views.order_pay),
    url(r'^detail/(?P<orderid>\d+)', views.order_detail),
    url(r'^change/(?P<status>\d+)/(?P<orderid>\d+)', views.order_change),
]