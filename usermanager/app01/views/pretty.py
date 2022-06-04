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

#靓号列表
def pretty_list(request):
    ##靓号列表 搜索功能
    data_dict = {}
    search_data = request.GET.get('q','') #有参数就拿到搜索的数据，无就为空
    if search_data:
        data_dict["mobile__contains"] = search_data
        #默认选择全部，筛选条件为 **data__dict，包含search_data中的值
    number = Number.objects.filter(**data_dict).order_by("-level")#按级别排序

    return render(request, "pretty_list.html", {'number': number,"search_data": search_data})

def pretty_add(request):
    title = "添加靓号"
    if request.method == "GET":
        form = PrettyModelFrom()
        return render(request, "pretty_add.html", {"form": form,'title': title})
    # 用post提交数据，数据校验
    form = PrettyModelFrom(data=request.POST)
    if form.is_valid():
        # 校验成功，保存到数据库
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'change.html', {'form': form})

def pretty_edit(request,uid):
    numObj = Number.objects.filter(id=uid).first()

    if request.method == "GET":
        form = PrettyEditModelFrom(instance=numObj)
        return render(request,"pretty_add.html",{'form':form})

    form = PrettyEditModelFrom(instance=numObj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request,"pretty_add.html",{'form':form})

def pretty_delete(request,uid):
    Number.objects.filter(id=uid).delete()
    return redirect("/pretty/list")