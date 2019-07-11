from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from crm import models


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in [reverse('login'), reverse('reg')]:
            return
        if request.path_info.startswith('/admin'):
            return
        # 获取登录session的pk
        pk = request.session.get('pk')
        obj = models.UserProfile.objects.filter(pk=pk).first()
        if not obj:  # 如果没有pk，就是没有登录
            return redirect(reverse('login'))
        # 登录了 保存obj
        request.user_obj = obj
