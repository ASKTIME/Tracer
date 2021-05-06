from django.shortcuts import redirect, HttpResponse, render
from WEB.forms.project import ProjectModelForm
from django.http import JsonResponse
from WEB import models


def project_list(request):
    # 自定义类把request.tracer封装
    # request.tracer.user
    # request.tracer.price_policy
    # 设置默认get提交项目列表
    # post提交则是 创建项目
    if request.method == 'GET':
        """
        1.从数据库中获取两部分数据
        我创建的	已星标 + 未星标
        我创建的	已星标	+ 未星标
        2.提取已星标
        列表 = 循环 [我创建的] + 循环 [我创建的]  把已星标的数据提取出来
        
        得到三个列表  已星标的 我创建的 我参与的

        """
        project_dict = {'star': [], 'my': [], 'join': []}
        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append(row)
            else:
                project_dict['my'].append(row)

        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        # 这里需要注意对象的不同，这里传入project对象
        for item in join_project_list:
            if item.star:
                project_dict['star'].append(item.project)
            else:
                project_dict['join'].append(item.project)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # 表单验证
    form = ProjectModelForm(request, data=request.POST, )
    print(form)
    if form.is_valid():
        # 验证通过 项目名 颜色 描述  creator 是谁创建的项目
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True, 'error': form.errors})
    return JsonResponse({'status': False, 'error': form.errors})
