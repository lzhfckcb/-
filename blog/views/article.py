from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from blog import models
from django.db.models import F


def article_detail(request, article_id):
    article_object = models.Article.objects.filter(pk=article_id).first()
    user = article_object.user
    blog = user.blog
    content = {
        "blog": blog,
        "article": article_object,
        "user": user,
    }
    return render(request, "page.html", content)


def digg(request):
    article_id = request.POST.get("article_id")
    user_id = request.session.get("info").get("id")
    user = models.UserInfo.objects.filter(pk=user_id).first()
    article = models.Article.objects.filter(pk=article_id).first()
    obj = models.ArticleUpDown.objects.filter(user=user, article=article).first()
    response = {
        "status": True
    }
    if not obj:
        models.ArticleUpDown.objects.create(user=user, article=article)
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
    else:
        response["status"] = False
    return JsonResponse(response)