# 用户账户相关的功能写在这里

from django.shortcuts import render, HttpResponse, redirect
from WEB.forms.account import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginForm
from django.http import JsonResponse
from WEB import models


def register(request):
    """ 注册 """
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 验证通过存储到数据库中 缺陷 密码是明文 需要是密文
        # 密码在 forms中处理
        instance = form.save()
        # print(instance)
        # instance = form.save()  # 这一步骤相当于以下
        # 这段牛逼之处在于能够把传入的数据没有用的地方都剔除掉 如重复确认密码 等等
        # form.cleaned_data.pop('code')
        # form.cleaned_data.pop('confirm')
        # instance = models.UserInfo.objects.create(**form.cleaned_data)
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """ 发送短信 """
    # 只是获取手机号， 不能为空 格式正确
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        # 发短信 通过钩子函数进行校验
        # 写入redis
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    form = LoginSmsForm()
    return render(request, 'login_sms.html', {'form': form})


def login(request):
    # 用户名密码登录
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        from django.db.models import Q
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)) \
            .filter(password=password).first()
        if user_object:
            # 登录成功为止1
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('index')

        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    # 生成图片验证码
    from utils.image_code import check_code
    from io import BytesIO
    image_object, code = check_code()
    stream = BytesIO()
    image_object.save(stream, 'png')
    print(code)
    request.session['image_code'] = code
    # 设置超时时间60s
    request.session.set_expiry(60)
    # 验证码需要加到session中
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')
