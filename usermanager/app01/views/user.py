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


def user_show(request):
    userinfo = UserInfo.objects.all()
    #userinfo.gender ## 1/2
    #userinfo.get_字段名称_display()
    #userinfo.depart_id 拿原始的值，
    #userinfo.depart.title   拿值对应的信息 （有表关联情况）
    #
    return render(request,"user_list.html",{'userinfo':userinfo})

def user_add(request):
    title = "新建用户"
    if request.method=="GET":
        form = UserModelFrom()
        return render(request,"user_add.html",{"form":form,"title": title })
    #用post提交数据，数据校验
    form = UserModelFrom(data=request.POST)
    if form.is_valid():
        #校验成功，保存到数据库
        form.save()
        return redirect('/user/list/')
    else:
        return render(request,'change.html',{'form':form})

#用户编辑
def user_edit(request,uid):
    userObj = UserInfo.objects.filter(id=uid).first()
    if request.method == "GET":
        #根据id找到当前数据库中的数据
       # userObj = UserInfo.objects.filter(id=uid).first()
        form = UserModelFrom(instance=userObj) # 把默认数据传递进去为了显示原来的数据
        return render(request, "user_edit.html", {'form': form})
    #用post提交数据，数据校验
    # 数据修改的信息，给数据库的哪一行做修改？
    #userObj = UserInfo.objects.filter(id=uid).first()
    form = UserModelFrom(instance=userObj,data=request.POST)
    if form.is_valid():
        #校验成功，保存到数据库
       # form.instance.password = 999    除了用户输入的值
        form.save()
        return redirect('/user/list/')
    else:
        return render(request,'user_add.html',{'form':form})

#用户删除
def user_delete(request,uid):
    #删除部门
    #删除指定id的用户信息
    UserInfo.objects.filter(id=uid).delete()
    #跳转回列表
    return redirect("/user/list/")