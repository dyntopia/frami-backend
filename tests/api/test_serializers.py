from uuid import uuid4

from pytest import raises
from rest_framework.serializers import ModelSerializer

from frami.api.models import Notification, Result
from frami.api.serializers import GenericFieldSerializer


class FieldSerializer(GenericFieldSerializer):  # pylint: disable=W0223
    serializers = []


class Serializer(ModelSerializer):
    target = FieldSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'


def test_generic_field(admin_user):
    r = Result.objects.create(creator=admin_user, patient=admin_user)
    n = Notification.objects.create(uuid=uuid4(), target=r)
    s = Serializer(n)

    with raises(Exception):
        s.data  # pylint: disable=W0104
