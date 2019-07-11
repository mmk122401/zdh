from django import template
from django.urls import reverse
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag
def reverse_url(request, name, *args, **kwargs):
    # 获取当前地址 访问目标后重新跳转的地址
    next = request.get_full_path()
    base_url = reverse(name, args=args, kwargs=kwargs)
    qd = QueryDict(mutable=True)
    qd['next'] = next
    url = '{}?{}'.format(base_url, qd.urlencode())
    return url
