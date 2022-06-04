"""usermanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import models
from app01.views import depart,user,pretty,admin,login,order,charts,upload,city
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    #path('admin/', admin.site.urls),

    #启用media
    # 以media开头，后面除了换行符以外的换行符都被匹配
    # serve： 以media开头的, 以Django来处理
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}, name='media'),

    path('depart/list/', depart.depart_show),
    path('depart/add/' ,depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:uid>/edit/', depart.depart_edit),
    path('depart/multi/',depart.depart_multi),

    path('user/list/', user.user_show),
    path('user/add/', user.user_add),
    path('user/<int:uid>/edit/', user.user_edit),
    path(r'user/<int:uid>/delete/', user.user_delete),

    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:uid>/edit/', pretty.pretty_edit),
    path(r'pretty/<int:uid>/delete/', pretty.pretty_delete),

    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:uid>/edit/',admin.admin_edit),
    path('admin/<int:uid>/delete/', admin.admin_delete),
    path('admin/<int:uid>/reset/',admin.admin_reset),

    path('login/',login.admin_login),
    path('logout/',login.logout),
    path('image/code/',login.image_code),

    #订单管理
    path('order/list/',order.order_list),
    path('order/add/',order.order_add),
    path('order/delete/',order.order_delete),
    path('order/detail/',order.order_detail),
    path('order/edit/',order.order_edit),

    path('chart/list/',charts.chart_list),
    path('chart/bar/',charts.chart_bar),
    path('chart/pie/',charts.chart_pie),

    path('upload/list/',upload.upload_list),
    path('upload/form/',upload.upload_form),
    path('upload/modelform/',upload.upload_modelform),

    path('city/list/',city.city_list),
    path('city/add/', city.city_add),
]
