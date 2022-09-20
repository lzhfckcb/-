from blog import models
from django.db.models import F


def get_user_ip(request, nid):
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取用户真实IP地址
        user_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        user_ip = request.META['REMOTE_ADDR']
    models.ViewIp.objects.create(user_ip=user_ip)
    total_views_add(nid)


def total_views_add(nid):
    id = nid
    article = models.Article.objects.filter(pk=id).first()
    obj = models.ArticleViews.objects.filter(view=article).first()
    if obj == None:
        obj = models.ArticleViews.objects.create(view=article)
        obj.update(up_count=F("views") + 1)
    else:
        obj.update(up_count=F("views") + 1)
