from django.shortcuts import render, redirect
from blog.utils.form import UserModelForm


def register(request):
    if request.method == "GET":
        return render(request, "user_register.html")
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.cleaned_data.pop("confirm_password")
        form.save()
        return redirect("/user/login/")
    else:
        return render(request,  "user_register.html", {"form": form})
# Create your views here.
