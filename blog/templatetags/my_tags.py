from django import template
from django.db.models import Count
from blog import models

register = template.Library()

@register.inclusion_tag("home_info.html")
def get_classification_data(home_site):
    blog = models.Blog.objects.filter(site_name=home_site).first()
    user = blog.userinfo
    articles = models.Article.objects.filter(user=user)
    num = 0
    for article in articles:
        num += article.up_count
    tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count('article')).values("title", "c")
    follow_number = models.FriendShip.objects.filter(fan=user).all().count()
    fan_number = models.FriendShip.objects.filter(follow=user).all().count()
    return {"blog": blog, "user": user, "tag_list": tag_list, "follow_number": follow_number, "fan_number": fan_number, "up_count":num}

