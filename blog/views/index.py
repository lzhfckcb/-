from django.shortcuts import render, redirect, HttpResponse
from blog import models
from django.db.models import Count
from django.db.models import Q
from blog.utils.pagination import Pagination


def index(request):
    queryset = models.Article.objects.all()
    page_object = Pagination(request, queryset, page_size=5)
    article_list = page_object.page_queryset
    page_string = page_object.html()
    name = request.session.get("info").get("name")
    user = models.UserInfo.objects.filter(name=name).first()
    content = {
        "article_list": article_list,
        "page_string": page_string,
        "user": user,
    }
    print(user)
    return render(request, "index_content.html", content)


def index_search(request):
    flag = ""
    content = request.GET.get("search")
    article_list = models.Article.objects.filter(
        Q(title__contains=content) | Q(content__contains=content) | Q(desc__contains=content))
    if not article_list:
        flag = "什么都没有找到哦"
    return render(request, "index_content.html", {"article_list": article_list, "flag": flag})


def index_ranking(request):
    article_list = models.Article.objects.order_by('-up_count')[:10]
    return render(request, "ranking_content.html", {"article_list": article_list})


def index_tag(request, **kwargs):
    tag_list = models.Tag.objects.all().values("pk").annotate(c=Count('article')).values("title", "c")
    param = kwargs.get('param')
    if param:
        queryset = models.Article.objects.filter(tags__title=param)
    else:
        queryset = models.Article.objects.all()
    page_object = Pagination(request, queryset, page_size=5)
    article_list = page_object.page_queryset
    page_string = page_object.html()
    return render(request, "index_tag.html",
                  {"tag_list": tag_list, "article_list": article_list, "page_string": page_string})


def index_friendship(request):
    user_name = request.session.get("info").get("name")
    user = models.UserInfo.objects.filter(name=user_name).first()
    follow = models.FriendShip.objects.filter(fan=user).all()
    article_list = []
    for item in follow:
        articles = models.Article.objects.filter(user=item.follow).first()
        article_list.append(articles)
    return render(request, "index_friendship.html", {"article_list": article_list, "follow": follow})
