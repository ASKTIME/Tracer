# 用户账户相关的功能写在这里

from django.shortcuts import render, HttpResponse
from WEB.forms.account import RegisterModelForm, SendSmsForm
from django.http import JsonResponse


def register(request):
    """ 注册 """
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def send_sms(request):
    """ 发送短信 """
    # 只是获取手机号， 不能为空 格式正确
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        # 发短信 通过钩子函数进行校验
        # 写入redis
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
