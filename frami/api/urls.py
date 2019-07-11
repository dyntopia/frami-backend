from rest_framework.routers import DefaultRouter

from .viewsets import (
    AnswerViewSet,
    PrescriptionViewSet,
    QuestionViewSet,
    ResultViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'answer', AnswerViewSet)
router.register(r'prescription', PrescriptionViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'result', ResultViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls
