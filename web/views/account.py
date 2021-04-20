# 用户账户相关的功能写在这里

from django.shortcuts import render


def register(request):
    return render(request, 'register.html')
