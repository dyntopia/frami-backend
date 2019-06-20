from rest_framework.permissions import IsAuthenticated


class IsAdminOrSelf(IsAuthenticated):
    """
    Allow actions for authenticated users.

    Actions in `any_permissions` are allowed for any authenticated user.
    Other actions require staff permission.

    Object-level permission require that the user operate on either
    their own objects or are staff.
    """
    any_permission = []

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and (request.user.is_staff or view.action in self.any_permission)
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            and (request.user == obj or request.user.is_staff)
        )
