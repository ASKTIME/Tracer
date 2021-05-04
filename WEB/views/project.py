from django.shortcuts import redirect, HttpResponse, render


def project_list(request):
    # 自定义类把request.tracer封装
    # request.tracer.user
    # request.tracer.price_policy

    return render(request, 'project_list.html')
