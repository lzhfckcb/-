import os
from BIGproject import settings
from django.shortcuts import render, HttpResponse, redirect
from blog import models


def person_edit(request, nid):
    if request.method == "GET":
        id = nid
        user = models.UserInfo.objects.filter(id=id).first()
        blog = user.blog
        return render(request, "person_info.html", {"user": user, "blog": blog})
    name = request.POST.get("name")
    telephone = request.POST.get("telephone")
    site_name = request.POST.get("site_name")
    introduction = request.POST.get("introduction")
    id = nid
    user = models.UserInfo.objects.filter(id=id).first()
    models.UserInfo.objects.filter(id=id).update(name=name, telephone=telephone, introduction=introduction)
    exist = models.Blog.objects.filter(userinfo=user).exists()
    if not exist:
        models.Blog.objects.create(title=user.name, site_name=site_name)
    else:
        models.Blog.objects.filter(userinfo=user).update(title="{}的站点".format(user.name), site_name=site_name)
    request.session["info"] = {
        "id": id,
        "name": name,
        "site_name": site_name,
        'avatar': "/avatars/default.jpg"
    }
    avatar = request.FILES.get("avatar")
    if avatar:
        media_path = os.path.join(settings.MEDIA_ROOT, avatar.name)
        f = open(media_path, mode='wb')
        for chunk in avatar.chunks():
            f.write(chunk)
        f.close()
        models.UserInfo.objects.filter(id=id).update(avatar=media_path)
    return redirect("/{}".format(site_name))
