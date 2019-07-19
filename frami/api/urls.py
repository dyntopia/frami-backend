from rest_framework.routers import DefaultRouter

from .viewsets import (
    AnswerViewSet,
    AppointmentRequestViewSet,
    AppointmentViewSet,
    PrescriptionRequestViewSet,
    PrescriptionViewSet,
    QuestionViewSet,
    ResultViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'answer', AnswerViewSet)
router.register(r'appointment', AppointmentViewSet)
router.register(r'appointment-request', AppointmentRequestViewSet)
router.register(r'prescription', PrescriptionViewSet)
router.register(r'prescription-request', PrescriptionRequestViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'result', ResultViewSet)
router.register(r'user', UserViewSet)

urlpatterns = router.urls
