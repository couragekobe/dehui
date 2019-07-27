from django.conf.urls import url

from . import views

urlpatterns = [
    # 收葳模块用到的路由
    url(r'^$', views.list_all),
    url(r'^add/(?P<spec_id>\d+)/$', views.add),
    url(r'^add_ajax/(?P<spec_id>\d+)/$', views.add_ajax),
    url(r'^delete/(?P<id>\d+)/$', views.delete),
    url(r'^delete_ajax/(?P<id>\d+)/$', views.delete_ajax),
    url(r'^clear_all/$', views.clear_all),
]
