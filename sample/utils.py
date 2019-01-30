from hashlib import md5

from django.contrib.auth.models import Group


def encryption(chars):
    return str.upper(md5(chars.encode("utf8")).hexdigest()[:6])


def isManager(user):
    return Group.objects.get(id=1) in user.groups.all()
