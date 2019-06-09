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

from sample.models import Sample, IMG, update, User, Lend


# 序列化和反序列化Img
class ImgSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    path = serializers.ReadOnlyField()

    # 使用的Model是IMG，需要序列化的字段是 id，path
    class Meta:
        model = IMG
        fields = (
            'id',
            'path',
        )


# 普通User序列化器
class CommonUserSerializer(serializers.ModelSerializer):
    # 在子类设置要序列化的model和字段，具体序列化操作由父类的方法完成
    class Meta:
        model = User
        fields = ('id', 'icon', 'name', 'groups', 'email')


class SampleSerializer(serializers.ModelSerializer):
    # 这里嵌套了别的序列化器，需要额外声明 many：是否有多个uploader/pics
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
            'pics',
            'borrowable',
            'checkinStatus',
            'lendStatus',
            'isEntity',
            'bacteria',
            'medium'
        )

    # 自定义create 函数，这样就不会调用父类的create（数据到model）的函数
    def create(self, validated_data):
        # 从中取出并删除pics字段
        pics = validated_data.pop('pics')

        sample = Sample.objects.create(**validated_data)

        for pic in pics:
            img = IMG.objects.get(id=pic['id'])

            # 为每个pics设置外键sample
            img.sample = sample
            img.save()
        sample.uploader = self._context['request'].user
        sample.save()
        return sample

    # 自定义更新函数， instance为要更新的model
    def update(self, instance, validated_data):
        pics = validated_data.pop('pics')
        instance.pics.all().update(sample=Sample.objects.get(id=1))
        for pic in pics:
            img = IMG.objects.get(id=pic['id'])

            # 相当于把img的外键设置为instance
            instance.pics.add(img)
        instance.update(**validated_data)
        return instance


# 用来创建Sample的序列化器
class SampleCreateSerializer(serializers.ModelSerializer):
    pics = ImgSerializer(many=True)

    # 创建sample时的字段比较多
    class Meta:
        model = Sample
        fields = (
            'id',
            'name',
            'description',
            'reviewed',
            'reviewState',
            'pics',
            'isEntity',
            'bacteria',
            'medium'
        )

    # 同上
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

    # 同上
    def update(self, instance, validated_data):
        pics = validated_data.pop('pics')
        instance.pics.all().update(sample=Sample.objects.get(id=1))
        for pic in pics:
            img = IMG.objects.get(id=pic['id'])
            instance.pics.add(img)
        instance.update(**validated_data)
        return instance


# 用户序列化器
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
        # 调用setpassword来加密存储密码，防止明文存储
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

# 仅用来序列化修改密码时的数据
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# 编辑用户信息时的序列化器，因此只有update
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'icon')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        update(instance, **validated_data)
        return instance

#没有用到这个
class CheckinCodeSerializer(serializers.ModelSerializer):
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
            'checkinCode',
            'pics',
            'borrowable',
            'checkinStatus',
            'lendStatus',
            'isEntity',
            'bacteria',
            'medium'
        )

# 序列化借阅记录，有两个外键
class LendSerializer(serializers.ModelSerializer):
    from_user = CommonUserSerializer(many=False)
    to_sample = SampleSerializer(many=False)

    class Meta:
        model = Lend
        fields = (
            'id',
            'checkState',
            'lendState',
            'from_user',
            'to_sample',
            'createTime',
            'pickTime',
            'returnTime',
            'latestReturnTime',
            'latestPickTime',
            'code',
        )
