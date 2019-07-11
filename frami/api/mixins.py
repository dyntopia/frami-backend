from rest_framework.mixins import CreateModelMixin as _CreateModelMixin
from rest_framework.mixins import DestroyModelMixin as _DestroyModelMixin
from rest_framework.mixins import ListModelMixin as _ListModelMixin
from rest_framework.mixins import RetrieveModelMixin as _RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin as _UpdateModelMixin
from rest_framework.response import Response


class CreateModelMixin(_CreateModelMixin):
    def create(self, request, *args, **kwargs):
        """
        Create an object with the authenticated user as creator.
        """
        serializer = self.get_serializer()
        creator = serializer.fields.get(getattr(self, 'creator_field', None))
        if creator and not creator.read_only:
            request.data[creator.field_name] = request.user
        return super().create(request, *args, **kwargs)


class DestroyModelMixin(_DestroyModelMixin):
    pass


class ListModelMixin(_ListModelMixin):
    def list(self, request, *args, **kwargs):
        """
        List a queryset and optionally filter on `filter_field`.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_name = getattr(self, 'filter_field', None)
        filter_value = request.query_params.get(filter_name)
        if filter_value:
            queryset = queryset.filter(**{filter_name: filter_value})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(_RetrieveModelMixin):
    pass


class UpdateModelMixin(_UpdateModelMixin):
    pass
