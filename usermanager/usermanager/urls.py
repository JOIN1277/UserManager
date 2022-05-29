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
from app01 import views,models
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    #path('admin/', admin.site.urls),

    #启用media
    # 以media开头，后面除了换行符以外的换行符都被匹配
    # serve： 以media开头的, 以Django来处理
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}, name='media'),

    path('depart/list/', views.depart_show),
    path('depart/add/' ,views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:uid>/edit/', views.depart_edit),
    path('depart/multi/',views.depart_multi),
    path('user/list/', views.user_show),
    path('user/add/', views.user_add),
    path('user/<int:uid>/edit/', views.user_edit),
    path(r'user/<int:uid>/delete/', views.user_delete),
    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/<int:uid>/edit/', views.pretty_edit),
    path(r'pretty/<int:uid>/delete/', views.pretty_delete),
    path('admin/list/',views.admin_list),
    path('admin/add/',views.admin_add),
    path('admin/<int:uid>/edit/',views.admin_edit),
    path('admin/<int:uid>/delete/', views.admin_delete),
    path('admin/<int:uid>/reset/',views.admin_reset),
    path('login/',views.admin_login),
    path('logout/',views.logout),
    path('image/code/',views.image_code),
    #订单管理
    path('order/list/',views.order_list),
    path('order/add/',views.order_add),
    path('order/delete/',views.order_delete),
    path('order/detail/',views.order_detail),
    path('order/edit/',views.order_edit),
    path('chart/list/',views.chart_list),
    path('chart/bar/',views.chart_bar),
    path('chart/pie/',views.chart_pie),
    path('upload/list/',views.upload_list),
    path('upload/form/',views.upload_form),
    path('upload/modelform/',views.upload_modelform),
    path('city/list/',views.city_list),
    path('city/add/', views.city_add),
]
