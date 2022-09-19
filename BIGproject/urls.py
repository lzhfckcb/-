"""BIGproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from blog.views import register, home, login, article, re_set, index, admins, person

urlpatterns = [
    path('image/code/', login.image_code),
    path('user/login/', login.login),
    path('user/outlogin/', login.out_login),
    path('user/register/', register.register),
    path('admin/', admin.site.urls),
    path('recover/verify/', re_set.verify),
    path('recover/reset/', re_set.re_set_middle),
    path('user/reset/', re_set.re_set),
    path('blog/index/', index.index),
    path('index/ranking/', index.index_ranking),
    path('index/search/', index.index_search),
    path('index/tag/', index.index_tag),
    path('index/friendship/', index.index_friendship),
    path("digg/", article.digg),
    path("comment/", article.comment),
    path("blog/admin/", admins.admin_show),
    path("blog/add/", admins.blog_add),
    path("article/upload/", admins.article_upload),
    path("blog/delete/<int:nid>/", admins.blog_delete),
    path("tag/delete/<int:nid>/", admins.tag_delete),
    path("blog/edit/<int:nid>/", admins.blog_edit),
    path("tag/add/", admins.tag_add),
    path("tag/edit/<int:nid>/", admins.tag_edit),
    path("friendship/add/", home.friendship_add),
    path("person/edit/<int:nid>", person.person_edit),
    re_path('index/tag/(?P<param>.*)/$', index.index_tag),
    re_path('^(?P<home_site>\w+)$', home.home_site),
    re_path('^(?P<home_site>\w+)/tag/(?P<param>.*)/$', home.home_site),
    re_path('article/(?P<article_id>.*)/$', article.article_detail),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

]
