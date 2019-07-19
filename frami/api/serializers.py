from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SlugRelatedField,
)

from .models import (
    Answer,
    Appointment,
    AppointmentRequest,
    Prescription,
    PrescriptionRequest,
    Question,
    Result,
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
