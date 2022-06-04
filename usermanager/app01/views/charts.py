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

#数据统计展示页面
def chart_list(request):
    return render(request,"chart_list.html")

#构造柱状图的数据
def chart_bar(request):
    # #数据库中获取数据
    legend = ["销量","业绩"]
    # x_axis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    # series_list = [
    #       {
    #         "name": '销量',
    #         "type": 'bar',
    #         "data": [5, 20, 36, 10, 10, 20]
    #       },
    #       {
    #         "name": '业绩',
    #         "type": 'bar',
    #         "data": [1, 40, 23, 10, 10, 5]
    #       }
    #     ]
    # result = {
    #     "status":True,
    #     "data":{
    #         "legend":legend,
    #         "x_axis":x_axis,
    #         "series_list":series_list
    #     }
    # }
    # return JsonResponse(result)
    objs = models.UserInfo.objects.all()
    return render(request,"chart_list.html",locals())

#构造饼图数据
def chart_pie(request):
    user_obj = models.UserInfo.objects.all()

    db_data_list = [
                { "value": 1048, "name": '公安部' },
                { "value": 735, "name": '交通部' },
                { "value": 580, "name": '运营' },
              ]

    result = {
        "status": True,
        "data": db_data_list,
    }
    return JsonResponse(result)
