from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from blog import models
from django.db.models import F


def article_detail(request, article_id):
    article_object = models.Article.objects.filter(pk=article_id).first()
    user = article_object.user
    blog = user.blog
    comment_list = models.Comment.objects.filter(article_id=article_id).all()
    content = {
        "blog": blog,
        "article": article_object,
        "user": user,
        "comment_list": comment_list,
    }
    return render(request, "page.html", content)


def digg(request):
    article_id = request.POST.get("article_id")
    user_id = request.session.get("info").get("id")
    obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    response = {
        "status": True
    }
    if not obj:
        models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id)
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
    else:
        response["status"] = False
    return JsonResponse(response)


def comment(request):
    user_id = request.session.get("info").get("id")
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    data = models.Comment.objects.create(
        user_id=user_id,
        article_id=article_id,
        content=content,
        parent_comment_id=pid,
    )
    models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
    return  HttpResponse("成功")
