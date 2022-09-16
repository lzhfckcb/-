from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserInfo(models.Model):
    """用户信息"""
    name = models.CharField(verbose_name="昵称", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    telephone = models.CharField(verbose_name="手机号", max_length=11)
    avatar = models.FileField(verbose_name="头像", max_length=128, default="/avatars/default.jpg")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    introduction = models.TextField(verbose_name='简介', default="他什么都没有写哦。")
    blog = models.OneToOneField(to="Blog", to_field="id", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FriendShip(models.Model):
    fan = models.ForeignKey(UserInfo, related_name='fan', on_delete=models.CASCADE)
    follow = models.ForeignKey(UserInfo, related_name='follow', on_delete=models.CASCADE)

    def __str__(self):
        return "{}关注了{}".format(self.fan, self.follow)


class Blog(models.Model):
    """博客信息表（站点表）"""
    title = models.CharField(verbose_name="个人博客标题", max_length=64)
    site_name = models.CharField(verbose_name="站点名称", max_length=64)
    theme = models.CharField(verbose_name="博客主题", max_length=32)

    def __str__(self):
        return self.title


class Article(models.Model):
    """博客文章表"""
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    up_count = models.IntegerField(verbose_name="赞数", default=0)
    down_count = models.IntegerField(verbose_name="踩数", default=0)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    content = models.TextField()

    def __str__(self):
        return self.title


class ArticleUpDown(models.Model):
    """点赞表"""
    user = models.ForeignKey(to='UserInfo', null=True, on_delete=models.CASCADE, to_field="id")
    article = models.ForeignKey(to="Article", null=True, on_delete=models.CASCADE, to_field="id")
    is_up = models.BooleanField(default=True)


class Comment(models.Model):
    """评论表"""
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey(to='self', null=True, on_delete=models.SET_NULL, to_field="id")


class Tag(models.Model):
    """标签表"""
    title = models.CharField(verbose_name="标签名称", max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='id', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        v = self.article.title + "---" + self.tag.title
        return v
