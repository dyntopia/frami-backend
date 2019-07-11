from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from .generics import BaseViewSet
from .models import Answer, Prescription, Question
from .serializers import (
    AnswerSerializer,
    PrescriptionSerializer,
    QuestionSerializer,
    UserSerializer,
)


class UserViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    owner_field = 'pk'


class PrescriptionViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

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


class AnswerViewSet(CreateModelMixin, BaseViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

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


class QuestionViewSet(
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        BaseViewSet,
):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

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
