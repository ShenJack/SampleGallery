from django.test import TestCase

# Create your tests here.
from django.db import models
from django.test import SimpleTestCase
from django.test.utils import isolate_apps

from sample.models import IMG


class TestModelDefinition(TestCase):
    def testImageName(self):
        image = IMG.objects.all()
        for i in image:
            print(i.img)
