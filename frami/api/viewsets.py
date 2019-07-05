from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Answer, Prescription, Question
from .permissions import IsAdminOrSelf
from .serializers import (
    AnswerSerializer,
    PrescriptionSerializer,
    QuestionSerializer,
    UserSerializer,
)


class Permission(IsAdminOrSelf):
    any_permission = ['retrieve']


class UserViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Permission, )


class PrescriptionViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericViewSet,
):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = (Permission, )

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'prescriber': request.user.username}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class AnswerViewSet(CreateModelMixin, GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminUser, )

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'user': request.user.username}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class QuestionViewSet(CreateModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *_args, **_kwargs):
        """
        Create an object.
        """
        data = {**request.data, 'user': request.user.username}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def list(self, request, *_args, **_kwargs):
        """
        List objects.

        Staff retrieves a complete list.  Regular users retrieve objects
        that they own.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *_args, **_kwargs):
        """
        Retrieve an object.

        Staff may retrieve any object.  Regular users are limited to
        objects that they own.
        """
        instance = self.get_object()
        if request.user.is_staff or request.user == instance.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        raise PermissionDenied()
