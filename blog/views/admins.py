import json
from django.shortcuts import render, HttpResponse, redirect
from blog import models


def admin_show(request):
    user_id = request.session.get("info").get("id")
    article_list = models.Article.objects.filter(user_id=user_id).all()
    user = models.UserInfo.objects.filter(id=user_id).first()
    blog = user.blog
    tag_list = models.Tag.objects.filter(blog=blog).all()
    return render(request, "admin.html", {"article_list": article_list, "tag_list": tag_list})


def blog_delete(request, nid):
    id = nid
    models.Article.objects.filter(id=id).delete()
    return redirect("/blog/admin/")


def blog_add(request):
    return render(request, "blog_add.html")


def article_upload(request):
    user_id = request.session.get("info").get("id")
    title = request.POST.get("title")
    content = request.POST.get("content")
    models.Article.objects.create(user_id=user_id, content=content, title=title)
    return redirect("/blog/admin/")


def tag_add(request):
    if request.method == "GET":
        return render(request, "tag_add.html")
    title = request.POST.get("title")
    user_id = request.session.get("info").get("id")
    user = models.UserInfo.objects.filter(id=user_id).first()
    blog = user.blog
    models.Tag.objects.create(title=title, blog=blog)
    return redirect("/blog/admin/")


def tag_delete(request, nid):
    id = nid
    models.Tag.objects.filter(id=id).delete()
    return redirect("/blog/admin/")


def blog_edit(request, nid):
    if request.method == "GET":
        id = nid
        article = models.Article.objects.filter(id=id).first()
        return render(request, "blog_edit.html", {"article": article})
    title = request.POST.get("title")
    content = request.POST.get("content")
    id = nid
    models.Article.objects.filter(id=id).update(title=title, content=content)
    return redirect("/blog/admin/")


def tag_edit(request, nid):
    if request.method == "GET":
        id = nid
        tag = models.Tag.objects.filter(id=id).first()
        return render(request, "tag_edit.html", {"tag": tag})
    title = request.POST.get("title")
    id = nid
    models.Tag.objects.filter(id=id).update(title=title)
    return redirect("/blog/admin/")
