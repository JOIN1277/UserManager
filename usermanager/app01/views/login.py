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
from app01.utils.form import UserModelFrom,PrettyModelFrom,LoginForm,AdminModelForm,AdminEditModelFrom,AdminResetModelForm,orderModelForm,UpForm,UpModelForm,PrettyEditModelFrom
from openpyxl import load_workbook
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def admin_login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,"login.html",{"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        #表示验证成功，拿到用户名密码
        #form.cleaned_data

        #验证码校验
        #由于数据库中没有code,所有要剔除掉，只保留用户名密码
        user_input_code = form.cleaned_data.pop('code')
        image_code = request.session.get('image_code',"")
        if image_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        # 通过数据库校验
        # 复杂：models.admin.objects.filter(username="xxx",password="xxx").first()
        admin_obj = models.admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password","用户名密码错误")
            return render(request, 'login.html', {"form": form})
        #输入正确继续操作
        #网站生成随机字符串，写到用户浏览器的cookie中，；再写入session中
        #将info（代表用户的身份信息）自动保存到服务器
        request.session["info"] = {'id': admin_obj.id ,'name': admin_obj.username}

        #重新设置session超时时间
        request.session.set_expiry(60*60*24*7)
        return redirect('/admin/list/')
    return render(request,'login.html',{"form": form})

# 注销
def logout(request):
    #清除会话数据，在存储中删除会话的整条数据
    request.session.clear()
    return redirect('/login/')

from io import BytesIO
#生成图片验证码
def image_code(request):
    #调用pillow函数，生成图片
    img, code = check_code()
    #print(code)

    #将生成的验证码保存到用户session中(以便后续获取验证码进行校验)
    request.session['image_code'] = code
    #设置session60秒超时
    request.session.set_expiry(60)

    #图片内容写入内存中，
    stream = BytesIO()
    img.save(stream,'png')
    #从内存中把原始数据取到
    return HttpResponse(stream.getvalue())
