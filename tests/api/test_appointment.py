# pylint: disable=W0621
from django.utils import timezone
from pytest import fixture, mark
from rest_framework import status

from frami.api.models import Appointment

url = '/api/appointment/'
url_pk = '/api/appointment/{pk}/'
url_patient = '/api/appointment/?patient={patient}'


@fixture
@mark.django_db
def appointments(admin_user, regular_user, extra_users):
    return {
        user: [
            Appointment.objects.create(
                patient=user,
                staff=admin_user,
                creator=admin_user,
                start_date=timezone.now(),
                end_date=timezone.now(),
            ) for i in range(3)
        ]
        for user in [regular_user] + extra_users
    }


def test_create(api, admin_user, regular_user):
    data = {
        'start_date': timezone.now().isoformat(),
        'end_date': timezone.now().isoformat(),
        'patient': regular_user.username,
        'staff': admin_user.username,
    }

    # Unauthenticated.
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Staff.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED, res.data
    assert res.data['patient'] == regular_user.username
    assert res.data['staff'] == admin_user.username


def test_destroy(api, admin_user, regular_user, appointments):
    target = url_pk.format(pk=appointments[regular_user][0].pk)

    # Unauthenticated.
    assert api.delete(target).status_code == status.HTTP_403_FORBIDDEN

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    assert api.delete(target).status_code == status.HTTP_403_FORBIDDEN

    # Staff.
    assert api.login(username=admin_user.username, password='password')
    assert api.delete(target).status_code == status.HTTP_204_NO_CONTENT
    assert api.get(target).status_code == status.HTTP_404_NOT_FOUND


def test_list(api, admin_user, regular_user, extra_users, appointments):
    # Unauthenticated.
    res = api.get(url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can list own appointments.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(appointments[regular_user])
    for i, a in enumerate(appointments[regular_user]):
        assert res.data[i]['patient'] == a.patient.username

    # Regular user get nothing when filtering on others appointments.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url_patient.format(patient=extra_users[0].pk))
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data

    # Staff can list all.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(a) for a in appointments.values()])

    # Staff can filter.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url_patient.format(patient=regular_user.pk))
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(appointments[regular_user])


def test_retrieve(api, admin_user, regular_user, extra_users, appointments):
    # Unauthenticated.
    res = api.get(url_pk.format(pk=appointments[regular_user][0].pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Users can retrieve their own appointments.
    assert api.login(username=regular_user.username, password='password')
    for a in appointments[regular_user]:
        res = api.get(url_pk.format(pk=a.id))
        assert res.status_code == status.HTTP_200_OK, res.data
        assert res.data['patient'] == 'regular'

    # Users can not retrieve other users appointments.
    for user in extra_users:
        for a in appointments[user]:
            res = api.get(url_pk.format(pk=a.id))
            assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Staff can retrieve any appointment.
    assert api.login(username=admin_user.username, password='password')
    for user, apts in appointments.items():
        for a in apts:
            res = api.get(url_pk.format(pk=a.pk))
            assert res.status_code == status.HTTP_200_OK, res.data
            assert res.data['patient'] == user.username
            assert res.data['creator'] == admin_user.username


def test_update(api, admin_user, regular_user, extra_users, appointments):
    appt = appointments[regular_user][0]
    target = url_pk.format(pk=appt.pk)

    extra_appt = appointments[extra_users[0]][0]
    extra_target = url_pk.format(pk=extra_appt.pk)

    # Unauthenticated.
    res = api.patch(target, {'note': 'abcd'})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Regular user can't update self.
    assert api.login(username=regular_user.username, password='password')
    res = api.patch(target, {'note': 'abcd'})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Regular user can't update others.
    assert api.login(username=regular_user.username, password='password')
    res = api.patch(extra_target, {'note': 'abcd'})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Admin can update any.
    assert api.login(username=admin_user.username, password='password')
    res = api.patch(target, {'note': 'abcd'})
    assert res.status_code == status.HTTP_200_OK
    assert res.data['note'] == 'abcd'
    assert res.data['patient'] == appt.patient.username
    assert res.data['staff'] == admin_user.username
    assert res.data['creator'] == admin_user.username
