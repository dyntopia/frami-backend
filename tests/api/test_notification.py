from uuid import uuid4

from django.utils import timezone
from rest_framework import status

from frami.api.models import GroupNotification, Result, UserNotification
from frami.api.serializers import (
    GroupNotificationSerializer,
    UserNotificationSerializer,
)

user_url = '/api/user-notification/'
user_url_pk = '/api/user-notification/{pk}/'

group_url = '/api/group-notification/'
group_url_pk = '/api/group-notification/{pk}/'


def test_user_list_own_group_notification(api, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    GroupNotification.objects.create(
        group=regular_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == 1


def test_user_list_other_group_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    GroupNotification.objects.create(
        group=admin_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data


def test_admin_list_own_group_notification(api, admin_user):
    r = Result.objects.create(patient=admin_user, creator=admin_user)
    GroupNotification.objects.create(
        group=admin_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == 1


def test_admin_list_other_group_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    GroupNotification.objects.create(
        group=regular_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data


def test_user_list_own_user_notification(api, regular_user, extra_users):
    r = Result.objects.create(patient=extra_users[0], creator=extra_users[0])
    UserNotification.objects.create(
        user=regular_user,
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == 1


def test_user_list_other_user_notification(api, regular_user, extra_users):
    r = Result.objects.create(patient=extra_users[0], creator=extra_users[0])
    UserNotification.objects.create(
        user=extra_users[0],
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data


def test_admin_list_own_user_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    UserNotification.objects.create(
        user=admin_user,
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == 1


def test_admin_list_other_user_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    UserNotification.objects.create(
        user=regular_user,
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data


def test_user_update_own_group_notification(api, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = GroupNotification.objects.create(
        group=regular_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=n.pk), {'read': True})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data


def test_user_update_other_group_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = GroupNotification.objects.create(
        group=admin_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=n.pk), {'read': True})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data


def test_admin_update_own_group_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = GroupNotification.objects.create(
        group=admin_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )
    n_data = GroupNotificationSerializer(n).data
    data = {
        'read': True,
        'uuid': uuid4(),
        'target': 'asdf',
        'target_name': 'm00',
        'creation_date': timezone.now(),
        'event': 'deleted',
    }

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=n.pk), data)
    assert res.status_code == status.HTTP_200_OK

    # Can only update 'read'.
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in n_data.items() if k != 'read'}
    assert got == want


def test_admin_update_other_group_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = GroupNotification.objects.create(
        group=regular_user.groups.first(),
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=n.pk), {'read': True})
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_user_update_own_user_notification(api, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = UserNotification.objects.create(
        user=regular_user,
        uuid=uuid4(),
        target=r,
    )
    n_data = UserNotificationSerializer(n).data
    data = {
        'read': True,
        'uuid': uuid4(),
        'target': 'asdf',
        'target_name': 'm00',
        'creation_date': timezone.now(),
        'event': 'deleted',
    }

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=n.pk), data)
    assert res.status_code == status.HTTP_200_OK, res.data

    # Can only update 'read'.
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in n_data.items() if k != 'read'}
    assert got == want


def test_user_update_other_user_notification(api, regular_user, extra_users):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = UserNotification.objects.create(
        user=extra_users[0],
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=n.pk), {'read': True})
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_admin_update_own_user_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = UserNotification.objects.create(
        user=admin_user,
        uuid=uuid4(),
        target=r,
    )
    n_data = UserNotificationSerializer(n).data
    data = {
        'read': True,
        'uuid': uuid4(),
        'target': 'asdf',
        'target_name': 'm00',
        'creation_date': timezone.now(),
        'event': 'deleted',
    }

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=n.pk), data)
    assert res.status_code == status.HTTP_200_OK, res.data

    # Can only update 'read'.
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in n_data.items() if k != 'read'}
    assert got == want


def test_admin_update_other_user_notification(api, admin_user, regular_user):
    r = Result.objects.create(patient=regular_user, creator=regular_user)
    n = UserNotification.objects.create(
        user=regular_user,
        uuid=uuid4(),
        target=r,
    )

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=n.pk), {'read': True})
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_list_appointment_request(
        api,
        admin_user,
        regular_user,
        extra_users,
        appointment_requests,
):
    requests = appointment_requests

    # Unauthenticated.
    res = api.get(user_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    res = api.get(group_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Users cannot list any AppointmentRequest notifications.
    for user in [regular_user] + extra_users:
        assert api.login(username=user.username, password='password')
        res = api.get(user_url)
        assert res.status_code == status.HTTP_200_OK, res.data
        assert not res.data

        res = api.get(group_url)
        assert res.status_code == status.HTTP_200_OK, res.data
        assert not res.data

    # Admin can see all user notifications.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(x) for x in requests.values()])

    # Admin can see all group notifications.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(x) for x in requests.values()])


def test_update_appointment_request(
        api,
        admin_user,
        regular_user,
        appointment_requests,
):
    data = {
        'read': True,
        'uuid': uuid4(),
        'target': 'asdf',
        'target_name': 'm00',
        'creation_date': timezone.now(),
        'event': 'deleted',
    }

    request = appointment_requests[regular_user][0]
    un = UserNotification.objects.get(target_id=request.pk)
    gn = GroupNotification.objects.get(target_id=request.pk)

    # Unauthenticated.
    res = api.patch(user_url_pk.format(pk=un.pk), data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    res = api.patch(group_url_pk.format(pk=gn.pk), data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # User are not privy to AppointmentRequest notifications.
    assert api.login(username=regular_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=un.pk), data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=gn.pk), data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin can only update 'read' for user notifications.
    request = appointment_requests[regular_user][1]
    un = UserNotification.objects.get(target_id=request.pk)
    un_data = UserNotificationSerializer(un).data
    gn = GroupNotification.objects.get(target_id=request.pk)
    gn_data = GroupNotificationSerializer(gn).data

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=un.pk), data)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in un_data.items() if k != 'read'}
    assert got == want

    # Admin can only update 'read' for group notifications.
    request = appointment_requests[regular_user][2]
    un = UserNotification.objects.get(target_id=request.pk)
    un_data = UserNotificationSerializer(un).data
    gn = GroupNotification.objects.get(target_id=request.pk)
    gn_data = GroupNotificationSerializer(gn).data

    assert api.login(username=admin_user.username, password='password')
    res = api.patch(group_url_pk.format(pk=gn.pk), data)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in gn_data.items() if k != 'read'}
    assert got == want


def test_list_result(api, admin_user, regular_user, results):
    # Unauthenticated.
    res = api.get(user_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    res = api.get(group_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Users can see their own notifications.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(results[regular_user])
    for x in res.data:
        assert x['user'] == regular_user.username

    # Users cannot see group notifications.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data

    # Admin cannot see user notifications.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(user_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data

    # Admin cannot see group notifications.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(group_url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert not res.data


def test_update_result(api, regular_user, extra_users, results):
    data = {
        'read': True,
        'uuid': uuid4(),
        'target': 'asdf',
        'target_name': 'm00',
        'creation_date': timezone.now(),
        'event': 'deleted',
    }

    # Users can only update 'read' for their notifications.
    result = results[regular_user][0]
    n = UserNotification.objects.get(target_id=result.pk)
    n_data = UserNotificationSerializer(n).data

    assert api.login(username=regular_user.username, password='password')
    res = api.patch(user_url_pk.format(pk=result.pk), data)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert res.data['read'] is True
    got = {k: v for k, v in res.data.items() if k != 'read'}
    want = {k: v for k, v in n_data.items() if k != 'read'}
    assert got == want

    # Users cannot update other users notifications
    for user in extra_users:
        for result in results[user]:
            n = UserNotification.objects.get(target_id=result.pk)
            assert api.login(
                username=regular_user.username,
                password='password',
            )
            res = api.patch(user_url_pk.format(pk=result.pk), data)
            assert res.status_code == status.HTTP_403_FORBIDDEN, res.data
