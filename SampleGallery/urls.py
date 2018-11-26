"""SampleGallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from sample.models import Sample
from sample.permissions import IsOwnerOrReadOnly


class UserSerializer(serializers.HyperlinkedModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True, queryset=Sample.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff','samples')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    uploader = serializers.JSONField(False)

    class Meta:
        model = Sample
        fields = (
            'name',
            'description',
            'uploader',
            'uploadTime',
            'reviewedTime',
            'passTime',
            'reviewed',
            'reviewState',)


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    serializer_class = SampleSerializer


# Routers provide an easy way of automatically determining the URL conf.


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'samples', SampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
