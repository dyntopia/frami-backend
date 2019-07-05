from rest_framework.routers import DefaultRouter

from .viewsets import PrescriptionViewSet, QuestionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'prescription', PrescriptionViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls
