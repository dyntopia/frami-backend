from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.http import JsonResponse
from rest_framework import status

from ..api.serializers import UserSerializer


class LoginView(BaseLoginView):
    def form_valid(self, form):
        user = form.get_user()
        data = UserSerializer(user).data
        login(self.request, user)
        return JsonResponse(data=data, status=status.HTTP_200_OK)

    def form_invalid(self, form):
        data = {'message': 'invalid credentials'}
        return JsonResponse(data=data, status=status.HTTP_401_UNAUTHORIZED)
