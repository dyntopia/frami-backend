from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from .permissions import ModelAndObjectPermission


class BaseViewSet(GenericViewSet):
    creator_field = 'creator'
    filter_field = 'creator'
    admin_groups = ['admin']
    permission_classes = (ModelAndObjectPermission, )

    def is_admin(self, user):
        """
        Check if `user` is in `admin_groups`.
        """
        return any(user.groups.filter(name=g) for g in self.admin_groups)

    def get_queryset(self):
        """
        Retrieve a queryset.

        Users in `admin_groups` retrieves a complete queryset.  Other
        users are limited to objects that matches `filter_field`.
        """
        queryset = super().get_queryset()
        if self.is_admin(self.request.user):
            return queryset
        return queryset.filter(**{self.filter_field: self.request.user.pk})

    def get_object(self):
        """
        Retrieve an object.

        If the object doesn't exist, 404 is raised for users in
        `admin_groups` and 403 is raised for other users.
        """
        try:
            return super().get_object()
        except Http404 as e:
            if self.is_admin(self.request.user):
                raise e
            raise PermissionDenied()
