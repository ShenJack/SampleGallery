import datetime

import django_filters
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from sample.models import Sample, IMG
from sample.serializer import UserSerializer, SampleSerializer


# class UserList(generics.ListAPIView):


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def currentUser(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class SampleList(ListAPIView):
    """
    List all snippets, or create a new snippet.
    """

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'name', 'description')
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()

    # def get(self, request, format=None, **kwargs):
    #     samples = Sample.objects.all()
    #     serializer = SampleSerializer(samples, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SampleSerializer(data=request.data)
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
        serializer = SampleSerializer(sample, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sample = self.get_object(pk)
        sample.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SampleViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
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


# class SampleViewSet(viewsets.GenericViewSet):


def upload_file(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get("file"),
        )
        new_img.save()
        return JsonResponse({"path": '/' + new_img.img.name, "id": new_img.id})
    else:
        return HttpResponse('Not a post!')
