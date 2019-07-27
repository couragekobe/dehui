from django.conf.urls import url

from . import views

urlpatterns = [
    url('add', views.add_address, name='add_address'),
    url('list', views.list_address, name='list_address'),
    url('default', views.default, name='default'),
    url('delete', views.delete_adress, name='delete_adress'),
    url(r'^$', views.index),
]

