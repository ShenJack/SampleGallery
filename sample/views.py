import datetime

import django_filters
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sample.models import Sample, IMG, User, Lend
from sample.serializer import UserSerializer, SampleSerializer, ChangePasswordSerializer, UserEditSerializer, \
    SampleCreateSerializer, CheckinCodeSerializer, LendSerializer

# class UserList(generics.ListAPIView):
from sample.utils import encryption, isManager


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def currentUser(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        user = User.objects.get(pk=pk)
        serializer = UserEditSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SampleList(ListAPIView):
    """
    List all snippets, or create a new snippet.
    """

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'description', 'reviewed', 'uploader')
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()

    def get(self, request, format=None, **kwargs):
        if isManager(request.user):
            queryset = Sample.objects.all()
            if "checkInCode" in request.query_params:
                queryset = Sample.objects.filter(checkinCode=request.query_params['checkInCode'])
        elif "personal" in request.query_params and request.query_params['personal']:
            queryset = Sample.objects.filter(uploader=request.user)
        else:
            queryset = Sample.objects.filter(reviewed=True, reviewState=Sample.STATE_PASSED)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = SampleCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SampleDetail(RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a sample instance.
    """

    serializer_class = SampleSerializer

    def get_object(self, pk):
        try:
            return Sample.objects.get(pk=pk)
        except Sample.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sample = self.get_object(pk)
        serializer = SampleSerializer(sample)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sample = self.get_object(pk)
        serializer = SampleCreateSerializer(sample, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sample = self.get_object(pk)
        sample.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LendViewset(viewsets.ModelViewSet):
    queryset = Lend.objects.all()
    serializer_class = LendSerializer
    filter_backends = (DjangoFilterBackend,)

    def pick(self, request, pk):
        try:
            lend = Lend.objects.get(pk=pk)
            lend.pickTime = timezone.now()
            sample = lend.to_sample
            sample.lendStatus = sample.STATE_LENT
            sample.save()
            lend.save()
        except Lend.DoesNotExist as e:
            raise Http404()


class SampleViewSet(viewsets.ViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = (DjangoFilterBackend,)

    @action(detail=True, methods=['get'])
    def passed(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            sample.reviewed = True
            sample.reviewState = Sample.STATE_PASSED
            sample.save()
            serializer = SampleSerializer(sample, context={'request': request})
            return Response(serializer.data)
        except Sample.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def reject(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            sample.reviewed = True
            sample.reviewState = Sample.STATE_REJECTED
            sample.save()
            serializer = SampleSerializer(sample, context={'request': request})
            return Response(serializer.data)
        except Sample.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def borrow(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            lend = Lend.objects.create(to_sample=sample, from_user=request.user)
            lend.init()
            lend.save()
            serializer = LendSerializer(lend)
            return Response(serializer.data)
        except Sample.DoesNotExist as e:
            raise Http404

    @action(detail=True, methods=['get'])
    def checkReceiveCode(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            sample.checkinStatus = Sample.STATE_IN_STORAGE
            sample.lendStatus = Sample.STATE_AVAILABLE
            sample.save()
            return Response(SampleSerializer(sample).data)
        except Sample.DoesNotExist as e:
            raise Http404

    @action(detail=True, methods=['get'])
    def dismissReceive(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            sample.checkinStatus = Sample.STATE_WAIT_APPLY
            sample.lendStatus = Sample.STATE_UNAVAILABLE
            sample.save()
            return Response(SampleSerializer(sample).data)
        except Sample.DoesNotExist as e:
            raise Http404


# class SampleViewSet(viewsets.GenericViewSet):


def upload_file(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get("file", ),
        )
        new_img.save()
        return JsonResponse({"path": '/' + new_img.img.name, "id": new_img.id})
    else:
        return HttpResponse('Not a post!')


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password", )):
                return Response({"detail": "密码错误"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password", ))
            self.object.save()
            return Response({"detail": "修改成功"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCheckinCode(RetrieveUpdateAPIView):

    def get_object(self, pk):
        try:
            return Sample.objects.get(pk=pk)
        except Sample.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sample = self.get_object(pk)
        if sample.checkinCode == "":
            sample.checkinCode = encryption(str(sample.id) + sample.name + str(sample.uploadTime))
            sample.save()
        serializer = CheckinCodeSerializer(sample)
        return Response(serializer.data)


class VerifyCheckinCode(APIView):

    def post(self, request, format=None):
        if 'code' in request.data:
            code = str.upper(request.data['code'])
            sample_queryset = Sample.objects.filter(checkinCode=code)
            if len(sample_queryset) > 0:
                sample = sample_queryset[0]
                sample.checkinStatus = Sample.STATE_IN_STORAGE
                sample.lendStatus = Sample.STATE_AVAILABLE
                sample.save()
                return Response(SampleSerializer(sample).data)
            else:
                raise Http404


class VerifyPickCode(APIView):
    def post(self, request, format=None):
        if 'code' in request.data:
            code = str.upper(request.data['code'])
            sample_queryset = Sample.objects.filter(checkinCode=code)
            if len(sample_queryset) > 0:
                sample = sample_queryset[0]
                sample.checkinStatus = Sample.STATE_IN_STORAGE
                sample.lendStatus = Sample.STATE_AVAILABLE
                sample.save()
                return Response(SampleSerializer(sample).data)
            else:
                raise Http404
