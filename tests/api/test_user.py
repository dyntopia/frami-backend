from pytest import mark
from rest_framework import status


@mark.django_db
def test_unauthenticated(client, regular_user):
    assert client.get('/api/user/').status_code == status.HTTP_403_FORBIDDEN
    assert client.get('/api/user/{}/'.format(regular_user.id)).status_code == \
        status.HTTP_403_FORBIDDEN


@mark.django_db
def test_create(client, admin_user, regular_user):
    url = '/api/user/'

    # Forbidden.
    assert client.login(username=regular_user.username, password='password')
    res = client.post(url, {'username': 'abc', 'password': 'pwpwpw1234'})
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert not client.login(username='abc', password='pwpwpw1234')

    # Invalid group.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(
        url, {
            'username': 'abc',
            'password': 'pwpwpw1234',
            'groups': ['abcdefghijkl'],
        }
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'does_not_exist' in [err.code for err in res.data['groups']]
    assert not client.login(username='abc', password='pwpwpw1234')

    # New patient.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(
        url, {
            'username': 'abc',
            'password': 'pwpwpw1234',
            'groups': ['patient'],
        }
    )
    assert not res.data['is_staff']
    assert res.data['username'] == 'abc'
    assert res.data['groups'] == ['patient']
    assert res.status_code == status.HTTP_201_CREATED
    assert client.login(username='abc', password='pwpwpw1234')

    # New admin.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(
        url, {
            'username': 'xyz',
            'password': 'pwpwpw1234',
            'groups': ['admin'],
        }
    )
    assert not res.data['is_staff']
    assert res.data['username'] == 'xyz'
    assert res.data['groups'] == ['admin']
    assert res.status_code == status.HTTP_201_CREATED
    assert client.login(username='xyz', password='pwpwpw1234')

    # New admin and patient.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(
        url, {
            'username': 'xyz321',
            'password': 'pwpwpw1234',
            'groups': ['admin', 'patient'],
        }
    )
    assert not res.data['is_staff']
    assert res.data['username'] == 'xyz321'
    assert sorted(res.data['groups']) == ['admin', 'patient']
    assert res.status_code == status.HTTP_201_CREATED
    assert client.login(username='xyz321', password='pwpwpw1234')

    # Duplicate.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(url, {'username': 'abc', 'password': 'pwpwpw1234'})
    assert 'unique' in [err.code for err in res.data['username']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Missing password.
    assert client.login(username=admin_user.username, password='password')
    res = client.post(url, {'username': 'meh'})
    assert 'required' in [err.code for err in res.data['password']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Invalid password.
    assert client.login(username=admin_user, password='password')
    res = client.post(url, {'username': 'meh', 'password': 'x'})
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@mark.django_db
def test_destroy(client, admin_user, regular_user, extra_users):
    user_url = '/api/user/{}/'.format(regular_user.id)
    extra_url = '/api/user/{}/'.format(extra_users[0].id)
    admin_url = '/api/user/{}/'.format(admin_user.id)

    # User delete other.
    assert client.login(username=regular_user.username, password='password')
    assert client.delete(extra_url).status_code == status.HTTP_403_FORBIDDEN

    # User delete self.
    assert client.login(username=regular_user.username, password='password')
    assert client.delete(user_url).status_code == status.HTTP_403_FORBIDDEN

    # Admin delete other.
    assert client.login(username=admin_user.username, password='password')
    assert client.delete(extra_url).status_code == status.HTTP_204_NO_CONTENT
    assert client.get(extra_url).status_code == status.HTTP_404_NOT_FOUND

    # Admin delete self.
    assert client.login(username=admin_user.username, password='password')
    assert client.delete(admin_url).status_code == status.HTTP_204_NO_CONTENT
    assert client.get(admin_url).status_code == status.HTTP_403_FORBIDDEN


@mark.django_db
def test_list(client, admin_user, regular_user, extra_users):
    # Regular user list.
    assert client.login(username=regular_user.username, password='password')
    res = client.get('/api/user/')
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['id'] == regular_user.id
    assert res.data[0]['username'] == regular_user.username
    assert not res.data[0].get('password')

    # Admin user list.
    assert client.login(username=admin_user.username, password='password')
    res = client.get('/api/user/')
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == len(extra_users) + 2
    for i, user in enumerate([admin_user, regular_user] + extra_users):
        assert res.data[i]['id'] == user.id
        assert res.data[i]['username'] == user.username
        assert not res.data[i].get('password')


@mark.django_db
def test_retrieve(client, admin_user, regular_user):
    # User retrieve self.
    assert client.login(username=regular_user.username, password='password')
    res = client.get('/api/user/{}/'.format(regular_user.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == regular_user.id
    assert res.data['username'] == regular_user.username
    assert not res.data.get('password')

    # Admin retrieve self.
    assert client.login(username=admin_user.username, password='password')
    res = client.get('/api/user/{}/'.format(admin_user.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == admin_user.id
    assert res.data['username'] == admin_user.username
    assert not res.data.get('password')


@mark.django_db
def test_retrieve_other(client, admin_user, regular_user, extra_users):
    # User retrieve other.
    assert client.login(username=regular_user.username, password='password')
    res = client.get('/api/user/{}/'.format(extra_users[0].id))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Admin retrieve other.
    assert client.login(username=admin_user.username, password='password')
    res = client.get('/api/user/{}/'.format(extra_users[0].id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == extra_users[0].id
    assert res.data['username'] == extra_users[0].username
    assert not res.data.get('password')


@mark.django_db
def test_update(client, admin_user, regular_user, extra_users):
    user_url = '/api/user/{}/'.format(regular_user.id)
    extra_url = '/api/user/{}/'.format(extra_users[0].id)
    admin_url = '/api/user/{}/'.format(admin_user.id)

    # User update other.
    assert client.login(username=regular_user.username, password='password')
    res = client.patch(extra_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # User update self.
    assert client.login(username=regular_user.username, password='password')
    res = client.patch(user_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Admin update other.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(extra_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert res.data['first_name'] == 'abc'

    # Admin update other with invalid password.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(extra_url, {'password': 'x'}, 'application/json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert client.login(username=extra_users[0].username, password='password')
    assert not client.login(username=extra_users[0].username, password='x')

    # Admin update other with valid password.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(extra_url, {'password': 'xyz43210'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert client.login(username=extra_users[0].username, password='xyz43210')
    assert not client.login(
        username=extra_users[0].username,
        password='password',
    )

    # Admin update self.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(admin_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert res.data['first_name'] == 'abc'

    # Admin update self with invalid password.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(admin_url, {'password': 'x'}, 'application/json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert client.login(username=admin_user.username, password='password')
    assert not client.login(username=admin_user.username, password='x')

    # Admin update self with valid password.
    assert client.login(username=admin_user.username, password='password')
    res = client.patch(admin_url, {'password': 'xyz43210'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert client.login(username=admin_user.username, password='xyz43210')
    assert not client.login(username=admin_user.username, password='password')
