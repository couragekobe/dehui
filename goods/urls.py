from django.conf.urls import url

from . import views

urlpatterns = [
    # 商品列表页用到的路由
    url(r'^$', views.goods_list),
    url(r'^list/(?P<type_id>\d+)$', views.goods_list),
    # 商品详情页用到的路由
    url(r'^detail/(?P<goods_id>\d+)/(?P<spec_id>\d+)/$', views.detail),
    url(r'^detail/(?P<goods_id>\d+)/$', views.detail),
    url(r'^search', views.search),
]

