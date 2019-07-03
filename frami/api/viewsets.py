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
from rest_framework.viewsets import GenericViewSet

from .models import Prescription
from .permissions import IsAdminOrSelf
from .serializers import PrescriptionSerializer, UserSerializer


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


class PrescriptionViewSet(
        CreateModelMixin,
        DestroyModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericViewSet,
):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = (Permission, )

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
