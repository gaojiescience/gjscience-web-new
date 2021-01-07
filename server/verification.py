import redis
import random
import string
import json
import os
from django.shortcuts import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from gjsicence import settings
from django.core import serializers

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
cursor = redis.Redis(connection_pool=pool)
base_dir = settings.BASE_DIR


def create_default_avatar(name, code):
    if name[0].isalpha():
        try:
            avatar_name = name[0].upper() + name[1]
            font = ImageFont.truetype(os.path.join(base_dir, "/static/fonts/arial.ttf"), size=20)
        except IndexError:
            avatar_name = name[0]
            font = ImageFont.truetype(os.path.join(base_dir, "/static/fonts/SIMYOU.TTF"), size=20, encoding="unic")
    else:
        avatar_name = name[0]
        font = ImageFont.truetype(os.path.join(base_dir, "/static/fonts/SIMYOU.TTF"), size=20, encoding="unic")
    path = os.path.join(os.path.abspath(os.path.join(base_dir, "/static/avatar/")), name + "-" + code + ".png")
    base_img = Image.new("RGB", (50, 50), "white")
    d = ImageDraw.Draw(base_img)
    d.text((15, 15), avatar_name, font=font, fill=(110, 110, 110, 128))
    with open(path, "wb") as f:
        base_img.save(f, font=font, format="png")
    return "/static/avatar/" + name + "-" + code + ".png"


def create_16_code():
    code = ""
    for word in range(16):
        code += random.choice(string.ascii_letters)
    print(code)
    return code


def create_64_code():
    code = ""
    for word in range(64):
        code += random.choice(string.ascii_letters)
    print(code)
    return code


class VerificationCodeManager(object):

    def __init__(self):
        self.pool = pool,
        self.cursor = cursor
        self.pool_length = 1000

    @staticmethod
    def create_code():
        code = ""
        for num in range(0, 6):
            code += random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        return code

    def set_email(self, type_, code):
        self.cursor.set(code + "_" + type_ + "_verification", VerificationCodeManager.create_code(), ex=600)

    def get(self, type_, code):
        verification_code = self.cursor.get(code + "_" + type_ + "_verification")
        if code:
            return [200, verification_code]
        else:
            return [404, None]
    # def check_pool(self):
    #     if len(self.pool) == self.pool_length:


class TokenManager(object):

    def __init__(self):
        self.pool = pool
        self.cursor = cursor
        self.pool_length = 1000

    def get(self, code):
        token = self.cursor.get(code+"_token")
        return token

    def create(self, code):
        token = create_64_code()
        self.cursor.set(code+"_token", token, ex=604800)
        # self.cursor.set("lol", "lol")
        return 200

    def check(self, func):

        def inner_func(items, request):
            token = request.GET.get("token")
            code = request.GET.get("code")
            if token == self.get(code).decode("utf-8"):
                return func(items, request)
            else:
                return HttpResponse(json.dumps([500, None]))
        return inner_func
