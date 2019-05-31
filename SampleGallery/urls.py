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
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework import authtoken
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.urlpatterns import format_suffix_patterns

from SampleGallery import settings
from SampleGallery.auth import CustomAuthToken
from sample import views
from sample.views import upload_file

# 定义一个router
router = routers.DefaultRouter()

# router的以users开头的请求会由UserViewSet处理
router.register(r'users', views.UserViewSet)

router.register(r'samples', views.SampleViewSet)
router.register(r'borrows', views.LendViewset)

# 定义了url和其对应的处理函数，class形式的处理函数需要调用asview（）才行，这里相当于是处理一个请求的开始，需要根据其具体url来分发请求给具体的处理函数
urlpatterns = [
    path('samples/', views.SampleList.as_view()),
    path('borrows/', views.LendList.as_view()),

    # 这里的int：pk会作为sampledetail中函数调用时的一个参数
    path('samples/<int:pk>/', views.SampleDetail.as_view()),
    path('admin', admin.site.urls),
    path('login', CustomAuthToken.as_view()),
    path('image', upload_file),
    path('changePassword', views.ChangePasswordView.as_view()),

    # 下面三个没用到
    path('checkinCode/<int:pk>/', views.GetCheckinCode.as_view()),
    path('checkReceive/', views.VerifyCheckinCode.as_view()),
    path('checkPick/', views.VerifyPickCode.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

# 往上面的列表中加入router中规则
urlpatterns += path('', include(router.urls)),
