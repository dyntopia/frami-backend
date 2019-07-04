from django.urls import path, re_path

from .views import IndexView, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='index.html')),
    path('logout/', LogoutView.as_view(template_name='index.html')),
    re_path(r'', IndexView.as_view(template_name='index.html')),
]
