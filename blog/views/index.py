from django.shortcuts import render, redirect, HttpResponse
from blog import models
from django.db.models import Q
from blog.utils.pagination import Pagination

def index(request):
    queryset = models.Article.objects.all()
    page_object = Pagination(request, queryset, page_size=5)
    article_list = page_object.page_queryset
    page_string = page_object.html()
    content = {
        "article_list": article_list,
        "page_string": page_string,
    }
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


def index_tag(request,param):
    pass
