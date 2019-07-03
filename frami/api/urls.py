from rest_framework.routers import DefaultRouter

from .viewsets import PrescriptionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'prescription', PrescriptionViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls
