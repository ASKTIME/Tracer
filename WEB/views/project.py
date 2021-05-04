from django.shortcuts import redirect, HttpResponse, render
from WEB.forms.project import ProjectModelForm
from django.http import JsonResponse


def project_list(request):
    # 自定义类把request.tracer封装
    # request.tracer.user
    # request.tracer.price_policy
    # 设置默认get提交项目列表
    # post提交则是 创建项目
    if request.method == 'GET':
        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form})

    # 表单验证
    form = ProjectModelForm(request, data=request.POST, )
    print(form)
    if form.is_valid():
        # 验证通过 项目名 颜色 描述  creator 是谁创建的项目
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True, 'error': form.errors})
    return JsonResponse({'status': False, 'error': form.errors})
