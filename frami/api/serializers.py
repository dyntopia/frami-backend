from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    RelatedField,
    SlugRelatedField,
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


class AppointmentSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    staff = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(groups__name='admin'),
    )
    patient = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentRequestSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    staff = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(groups__name='admin'),
        required=False,
    )

    class Meta:
        model = AppointmentRequest
        fields = '__all__'


class PrescriptionSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )
    refill_request = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'


class PrescriptionRequestSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )

    class Meta:
        model = PrescriptionRequest
        fields = '__all__'


class AnswerSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Question
        fields = '__all__'


class ResultSerializer(ModelSerializer):
    creator = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )

    class Meta:
        model = Result
        fields = '__all__'


class UserSerializer(ModelSerializer):
    groups = SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Group.objects.all(),
    )
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'groups',
            'prescriptions',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return make_password(value)


class GenericFieldSerializer(RelatedField):  # pylint: disable=W0223
    serializers = [
        AppointmentSerializer,
        AppointmentRequestSerializer,
        PrescriptionSerializer,
        PrescriptionRequestSerializer,
        QuestionSerializer,
        AnswerSerializer,
        ResultSerializer,
    ]

    def to_representation(self, value):
        for serializer in self.serializers:
            if isinstance(value, serializer.Meta.model):
                return serializer(value).data
        raise Exception('Could not find model')


class UserNotificationSerializer(ModelSerializer):
    target = GenericFieldSerializer(read_only=True)
    user = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = UserNotification
        fields = (
            'uuid',
            'target',
            'target_name',
            'creation_date',
            'user',
            'event',
            'read',
        )
        read_only_fields = (
            'uuid',
            'target',
            'target_name',
            'creation_date',
            'user',
            'event',
        )


class GroupNotificationSerializer(ModelSerializer):
    target = GenericFieldSerializer(read_only=True)
    group = SlugRelatedField(slug_field='name', queryset=Group.objects.all())

    class Meta:
        model = GroupNotification
        fields = (
            'uuid',
            'target',
            'target_name',
            'creation_date',
            'group',
            'event',
            'read',
        )
        read_only_fields = (
            'uuid',
            'target',
            'target_name',
            'creation_date',
            'group',
            'event',
        )
