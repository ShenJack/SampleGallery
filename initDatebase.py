import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SampleGallery.settings')
django.setup()

from sample.models import User, Sample

# Now this script or any imported module can use any part of Django it needs.
from django.contrib.auth.models import Group

Group.objects.update_or_create(id=1, defaults={"name": 'manager'})
Group.objects.update_or_create(id=2, defaults={"name": 'user'})

manager,createdManager = User.objects.update_or_create(id=1, defaults={"name": "manager", "username": "manager", "password": "asdasd",
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
