# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
# wpisujemy to jeśli chcemy mieć na stronie http://127.0.0.1:8000/admin/
# sekcję "profil" i zarządzać nią w aplikacji
