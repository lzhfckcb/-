from django.shortcuts import render, HttpResponse
from blog import models


def article_detail(request, article_id):
    article_object = models.Article.objects.filter(pk=article_id).first()
    user = article_object.user
    blog = user.blog
    content = {
        "blog": blog,
        "article": article_object,
        "user": user,
    }
    return render(request, "article.html", content)
