# author:klx
# time:2022/5/10 -{TIME}
# function:定义登录验证中间件
#
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect

class authMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #排除不需要登陆就可以访问的页面，否则回无限循环发送请求
        if request.path_info in ['/login/','/image/code/']:
            return
        # 1.如果有登录信息,就可以向后走
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 2.没有登陆过,认证失败，重新登陆
        return redirect('/login/')