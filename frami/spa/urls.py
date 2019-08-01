from django.conf import settings
from django.urls import path, re_path

from .views import (
    IndexView,
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)

urlpatterns = []

email = [
    'EMAIL_HOST',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
]
if all([getattr(settings, x, False) for x in email]):
    urlpatterns = [
        path(
            'reset/request/',
            PasswordResetView.as_view(template_name='reset-request.html'),
            name='password_reset',
        ),
        path(
            'reset/request/done/',
            PasswordResetDoneView.as_view(
                template_name='reset-request-done.html',
            ),
            name='password_reset_done'
        ),
        path(
            'reset/confirm/<uidb64>/<token>/',
            PasswordResetConfirmView.as_view(
                template_name='reset-confirm.html'
            ),
            name='password_reset_confirm'
        ),
        path(
            'reset/confirm/done/',
            PasswordResetCompleteView.as_view(
                template_name='reset-confirm-done.html',
            ),
            name='password_reset_complete'
        ),
    ]

urlpatterns += [
    path('login/', LoginView.as_view(template_name='index.html')),
    path('logout/', LogoutView.as_view(template_name='index.html')),
    re_path(r'', IndexView.as_view(template_name='index.html')),
]
