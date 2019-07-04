from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import status

from ..api.serializers import UserSerializer


class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data = UserSerializer(self.request.user).data
            context['user_serialized'] = data
        return context


class LoginView(BaseLoginView):
    def form_valid(self, form):
        user = form.get_user()
        data = UserSerializer(user).data
        login(self.request, user)
        return JsonResponse(data=data, status=status.HTTP_200_OK)

    def form_invalid(self, form):
        data = {'message': 'invalid credentials'}
        return JsonResponse(data=data, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(BaseLogoutView):
    pass
