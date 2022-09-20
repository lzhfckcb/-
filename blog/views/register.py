from django.shortcuts import render, redirect
from blog.utils.form import UserModelForm
from blog import models


def register(request):
    if request.method == "GET":
        return render(request, "user_register.html")
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.cleaned_data.pop("confirm_password")
        form.save()
        creat_home(form)
        return redirect("/user/login/")
    else:
        return render(request, "user_register.html", {"form": form})


# Create your views here.


def creat_home(form):
    name = form.cleaned_data.get("name")
    blog = models.Blog.objects.create(title=name, site_name=name)
    models.UserInfo.objects.filter(name=name).update(blog=blog)

