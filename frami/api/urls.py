from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = router.urls
