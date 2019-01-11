# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        """poniższy if zmniejszanie zdjęć, aby nie obciążać zbytnio aplikacji"""

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Messages(models.Model):
    title = models.CharField(max_length=64)
    message = models.TextField()
    date_send = models.DateTimeField(auto_now_add=True)
    send_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_from")
    send_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to")
    read = models.BooleanField(default=False)
    block = models.BooleanField(default=False)

    def __str__(self):
        return f'from: {self.send_from} to: {self.send_to} message: {self.message[0:20]}'


