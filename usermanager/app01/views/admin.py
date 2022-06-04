# author:klx
# time:2022/6/4 -{TIME}
# function:
#
from django.http import HttpResponse
from django.shortcuts import render,redirect
from app01.models import Department,UserInfo,Number,admin,Boss,City
from django import forms
from app01 import models
from django.core.validators import RegexValidator,ValidationError
from app01.utils.bootstrap import bootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from django.http import JsonResponse
import random
import os
from datetime import datetime
from django.conf import settings
from app01.utils.form import UserModelFrom,PrettyModelFrom,AdminModelForm,AdminEditModelFrom,AdminResetModelForm,orderModelForm,UpForm,UpModelForm,PrettyEditModelFrom
from openpyxl import load_workbook
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def admin_list(request):
    ##管理员列表
    #检测用户是否登录，已登录，继续，未登录，跳转登录页
    #用户发来的请求， 获取cookie随机字符串，拿字符串看看session中有没有
    # info = request.session.get["info"] #到这一步一定拿到session了
    # if not info:
    #     return redirect("/login/")

    ##管理员列表 搜索功能
    data_dict = {}
    search_data = request.GET.get('q','') #有参数就拿到搜索的数据，无就为空
    if search_data:
        data_dict["username__contains"] = search_data
        #默认选择全部，筛选条件为 **data__dict，包含search_data中的值
    queryset = admin.objects.filter(**data_dict)
    context = {
        'queryset': queryset,
        'search_data': search_data,

    }
    return render(request,"admin_list.html",context)

##添加管理员
def admin_add(request):
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html',{'form': form ,"title": title })

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        #展示所有通过验证的数据
        #print(form.cleaned_data)
        #{'username': 'root', 'password': '123', 'confirm_password': '123'}
        form.save()
        return redirect("/admin/list/")

    return render(request, 'change.html',{'form': form ,"title": title })

#管理员编辑
def admin_edit(request,uid):
    title = "编辑管理员"
    #先获取一个对象，判断是否存在
    admin_obj = models.admin.objects.filter(id=uid).first()
    if not admin_obj:
        return render(request,"404.html",{"error_msg": "404 NOT FOUND!!"})
    if request.method == 'GET':
        #显示原来的值
        form = AdminEditModelFrom(instance=admin_obj)
        return render(request,'change.html',{"title": title,"form": form})

    form = AdminEditModelFrom(data=request.POST, instance=admin_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"title": title, "form": form})

#管理员删除
def admin_delete(request,uid):
    admin_obj = models.admin.objects.filter(id=uid).first()
    if not admin_obj:
        return render(request,"404.html",{"error_msg": "404 NOT FOUND!!"})
    admin.objects.filter(id=uid).delete()
    return redirect("/admin/list/")

#管理员重置密码
def admin_reset(request,uid):
    admin_obj = models.admin.objects.filter(id=uid).first()
    if not admin_obj:
        return render(request, "404.html", {"error_msg": "404 NOT FOUND!!"})

    title = "重置密码 - {}".format(admin_obj.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"title": title,"form": form})

    form = AdminResetModelForm(data=request.POST,instance=admin_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,"change.html",{"form": form,"title": title})

