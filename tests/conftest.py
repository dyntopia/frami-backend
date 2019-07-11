# pylint: disable=W0621
from django.contrib.auth.models import Group
from pytest import fixture, mark
from rest_framework.test import APIClient

from frami.api.groups import create_groups


@fixture
def api():
    return APIClient()


@fixture
def admin_user(create_user):
    return create_user('adm', 'admin')


@fixture
def regular_user(create_user):
    return create_user('regular', 'patient')


@fixture
def extra_users(create_user):
    return [create_user('other-{}'.format(i), 'patient') for i in range(5)]


@fixture
@mark.django_db
def groups():
    create_groups()


@fixture
@mark.django_db
def create_user(django_user_model, django_username_field, groups):
    model = django_user_model
    field = django_username_field
    return lambda name, *groups: _create_user(model, field, name, *groups)


def _create_user(model, name_field, name, *groups):
    kwargs = {
        name_field: name,
        'email': '{}@example.invalid'.format(name),
        'password': 'password'
    }
    user = model.objects.create_user(**kwargs)
    user.groups.set([Group.objects.get(name=g) for g in groups])
    return user
