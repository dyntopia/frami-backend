# pylint: disable=W0621
from django.utils import timezone
from pytest import fixture
from rest_framework import status

url = '/api/appointment-request/'
url_pk = '/api/appointment-request/{pk}/'
url_creator = '/api/appointment-request/?creator={creator}'


@fixture
def requests(appointment_requests):
    return appointment_requests


def test_create(api, admin_user, regular_user):
    data = {
        'start_date': timezone.now().isoformat(),
        'end_date': timezone.now().isoformat(),
        'subject': 'abc',
        'message': 'xyz',
    }

    # Unauthenticated.
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED, res.data
    assert res.data['subject'] == data['subject']
    assert res.data['message'] == data['message']
    assert res.data['creator'] == regular_user.username

    # Staff.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data


def test_destroy(api, admin_user, regular_user, extra_users, requests):
    # Unauthenticated.
    res = api.delete(url_pk.format(pk=requests[regular_user][0].pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Regular can destroy own.
    assert api.login(username=regular_user.username, password='password')
    res = api.delete(url_pk.format(pk=requests[regular_user][0].pk))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Regular cannot destroy others.
    assert api.login(username=regular_user.username, password='password')
    res = api.delete(url_pk.format(pk=requests[extra_users[0]][0].pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Staff can destroy any.
    assert api.login(username=admin_user.username, password='password')
    res = api.delete(url_pk.format(pk=requests[regular_user][1].pk))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_list(api, admin_user, regular_user, extra_users, requests):
    # Unauthenticated.
    res = api.get(url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can list own requests.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(requests[regular_user])
    for i, r in enumerate(requests[regular_user]):
        assert res.data[i]['creator'] == r.creator.username

    # Regular user get nothing when filtering on others appointments.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url_creator.format(creator=extra_users[0].pk))
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data

    # Staff can list all.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(r) for r in requests.values()])

    # Staff can filter.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url_creator.format(creator=regular_user.pk))
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(requests[regular_user])


def test_retrieve(api, admin_user, regular_user, extra_users, requests):
    # Unauthenticated.
    res = api.get(url_pk.format(pk=requests[regular_user][0].pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Users can retrieve their own requests.
    assert api.login(username=regular_user.username, password='password')
    for r in requests[regular_user]:
        res = api.get(url_pk.format(pk=r.id))
        assert res.status_code == status.HTTP_200_OK, res.data
        assert res.data['creator'] == 'regular'

    # Users can not retrieve other users requests.
    for user in extra_users:
        for r in requests[user]:
            res = api.get(url_pk.format(pk=r.id))
            assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Staff can retrieve any request.
    assert api.login(username=admin_user.username, password='password')
    for user, rs in requests.items():
        for r in rs:
            res = api.get(url_pk.format(pk=r.pk))
            assert res.status_code == status.HTTP_200_OK, res.data
            assert res.data['creator'] == user.username
