import json

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
STATE_NEED_REVIEW = "NR"
STATE_REJECTED = "RJ"
STATE_PASSED = 'PS'
STATE_CHOICES = (
    (STATE_NEED_REVIEW, '待审核'),
    (STATE_PASSED, '审核通过'),
    (STATE_REJECTED, '审核未通过'),
)


class Sample(models.Model):
    name = models.TextField()
    description = models.TextField()
    uploader = models.ForeignKey('auth.User', related_name='samples', on_delete=models.SET_DEFAULT, default=1)
    uploadTime = models.DateTimeField(default=timezone.now())
    reviewedTime = models.DateTimeField(default=timezone.now())
    passTime = models.DateTimeField(default=timezone.now())
    reviewed = models.BooleanField(default=False)
    reviewState = models.CharField(choices=STATE_CHOICES, max_length=2, default=STATE_NEED_REVIEW)


class IMG(models.Model):
    img = models.ImageField(upload_to='static/img')
    sample = models.ForeignKey(related_name='pics', on_delete=models.CASCADE, to=Sample,default=1)
    name = models.CharField(max_length=20)

    def path(self):
        return self.img.name
