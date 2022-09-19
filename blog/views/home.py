from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from blog import models
from blog.utils.pagination import Pagination


def home_info(home_site, **kwargs):
    blog = models.Blog.objects.filter(site_name=home_site).first()
    if not blog:
        return
    param = kwargs.get("param")
    user = blog.userinfo
    if param:
        article_list = models.Article.objects.filter(user=user).filter(tags__title=param)
    else:
        article_list = models.Article.objects.filter(user=user)
    content = {
        "blog": blog,
        "article_lists": article_list,
        "user": user,
    }
    return content


def home_site(request, home_site, **kwargs):
    content = home_info(home_site, **kwargs)
    if not content:
        return HttpResponse("博客不存在。")
    queryset = content.get("article_lists")
    page_object = Pagination(request, queryset, page_size=4)
    content["article_list"] = page_object.page_queryset
    content["page_string"] = page_object.html()
    return render(request, "home_index.html", content)


def friendship_add(request):
    fan_id = request.POST.get("fan")
    follow_id = request.POST.get("follow")
    exist = models.FriendShip.objects.filter(fan_id=fan_id, follow_id=follow_id)
    response = {
        "status": True
    }
    if not exist:
        models.FriendShip.objects.create(fan_id=fan_id, follow_id=follow_id)
    else:
        response["status"] = False
    return JsonResponse(response)