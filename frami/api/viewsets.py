from django.contrib.auth.models import User

from .generics import BaseViewSet
from .mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from .models import (
    Answer,
    Appointment,
    AppointmentRequest,
    GroupNotification,
    Prescription,
    PrescriptionRequest,
    Question,
    Result,
    UserNotification,
)
from .serializers import (
    AnswerSerializer,
    AppointmentRequestSerializer,
    AppointmentSerializer,
    GroupNotificationSerializer,
    PrescriptionRequestSerializer,
    PrescriptionSerializer,
    QuestionSerializer,
    ResultSerializer,
    UserNotificationSerializer,
    UserSerializer,
)


class AppointmentViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_field = 'patient'


class AppointmentRequestViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        BaseViewSet,
):
    queryset = AppointmentRequest.objects.all()
    serializer_class = AppointmentRequestSerializer


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
    filter_field = 'patient'


class PrescriptionRequestViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        BaseViewSet,
):
    queryset = PrescriptionRequest.objects.all()
    serializer_class = PrescriptionRequestSerializer


class AnswerViewSet(CreateModelMixin, BaseViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionViewSet(
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        BaseViewSet,
):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResultViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_field = 'patient'


class UserNotificationViewSet(
        ListModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    filter_field = 'user'
    admin_groups = []


class GroupNotificationViewSet(
        ListModelMixin,
        UpdateModelMixin,
        BaseViewSet,
):
    queryset = GroupNotification.objects.all()
    serializer_class = GroupNotificationSerializer
    filter_field = 'group__name__in'
    filter_value = 'user.groups.all'
    admin_groups = []
