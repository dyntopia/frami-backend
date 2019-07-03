from pytest import fixture, mark
from rest_framework.test import APIClient


@fixture
def api():
    return APIClient()


@fixture
@mark.django_db
def regular_user(django_user_model, django_username_field):
    model = django_user_model
    field = django_username_field
    return _create_user(model, field, 'regular')


@fixture
@mark.django_db
def extra_users(django_user_model, django_username_field):
    model = django_user_model
    field = django_username_field
    return [_create_user(model, field, 'other-{}'.format(i)) for i in range(5)]


def _create_user(model, name_field, name):
    kwargs = {
        name_field: name,
        'email': '{}@example.invalid'.format(name),
        'password': 'password'
    }
    return model.objects.create_user(**kwargs)
