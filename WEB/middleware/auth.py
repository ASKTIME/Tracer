from django.utils.deprecation import MiddlewareMixin
from WEB import models


class AuthMiddleware(MiddlewareMixin):
    # 如果用户登录，则在request中赋值，在整个程序中都可以得到
    def process_request(self, request):
        user_id = request.session.get('user_id')
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object
