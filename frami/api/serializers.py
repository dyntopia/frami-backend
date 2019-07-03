from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Prescription


class PrescriptionSerializer(ModelSerializer):
    prescriber = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(is_staff=True),
    )

    class Meta:
        model = Prescription
        fields = '__all__'


class UserSerializer(ModelSerializer):
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
            'prescriptions',
        )
        read_only_fields = ('id', )
