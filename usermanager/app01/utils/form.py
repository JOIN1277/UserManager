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
#使用modelform实现用户添加
class UserModelFrom(bootstrapModelForm):
    #约束name字段最小长度为3
    name = forms.CharField(min_length=3,label="用户名")
    #编写正则表达式
    #password = forms.CharField(label="密码",validators=[RegexValidator(r'^159[0-9]+$','数字必须以159开头’)])
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        widgts = {
            "create_time": forms.DateTimeInput
        }


#使用modelform实现靓号添加
class PrettyModelFrom(bootstrapModelForm):
    #正则表达式校验
    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^159[0-9]+$', "格式错误，要以159开头")])
    class Meta:
        model = models.Number
        fields = ["mobile", "price", "level", "status"]
        #fields = "__all__"
        #exclude= ['level'] 排除level字段
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     # 循环找到所有插件，添加class
    #     for name,field in self.fields.items():
    #         if field.widget.attrs :
    #             field.widget.attrs["class"] = "form-control"
    #         else:
    #             field.widget.attrs = {
    #                 "class": "form-control"
    #             }
    #方式2 验证
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = Number.objects.filter(mobile=txt_mobile)
        if exists:
            raise ValidationError("手机号已存在")
        #验证通过，返回输入的值
        return txt_mobile


#使用modelform实现靓号编辑
class PrettyEditModelFrom(bootstrapModelForm):
    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^159[0-9]+$', "格式错误，要以159开头")])
    #编辑页面手机号不可编辑
    #mobile = forms.CharField(disabled=True,label="手机号")
    class Meta:
        model = models.Number
        fields = ["mobile","price", "level", "status"]
        #fields = "__all__"
        #exclude= ['level'] 排除level字段
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     # 循环找到所有插件，添加class
    #     for name,field in self.fields.items():
    #         if field.widget.attrs :
    #             field.widget.attrs["class"] = "form-control"
    #         else:
    #             field.widget.attrs = {
    #                 "class": "form-control"
    #             }

    # 方式2 验证
    def clean_mobile(self):
        #当前编辑的一行的ID
        #print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        # 当然，编辑页面手机号不可编辑时就无效 排除自己那列，如果已存在，，，
        exists = Number.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
        if exists:
            raise ValidationError("手机号已存在")
        #验证通过，返回输入的值
        return txt_mobile


#管理员添加的modelform
class AdminModelForm(bootstrapModelForm):
    #实现二次验证密码 创建一个字段
    confirm_password = forms.CharField(
        label="确认密码",
        widget = forms.PasswordInput(render_value=True)  #出现错误不清空输入框
    )
    class Meta:
        model = models.admin
        fields = ["username","password","confirm_password"]
        #定制输入框类型
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    #不允许添加相同用户名
    def clean_username(self):
        username_obj = self.cleaned_data["username"]
        exists = models.admin.objects.filter(username=username_obj)
        if exists:
            raise ValidationError("该用户名已存在")
        return username_obj
    # MD5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
    #二次输入的密码也MD5加密
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        #对二次输入的密码也加密
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm!=pwd:
            raise ValidationError("两次密码不相同")
        return confirm


#编辑管理员的modelform
class AdminEditModelFrom(bootstrapModelForm):
    #编辑页面密码不可编辑
    password = forms.CharField(disabled=True,label="密码")
    class Meta:
        model = models.admin
        fields = ["username","password"]


#重置密码modelform
class AdminResetModelForm(bootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.admin
        fields = ["password","confirm_password"]
        widgets ={
            "password": forms.PasswordInput(render_value=True)
        }
    # MD5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        #在数据库校验更改的密码是否与之前一致
        #self.instance.pk，获取当前的id ,查找数据库中该条数据是否有这个密码
        exists = models.admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("不允许与之前密码一致")
        return md5_pwd

    #二次输入的密码也MD5加密
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        #对二次输入的密码也加密
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm!=pwd:
            raise ValidationError("两次密码不相同")
        return confirm


#订单列表的modelform
class orderModelForm(bootstrapModelForm):
    #num = forms.CharField(disabled=True,label="订单号")
    class Meta:
        model = models.order
        #fields = "__all__"
        #fields = {""}
        exclude = ["num","admin"]


## 文件上传From,
class UpForm(forms.Form):
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")

    # 可以局部添加/移除样式
    bootstrap_exclude_fields = ['img']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有插件，添加class
        for name,field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs :
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {
                    "class": "form-control"
                }


#文件上传的ModelForm
class UpModelForm(bootstrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


##使用Form，自己写字段
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget = forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget = forms.PasswordInput(attrs={"class": "form-control"},render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget = forms.TextInput(attrs={"class": "form-control"}),
        required = True
    )
    ##md5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)