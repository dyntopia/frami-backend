from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

groups = {
    'admin': [
        # Answer
        'add_answer',

        # Appointment
        'add_appointment',
        'delete_appointment',
        'change_appointment',
        'view_appointment',

        # AppointmentRequest
        'delete_appointmentrequest',
        'view_appointmentrequest',

        # Prescription
        'add_prescription',
        'change_prescription',
        'delete_prescription',
        'view_prescription',

        # Question
        'view_question',

        # Result
        'add_result',
        'change_result',
        'delete_result',
        'view_result',

        # User
        'add_user',
        'change_user',
        'delete_user',

        # 'delete_user',
        'view_user',
    ],
    'patient': [
        # Appointment
        'view_appointment',

        # AppointmentRequest
        'add_appointmentrequest',
        'delete_appointmentrequest',
        'view_appointmentrequest',

        # Question
        'add_question',
        'view_question',

        # Result
        'view_result',

        # User
        'view_user',
    ],
}


class GroupError(Exception):
    pass


def create_groups():
    for group, permissions in groups.items():
        group_obj, _ = Group.objects.get_or_create(name=group)
        try:
            group_obj.permissions.set([
                Permission.objects.get(codename=perm) for perm in permissions
            ])
        except ObjectDoesNotExist as e:
            raise GroupError(e)
