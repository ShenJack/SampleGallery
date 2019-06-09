import datetime

import django_filters
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
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


# viewset可以直接在urls里面注册，详细看urls.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)

    # 这个方法用来处理 url结尾是currentUser的请求，同时method是get的请求，用以获取当前用户信息
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def currentUser(self, request):
        serializer = UserSerializer(request.user, context={'request': request})

        # 用序列化器序列化好的数据来新建Response并返回给前端
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        user = User.objects.get(pk=pk)
        serializer = UserEditSerializer(user, data=request.data)

        # serializer 还提供了数据校验功能，但是这个系统没有具体设置，调用is——valid可以校验数据
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 用来处理： 获取所有sample和创建新的sample
class SampleList(ListAPIView):
    """
    List all snippets, or create a new snippet.
    """

    # 定义用于筛选（查询）的类
    filter_backends = (DjangoFilterBackend,)

    serializer_class = SampleSerializer

    # 默认查询集，但是好像没用到
    queryset = Sample.objects.all()

    # 自己定义的可以用来筛选的字段
    filter_keys = ['name', 'description', 'reviewState', "checkinStatus", 'lendStatus', 'reviewed']

    def get(self, request, format=None, **kwargs):

        if isManager(request.user):
            queryset = Sample.objects.all()

            # 遍历请求的查询参数
            for param in request.query_params:
                if param in self.filter_keys:
                    param_value = self.request.query_params.get(param, None)
                    # 每个参数都用来筛选一次 getTrueFalse：用来转换js的true/false 为 python的true/false
                    queryset = queryset.filter(**{param: getTrueFalse(param_value)})

            userId = self.request.query_params.get('uploader', None)

            # 如果有userId参数，就再用userId筛选一次
            if userId is not None:
                queryset = queryset.filter(uploader=User.objects.get(id=userId))

            # 如果有chechInCode就只用它来筛选，用于在入库管理里面通过验证码查询样本入库
            if "checkInCode" in request.query_params:
                queryset = Sample.objects.filter(checkinCode=request.query_params['checkInCode'])

        # 前端有一个接口，如果有personal参数就返回他自己的sample，（我的上传界面）
        elif "personal" in request.query_params and request.query_params['personal']:
            queryset = Sample.objects.filter(uploader=request.user)
        else:
            queryset = Sample.objects.filter(reviewed=True, reviewState=Sample.STATE_PASSED)

        # 构建筛选字典，由于js的truefalse格式和python不一样，这里转换一下（js开头小写，python开头大写）
        querydict = {}
        for i in request.query_params:
            if i in self.filter_keys:
                if request.query_params[i] == 'true':
                    querydict[i] = True
                elif request.query_params[i] == 'false':
                    querydict[i] = False
                else:
                    querydict[i] = request.query_params[i]

        queryset = queryset.filter(**querydict)

        # 不包括id是1的sample，因为这个sample里面有很多默认的图片（bug）（图片的默认外键是id为1的sample
        queryset = queryset.filter(~Q(id=1))

        # 使用上面定义的序列化器，这里应该是SampleSerializer
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 新建sample调用SampleCreateSerializer
    def post(self, request, format=None):
        serializer = SampleCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 对具体Sample的操作，获取详细信息或者修改信息或者删除
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

        # 调用Serializer时如果传了已有的sample进去，就会调用序列化器的update函数而不是create函数
        serializer = SampleCreateSerializer(sample, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sample = self.get_object(pk)
        sample.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 处理url形式是 lend/id/pck 和 lend/id/finish 的请求，用以领取和归还标本
class LendViewset(viewsets.ModelViewSet):
    queryset = Lend.objects.all()
    serializer_class = LendSerializer
    filter_backends = (DjangoFilterBackend,)

    @action(detail=True, methods=['get'])
    def pick(self, request, pk):
        try:
            lend = Lend.objects.get(pk=pk)
            lend.pickTime = timezone.now()
            sample = lend.to_sample
            sample.lendStatus = sample.STATE_LENT
            sample.save()
            lend.lendState = Lend.STATE_LENT
            lend.save()
            serializer = LendSerializer(lend, context={'request': request})
            return Response(serializer.data)
        except Lend.DoesNotExist as e:
            # 如果碰到Lend不存的错误就返回404错误
            raise Http404()

    @action(detail=True, methods=['get'])
    def finish(self, request, pk):
        try:
            lend = Lend.objects.get(pk=pk)
            lend.pickTime = timezone.now()
            sample = lend.to_sample
            sample.lendStatus = sample.STATE_AVAILABLE
            sample.save()
            lend.lendState = Lend.STATE_RETURNED
            lend.save()
            serializer = LendSerializer(lend, context={'request': request})
            return Response(serializer.data)
        except Lend.DoesNotExist as e:
            raise Http404()

    @action(detail=True, methods=['get'])
    def passLend(self, request, pk):
        try:
            lend = Lend.objects.get(pk=pk)
            lend.checkState = Lend.STATE_PASSED

            sample = lend.to_sample
            sample.lendStatus = Sample.STATE_WAIT
            sample.save()

            lend.save()

            # 拒绝所有别的Lend
            Lend.objects.filter(to_sample=sample).filter(~Q(id=lend.id)).update(checkState=Lend.STATE_REJECTED)

            serializer = LendSerializer(lend, context={'request': request})
            return Response(serializer.data)
        except Lend.DoesNotExist as e:
            raise Http404()

    @action(detail=True, methods=['get'])
    def rejectLend(self, request, pk):
        try:
            lend = Lend.objects.get(pk=pk)
            lend.checkState = Lend.STATE_REJECTED
            lend.save()
            serializer = LendSerializer(lend, context={'request': request})
            return Response(serializer.data)
        except Lend.DoesNotExist as e:
            raise Http404()


# 用以返回所有的Lend和通过pickCode查询具体的一个lend
class LendList(ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    serializer_class = LendSerializer

    def get(self, request, format=None, **kwargs):
        queryset = None
        if isManager(request.user):
            if "pickCode" in request.query_params:
                queryset = Lend.objects.filter(code=request.query_params['pickCode']).order_by('-createTime')
                if len(queryset) > 0:
                    queryset = [queryset[0]]
            else:
                queryset = getManagerLends()
        else:
            if "pickCode" in request.query_params:
                queryset = Lend.objects.filter(code=request.query_params['pickCode'], from_user=request.user).order_by(
                    '-createTime')
                if len(queryset) > 0:
                    queryset = [queryset[0]]
            else:
                # 所有可以借的Sample
                queryset = Sample.objects.all().filter(~Q(lendStatus=Sample.STATE_UNAVAILABLE))
                queryset = getLend(queryset, request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def getLend(queryset, user):
    result = []
    # 对每个sample
    for i in queryset:
        # 如果他和当前用户存在借阅记录
        if len(i.lend.all().filter(from_user=user).filter(~Q(lendState=Lend.STATE_RETURNED))) > 0:
            # 就返回最新的那个
            result.append(i.lend.all().filter(from_user=user).filter(~Q(lendState=Lend.STATE_RETURNED)).order_by('-createTime')[0])

    return result


def getManagerLends():
    result = []

    # 所有未归还的 和 未被拒绝的 Lend
    return Lend.objects.all().filter(~Q(lendState=Lend.STATE_RETURNED)).filter(
        ~Q(checkState=Lend.STATE_REJECTED)).order_by('-createTime')


# 对特定sample的具体操作
class SampleViewSet(viewsets.ViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    filter_backends = (DjangoFilterBackend,)

    # 审核通过
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

    # 审核不通过
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

    # 借阅
    @action(detail=True, methods=['get'])
    def borrow(self, request, pk=1):
        try:
            sample = Sample.objects.get(pk=pk)
            sample.save()

            # django会自动把user对象放到request中

            lend, created = Lend.objects.get_or_create(to_sample=sample, from_user=request.user)
            if created:
                lend.init()
            lend.checkState = Lend.STATE_NEED_REVIEW
            lend.save()
            serializer = LendSerializer(lend)
            return Response(serializer.data)
        except Sample.DoesNotExist as e:
            raise Http404

    # 接收
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

    # 没用到
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


# 上传图片
def upload_file(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get("file", ),
        )
        new_img.save()
        return JsonResponse({"path": '/' + new_img.img.name, "id": new_img.id})
    else:
        return HttpResponse('Not a post!')


# 处理函数：用来修改密码
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

    # 处理put请求
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 检查旧密码
            if not self.object.check_password(serializer.data.get("old_password", )):
                return Response({"detail": "密码错误"}, status=status.HTTP_400_BAD_REQUEST)
            # 设置新密码
            self.object.set_password(serializer.data.get("new_password", ))
            self.object.save()
            return Response({"detail": "修改成功"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 没用到
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


# 没用到
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


# 没用到
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


def getTrueFalse(str):
    if str == 'true':
        return True
    elif str == 'false':
        return False
    else:
        return str
