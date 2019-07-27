from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^register', views.register),
    url(r'^$', views.index),
    url(r'^personage.html', views.index),
    url(r'^mod_password', views.mod_password),
    url(r'^changepwd', views.mod_password),
    url(r'^personal_password.html', views.mod_password),    
    url(r'test$', views.test),
]

