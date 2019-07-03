from django.contrib.auth.models import User
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrSelf
from .serializers import UserSerializer


class Permission(IsAdminOrSelf):
    any_permission = ['retrieve']


class UserViewSet(
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
        GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (Permission, )
