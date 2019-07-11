from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Answer, Prescription, Question


class PrescriptionSerializer(ModelSerializer):
    prescriber = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )

    class Meta:
        model = Prescription
        fields = '__all__'


class AnswerSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(),
    )

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Question
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
