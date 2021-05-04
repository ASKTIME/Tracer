from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from WEB import models
from django.conf import settings
import datetime


class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None



class AuthMiddleware(MiddlewareMixin):
    # 如果用户登录，则在request中赋值，在整个程序中都可以得到
    def process_request(self, request):
        request.tracer = Tracer()

        user_id = request.session.get('user_id')
        user_object = models.UserInfo.objects.filter(id=user_id).first()

        request.tracer.user = user_object

        # 白名单
        """
        1.获取用户当前访问的url
        2.检查用户是否在当前的白名单中，如果在则继续访问，不在则判断是否已经登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            return redirect('login')

        # 获取当前用户的额度
        """
        在用户登录成功之后，访问后台管理的时候获取当前用户所拥有的的额度
        方式1 在交易记录中获取
        获取当前用户id值最大(最大的交易记录)
        """

        _object = models.Transaction.objects.filter(user=user_object, status=2) \
            .order_by('-id').first()
        # 判断使用时间是否过期(免费用户无限期)
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            # 过期
            # _object = models.Transaction.objects.filter(user=user_object, status=2) \
            #     .order_by('-id').first()
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        # tracer_object.price_policy = _object.price_policy
        request.tracer.price_policy = _object.price_policy

        # 方式二： 免费的额度存储配置文件
        # 获取当前用户的id值最大(最近交易记录)
        # _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # if not _object:
        #     # 没有购买
        #     request.price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        # else:
        #     # 付费购买了
        #     current_datetime = datetime.datetime.now()
        #     if _object.end_datetime and _object.end_datetime < current_datetime:
        #         request.price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        #     else:
        #         request.price_policy = _object.price_policy
