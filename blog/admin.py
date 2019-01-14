# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post, Comment

# Register your models here.

admin.site.register(Post)
# wpisujemy to jeśli chcemy mieć na stronie http://127.0.0.1:8000/admin/
# sekcję "posts" i zarządzać nią w aplikacji

admin.site.register(Comment)

