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

def order_list(request):
    order_obj = models.order.objects.all().order_by('id')
    form = orderModelForm
    context={
        "form": form,
        "order_obj": order_obj,
    }
    return render(request,'order_list.html',context)

@csrf_exempt #免除csrf_token认证
## 新建订单，通过ajax请求
def order_add(request):
    form = orderModelForm(data = request.POST)
    if form.is_valid():

        #创建一个num(订单编号)一起保存
        form.instance.num = datetime.now().strftime("%Y%M%d%H%M%S") + str(random.randint(1000,9999))

        #设置一个管理员的信息一起写入数据库 （当前登陆的session中拿到id）
        form.instance.admin_id = request.session["info"]["id"]

        form.save()
        return JsonResponse({"status": True})
       # return HttpResponse(json.dumps({"status": True}))

    return JsonResponse({"status": False, 'error': form.errors})

#订单删除
def order_delete(request):
    nid = request.GET.get("nid")
    exists = models.order.objects.filter(id=nid).exists()
    if not exists:
        return JsonResponse({"status": False,"error": "删除失败,数据不存在"})
    models.order.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})

#编辑展示订单详情
def order_detail(request):
    """ 方式一 ：    根据ID获取订单详情
    nid = request.GET.get("nid")
    //获取到一个对象。
    order_obj = models.order.objects.filter(id=nid).first()
    if not order_obj:
        return JsonResponse({"status": False,"error": "数据不存在"})
    #从数据库获取对象，order_obj
    order_dict = {
        "status": True,
        "data":{
            "title": order_obj.title,
            "price": order_obj.price,
            "status": order_obj.status,
        }
    }
    return JsonResponse(order_dict)
    """
    #方式二
    nid = request.GET.get("nid")
    # 获取到一个对象。
    order_dict = models.order.objects.filter(id=nid).values("title", "price", "status").first()
    if not order_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})

    order_obj = {
        "status": True,
        "data": order_dict
    }
    return JsonResponse(order_obj)

#订单编辑
@csrf_exempt
def order_edit(request):
    nid = request.GET.get("nid")
    order_obj = models.order.objects.filter(id=nid).first()
    if not order_obj:
        return JsonResponse({"status": False, "tips": "数据不存在"})

    form = orderModelForm(data=request.POST,instance = order_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})
