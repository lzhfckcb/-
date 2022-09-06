from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

"""此模块为中间件，用来实现登录功能"""


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in ["/user/register/", "/user/login/", "/image/code/", "/recover/verify/", "/recover/reset/", "/user/reset/"]:
            return
        info_dict = request.session.get("info")
        if not info_dict:
            return redirect("/user/login/")
        return

    def process_response(self, request, response):
        return response
