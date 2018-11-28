from django.contrib.auth.models import User
from rest_framework import permissions, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sample.models import Sample
from sample.permissions import IsOwnerOrReadOnly


class SampleSerializer(serializers.ModelSerializer):
    uploader = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

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


class UserSerializer(serializers.ModelSerializer):
    samples = SampleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'samples')


# ViewSets define the view behavior.
class PasswordSerializer(serializers.Serializer):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'currentUser':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def listUser(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def currentUser(self,request,pk=None):


    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user,context={'request':request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)