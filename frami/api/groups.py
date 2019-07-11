from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

groups = {
    'admin': [
        # Answer
        'add_answer',

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
