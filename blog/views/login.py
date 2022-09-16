from django.shortcuts import render, HttpResponse, redirect
from blog.utils.form import Login

from blog import models
from blog.utils.code import check_code


def login(request):
    if request.method == 'GET':
        return render(request, "user_login.html")
    form = Login(data=request.POST)
    if form.is_valid():
        user_code = form.cleaned_data.pop('code')
        code = request.session.get('code', '')
        if user_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "user_login.html", {"form": form})
        admin_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "user_login.html", {"form": form})
        blog = admin_object.blog
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.name, 'site_name': blog.site_name,
                                   'avatar': str(admin_object.avatar)}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/blog/index/")
    return render(request, "user_login.html", {"form": form})


def out_login(request):
    request.session.clear()
    return redirect("/user/login/")


def image_code(request):
    """生成图片验证码"""
    from io import BytesIO

    img, code_string = check_code()

    request.session["code"] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
