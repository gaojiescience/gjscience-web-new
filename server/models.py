import os
from django.db import models
from .verification import create_16_code, create_64_code
from gjsicence import settings


# Create your models here.
default_avatar = os.path.join(settings.BASE_DIR, "media/avatar/default_avatar.jpg")
html_root = os.path.join(settings.BASE_DIR, "media/comments/")
print(default_avatar)


class UserProfile(models.Model):

    user_code = models.CharField("用户编号", max_length=255, null=False, blank=False, unique=True, default=create_16_code)
    phone_str = models.CharField("手机号码", max_length=255, null=True, blank=True, unique=True)
    nickname_str = models.CharField("用户名", max_length=16, null=False, blank=False, default="匿名用户")
    password_str = models.CharField("密码", max_length=255, null=False, blank=False)
    wx_str = models.CharField("微信账号", max_length=255, null=True, blank=True, unique=True)
    avatar_str = models.CharField("头像地址", max_length=255, null=True, blank=True, default=default_avatar)
    email_str = models.CharField("用户邮箱", max_length=255, null=True, blank=True, unique=True)

    class Meta:
        db_table = "UserProfile"


class StockComments(models.Model):

    comment_code = models.CharField("评论编号", max_length=255, null=False, blank=False, unique=True, default=create_16_code)
    user_code = models.CharField("绑定用户编号", max_length=255, null=False, blank=False)
    stock_code = models.CharField("股票代码", max_length=255, null=False, blank=False, default="123456")
    content_html = models.CharField("评论内容html路径", max_length=255)
    create_date = models.DateTimeField("创建时间", auto_now_add=True)
    change_date = models.DateTimeField("最后修改时间", auto_now=True)
