from django import forms
from WEB import models
from WEB.forms.bootstrap import BootStrapForm
from django.core.exceptions import ValidationError


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    # 重写输入插件
    # desc = forms.CharField(widget=forms.Textarea)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        # 重写输入插件
        widgets = {
            'desc': forms.Textarea,
        }

    def clean_name(self):
        """项目校验"""
        # 1.当前用户是否已经创建过此项目
        name = self.cleaned_data['name']
        exists = models.Project.objects.filter(name=name,
                                               creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目名已经存在')
        # 2.当前用户是否有额度进行创建项目
        # 当前用户能创建的最多的项目数
        project_num = self.request.tracer.price_policy.project_num
        count = models.Project.objects.filter(
            creator=self.request.tracer.user).count()
        if count >= project_num:
            raise ValidationError('创建项目超过免费额度，请购买套餐')
        return name
