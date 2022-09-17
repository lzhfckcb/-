from django.shortcuts import render, HttpResponse, redirect
from blog import models


def admin_show(request):
    user_id = request.session.get("info").get("id")
    article_list = models.Article.objects.filter(user_id=user_id).all()
    return render(request, "admin.html", {"article_list": article_list})


def blog_delete(request, nid):
    id = nid
    models.Article.objects.filter(id=id).delete()
    return redirect("/blog/admin/")


def blog_add(request):
    return render(request, "blog_add.html")
