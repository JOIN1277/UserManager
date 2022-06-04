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

def city_list(request):
    city_obj = models.City.objects.all()
    return render(request,"city_list.html",{"city_obj":city_obj})

def city_add(request):
    title = "新建城市"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 写入数据库，自动将文件保存起来，将路径保存到数据库
        form.save()
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, "title": title})