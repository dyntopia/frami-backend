from django.contrib.auth.models import User
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrSelf
from .serializers import UserSerializer


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
