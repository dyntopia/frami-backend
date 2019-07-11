from rest_framework.permissions import DjangoModelPermissions


class ModelAndObjectPermission(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return (
            super().has_object_permission(request, view, obj)
            and request.user.has_perms(perms)
        )
