from django.shortcuts import render, HttpResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings


# Create your views here.

def send_sms(request):
    """
    # 发送短信
    ?tpl=login ->927735
    ?tpl= register -> 927734
    :param request:
    :return:
    """
    # 获取到用户传入的tpl
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    # tpl有可能为空
    if not template_id:
        return HttpResponse('模板不存在')

    code = random.randrange(1000, 9999)
    # 后期手机号也会给他处理掉
    res = send_sms_single('15568595905', template_id, [code, ])
    """
    {'result': 1019, 'errmsg': 'package format error, no such sdkappid', 'ext': ''}
    审核待通过
    local_settings应该放在最后
    """
    print(res)
    return HttpResponse('ok')


# 注册实例
def register(request):

    return HttpResponse('ok')
