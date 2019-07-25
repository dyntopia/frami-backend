from operator import attrgetter
from uuid import uuid4

from django.contrib.auth.models import Group
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    Answer,
    Appointment,
    AppointmentRequest,
    GroupNotification,
    Notification,
    Prescription,
    PrescriptionRequest,
    Question,
    Result,
    UserNotification,
)


def notification(signal, sender, users=None, groups=None):
    """
    Register notifications.

    :param signal: Signal to act on.
    :param sender: Model to register notifications for.
    :param users: A list of users on the receiver instance to assign a
        UserNotification.
    :param groups: A list of groups to assign a GroupNotification.
    :returns: Notification function.
    """
    dispatch_uid = sender._meta.model_name  # pylint: disable=W0212

    @receiver(signal, sender=sender, dispatch_uid=dispatch_uid)
    def fun(instance, **kwargs):
        uuid = uuid4()
        for user in users or []:
            user = attrgetter(user)(instance)
            if user:
                UserNotification.objects.create(
                    uuid=uuid,
                    user=user,
                    target=instance,
                    target_name=_get_sender_name(sender),
                    event=_get_signal_name(signal, kwargs.get('created')),
                )
        for group in groups or []:
            group = Group.objects.get(name=group)
            GroupNotification.objects.create(
                uuid=uuid,
                group=group,
                target=instance,
                target_name=_get_sender_name(sender),
                event=_get_signal_name(signal, kwargs.get('created')),
            )

    return fun


def _get_sender_name(sender):
    return sender._meta.model_name  # pylint: disable=W0212


def _get_signal_name(signal, created=False):
    if signal == post_save:
        return Notification.CREATED if created else Notification.CHANGED
    if signal == post_delete:
        return Notification.DELETED
    raise Exception('unknown signal')


answer = notification(
    signal=post_save,
    sender=Answer,
    users=['question.creator'],
)

appointment = notification(
    signal=post_save,
    sender=Appointment,
    users=['patient', 'staff'],
)

appointment_request = notification(
    signal=post_save,
    sender=AppointmentRequest,
    users=['staff'],
    groups=['admin'],
)

prescription = notification(
    signal=post_save,
    sender=Prescription,
    users=['patient'],
)

prescription_request = notification(
    signal=post_save,
    sender=PrescriptionRequest,
    users=['prescription.creator'],
    groups=['admin'],
)

question = notification(
    signal=post_save,
    sender=Question,
    groups=['admin'],
)

result = notification(
    signal=post_save,
    sender=Result,
    users=['patient'],
)
