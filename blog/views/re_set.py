from django.shortcuts import render, redirect, HttpResponse
from blog.utils.form import FindTelephone, FindUserModelForm
from blog import models


def verify(request):
    return render(request, "recover_verify.html")


def re_set_middle(request):
    telephone = request.POST.get("telephone")
    form = FindTelephone(data=request.POST)
    if not form.is_valid():
        return render(request, "recover_verify.html", {"form": form})

    return redirect(f"/user/reset?telephone={telephone}")


def re_set(request):
    if request.method == "GET":
        return render(request, "recover_reset.html")
    telephone = request.GET.get("telephone")
    user = models.UserInfo.objects.filter(telephone=telephone).first()
    form = FindUserModelForm(data=request.POST, instance=user)
    if form.is_valid():
        form.cleaned_data.pop("confirm_password")
        form.save()
        return redirect("/user/login/")
    return render(request, "recover_reset.html", {"form": form})
