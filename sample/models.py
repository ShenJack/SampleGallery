import datetime
import json

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
from sample.utils import encryption


class UpdateMixin(object):
    def update(self, **kwargs):
        if self._state.adding:
            raise self.DoesNotExist
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())


class User(AbstractUser, UpdateMixin):
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=20, default="")
    contact = models.CharField(max_length=20, default="")


class Sample(models.Model, UpdateMixin):
    STATE_NEED_REVIEW = "NR"
    STATE_REJECTED = "RJ"
    STATE_PASSED = 'PS'
    STATE_CHOICES = (
        (STATE_NEED_REVIEW, '待审核'),
        (STATE_PASSED, '审核通过'),
        (STATE_REJECTED, '审核未通过'),
    )

    STATE_UNAVAILABLE = "UA"
    STATE_AVAILABLE = "AV"
    STATE_WAIT = "WT"
    STATE_LENT = "LT"

    STATE_LEND = (
        (STATE_UNAVAILABLE, "不可借"),
        (STATE_AVAILABLE, '可借'),
        (STATE_WAIT, '等待领取'),
        (STATE_LENT, '已借出'),
    )

    STATE_WAIT_APPLY = "WA"
    STATE_ALREADY_APPLIED = "AP"
    STATE_IN_STORAGE = "IS"

    STATE_CHECKIN = (
        (STATE_WAIT_APPLY, '未申请'),
        (STATE_ALREADY_APPLIED, '等待入库'),
        (STATE_IN_STORAGE, '已入库'),
    )

    name = models.TextField()
    description = models.TextField()
    uploader = models.ForeignKey(to=User, related_name='samples', on_delete=models.SET_DEFAULT, default=1)
    uploadTime = models.DateTimeField(default=timezone.now)
    reviewedTime = models.DateTimeField(default=timezone.now)
    passTime = models.DateTimeField(default=timezone.now)
    reviewed = models.BooleanField(default=False)
    reviewState = models.CharField(choices=STATE_CHOICES, max_length=2, default=STATE_NEED_REVIEW)

    # About Lending
    isEntity = models.BooleanField(default=False)
    lendStatus = models.CharField(choices=STATE_LEND, max_length=2, default=STATE_UNAVAILABLE)
    checkinStatus = models.CharField(choices=STATE_CHECKIN, max_length=2, default=STATE_WAIT_APPLY)
    borrowable = models.BooleanField(default=False)

    checkinCode = models.CharField(max_length=6, default="")

    # About Colony Sample

    # 菌种
    bacteria = models.TextField(default="未知")

    # 培养基
    medium = models.TextField(default="未知")

    # Function
    def inStorage(self):
        return self.checkinStatus == self.STATE_IN_STORAGE


class IMG(models.Model):
    img = models.ImageField(upload_to='static/img')
    sample = models.ForeignKey(related_name='pics', on_delete=models.CASCADE, to=Sample, default=1)

    def path(self):
        return self.img.name


def update(model, **kwargs):
    if model._state.adding:
        raise model.DoesNotExist
    for field, value in kwargs.items():
        setattr(model, field, value)
    model.save(update_fields=kwargs.keys())


class Lend(models.Model):
    from_user = models.ForeignKey(to=User, related_name='lend', on_delete=models.CASCADE)
    to_sample = models.ForeignKey(to=Sample, related_name='lend', on_delete=models.CASCADE)
    createTime = models.DateTimeField(default=timezone.now)
    pickTime = models.DateTimeField(default=timezone.now)
    returnTime = models.DateTimeField(default=timezone.now)
    latestReturnTime = models.DateTimeField(default=timezone.now)
    latestPickTime = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=6, default="")

    def init(self):
        self.latestPickTime = self.createTime + datetime.timedelta(days=7)
        self.latestReturnTime = self.createTime + datetime.timedelta(days=31)
        self.code = encryption(str(self.from_user.id) + str(self.to_sample.id) + "lend")
        self.save()
