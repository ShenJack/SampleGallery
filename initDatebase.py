import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SampleGallery.settings')
django.setup()

from sample.models import User, Sample

# Now this script or any imported module can use any part of Django it needs.
from django.contrib.auth.models import Group

Group.objects.update_or_create(id=1, defaults={"name": 'manager'})
Group.objects.update_or_create(id=2, defaults={"name": 'user'})

user1,createdUser1 = User.objects.update_or_create(id=1, defaults={"name": "gss", "username": "user1", "password": "asdasd",
                                              'email': "asd@asd.asd"})
if user1 is not None:
    user1.set_password("asdasd")
    user1.groups.add(Group.objects.get(name="user"))
    user1.save()
else:
    createdUser1.set_password("asdasd")
    createdUser1.groups.add(Group.objects.get(name="user"))
    createdUser1.save()

user2,createdUser2 = User.objects.update_or_create(id=2, defaults={"name": "liu", "username": "user2", "password": "asdasd",
                                              'email': "asd@asd.asd"})

if user2 is not None:
    user2.set_password("asdasd")
    user2.groups.add(Group.objects.get(name="user"))
    user2.save()
else:
    createdUser2.set_password("asdasd")
    createdUser2.groups.add(Group.objects.get(name="user"))
    createdUser2.save()

manager,createdManager = User.objects.update_or_create(id=3, defaults={"name": "manager", "username": "manager", "password": "asdasd",
                                                                       'email': "asd@asd.asd",
                                                                       })

if manager is not None:
    manager.set_password("asdasd")
    manager.groups.add(Group.objects.get(name="manager"))
    manager.save()
else:
    createdManager.set_password("asdasd")
    createdManager.groups.add(Group.objects.get(name="manager"))
    createdManager.save()

Sample.objects.update_or_create(id=1, defaults={
    'name': 'testSample', 'description': "测试样本1",
    "uploader": User.objects.get(id=1)})
Sample.objects.update_or_create(id=2, defaults={
    'name': 'testSample', 'description': "测试样本2",
    "uploader": User.objects.get(id=1)}
                                )
