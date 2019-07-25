from django.db.models.signals import post_delete, post_save
from django.utils import timezone
from pytest import raises

from frami.api.models import (
    AppointmentRequest,
    GroupNotification,
    Notification,
    Result,
    UserNotification,
)
from frami.api.signals import _get_sender_name, _get_signal_name


def test_notification_maybe_no_user(admin_user, regular_user):
    AppointmentRequest.objects.create(
        creator=regular_user,
        start_date=timezone.now(),
        end_date=timezone.now(),
    )
    assert not UserNotification.objects.all()
    assert len(GroupNotification.objects.all()) == 1

    AppointmentRequest.objects.create(
        creator=regular_user,
        staff=admin_user,
        start_date=timezone.now(),
        end_date=timezone.now(),
    )
    assert len(UserNotification.objects.all()) == 1
    assert len(GroupNotification.objects.all()) == 2


def test_get_sender_name():
    assert _get_sender_name(Result) == 'result'


def test_get_signal_name():
    assert _get_signal_name(post_save, True) == Notification.CREATED
    assert _get_signal_name(post_save, False) == Notification.CHANGED
    assert _get_signal_name(post_delete) == Notification.DELETED

    with raises(Exception):
        _get_signal_name(None)
