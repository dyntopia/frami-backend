from django.contrib.auth.models import User

from .generics import BaseViewSet
from .mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
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
    filter_field = 'id'


class PrescriptionViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    creator_field = 'prescriber'
    filter_field = 'user'


class AnswerViewSet(CreateModelMixin, BaseViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    creator_field = filter_field = 'user'


class QuestionViewSet(
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        BaseViewSet,
):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    creator_field = filter_field = 'user'
