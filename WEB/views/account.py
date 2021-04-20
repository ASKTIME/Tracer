# 用户账户相关的功能写在这里

from django.shortcuts import render
from WEB.forms.account import RegisterModelForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
