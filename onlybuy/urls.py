"""onlybuy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage),  # 设置首项的路由
    url(r'^index.html$', views.homepage),
    url(r'^header.html$', views.header),
    url(r'^footer.html$', views.footer),
    url(r'^user/', include('user.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^verify/', include('verify.urls')),
    url(r'^sale/', include('sale.urls')),
    url(r'^goods/', include('goods.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^address/', include('address.urls')),
    url(r'^favorite/', include('favorite.urls')),
    url(r'^administrators/', include('administrator.urls')),
]

# 添加静态访问地址
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.CSS_URL, document_root=settings.CSS_PATH)
urlpatterns += static(settings.JS_URL, document_root=settings.JS_PATH)
urlpatterns += static(settings.JQ_URL, document_root=settings.JQ_PATH)





