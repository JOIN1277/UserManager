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

#上传文件
def upload_list(request):
    if request.method == "GET":
        return render(request,"upload_list.html")

    pic = request.FILES.get('avatar',None)
    #print(pic.name)  #文件名，a1.jpg

    f = open(pic.name,mode='wb')
    for chunk in pic.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse(",,,")

# 文件上传，Form实现组合数据上传
def upload_form(request):
    title = "FORM文件上传"
    if request.method == "GET":
        form = UpForm()
        return render(request,'upload_form.html',{"form": form,"title":title})

    form = UpForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        #1.读取图片内容，写入一个文件夹，并获取路径，
        img_obj = form.cleaned_data.get("img")

        #绝对路径
        #media_path = os.path.join(settings.MEDIA_ROOT,img_obj.name)

        #相对路径
        media_path = os.path.join("media", img_obj.name)

        #file_path = "app01/static/img/{}".format(img_obj.name)
        #file_path = os.path.join("app01",media_path)

        f = open(media_path,mode="wb")
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()

        #2.将图片路径存入数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age = form.cleaned_data['age'],
            img = media_path
        )

        return HttpResponse("---")
    return render(request,'upload_form.html',{"form": form,"title":title})

# 文件上传，modelForm实现
def upload_modelform(request):
    title = "ModelForm上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request,'upload_form.html',{"form":form,"title":title})

    form = UpModelForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        #写入数据库，自动将文件保存起来，将路径保存到数据库
        form.save()
        return HttpResponse("yes")
    return render(request, 'upload_form.html', {"form": form, "title": title})

