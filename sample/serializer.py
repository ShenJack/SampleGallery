import django_filters
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import permissions, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.fields import ReadOnlyField
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.relations import StringRelatedField
from rest_framework.response import Response

from sample.models import Sample, IMG, update, User


class ImgSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    path = serializers.ReadOnlyField()

    class Meta:
        model = IMG
        fields = (
            'id',
            'path',
        )


class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'icon', 'name', 'groups')


class SampleSerializer(serializers.ModelSerializer):
    uploader = CommonUserSerializer(many=False)
    pics = ImgSerializer(many=True)

    class Meta:
        model = Sample
        fields = (
            'id',
            'name',
            'description',
            'uploader',
            'reviewed',
            'reviewState',
            'pics'
        )

    def create(self, validated_data):
        pics = validated_data.pop('pics')
        sample = Sample.objects.create(**validated_data)
        for pic in pics:
            img = IMG.objects.get(id=pic['id'])
            img.sample = sample
            img.save()
        sample.uploader = self._context['request'].user
        sample.save()
        return sample

    def update(self, instance, validated_data):
        pics = validated_data.pop('pics')
        instance.pics.all().update(sample=Sample.objects.get(id=1))
        for pic in pics:
            img = IMG.objects.get(id=pic['id'])
            instance.pics.add(img)
        instance.update(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    samples = SampleSerializer(many=True, read_only=True)
    groups = serializers.StringRelatedField(many=True, read_only=True)
    is_staff = serializers.StringRelatedField(many=False, read_only=True)
    id = serializers.ReadOnlyField()
    icon = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'icon', 'username', 'email', 'is_staff', 'name', 'samples', 'password', 'groups', 'first_name')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.groups.add(Group.objects.get(id=2))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance


# class CreateUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ('username', 'email','password')
#
#     def create(self, validated_data):
#         user = super(CreateUserSerializer, self).create(validated_data)
#         user.set_password(validated_data['password'])
#         user.groups.add(Group.objects.get(id=2))
#         user.save()
#         return user

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        update(instance, **validated_data)
        return instance
